"""Spatial Graphs

This module contains classes and functions for working with spatial graphs.
"""

# Standard Library Imports
import bisect
import numpy as np
import networkx as nx
from itertools import combinations
from scipy.stats import qmc

import numpy as np
import networkx as nx
from scipy.spatial.distance import cdist
from itertools import combinations

# Local Imports
from ..sg.geometry import (rotate,
                           identify_crossings,
                           compute_counter_clockwise_angles)


from ..sgd.diagram_elements import Vertex, Crossing, Edge
from ..sgd.spatial_graph_diagrams import SpatialGraphDiagram
from .planar_embedding import PlanarEmbedding


from ..utils.visualization import plot_spatial_graph


import numpy as np
import networkx as nx
from itertools import combinations
from scipy.stats import qmc

from .planar_embedding import PlanarEmbedding


# ---------------------- low-level helpers ---------------------- #




def seg_intersection(a, b, c, d, atol=1e-10):
    """
    Proper open-segment intersection in 2D.

    Parameters
    ----------
    a, b, c, d : array_like, shape (2,)
    atol : float

    Returns
    -------
    (p, t, u) or None
        p = intersection point
        p = a + t*(b-a) = c + u*(d-c), with 0 < t,u < 1
    """
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    c = np.asarray(c, float)
    d = np.asarray(d, float)

    r = b - a
    s = d - c

    def cross(x, y):
        return x[0]*y[1] - x[1]*y[0]

    denom = cross(r, s)
    if abs(denom) < atol:
        return None

    q_p = c - a
    t = cross(q_p, s) / denom
    u = cross(q_p, r) / denom

    if atol < t < 1 - atol and atol < u < 1 - atol:
        p = a + t * r
        return p, t, u
    return None


def compute_counter_clockwise_angles(ref_vec, points):
    """
    Compute CCW angles from ref_vec to each vector in points.

    Parameters
    ----------
    ref_vec : array_like, shape (2,)
        Reference direction; angle 0 is along this vector.
    points : array_like, shape (N,2)
        Vectors from origin to neighbors.

    Returns
    -------
    angles : np.ndarray, shape (N,)
        Angles in [0, 2*pi), CCW from ref_vec.
    """
    ref_vec = np.asarray(ref_vec, float)
    points = np.asarray(points, float)

    theta_ref = np.arctan2(ref_vec[1], ref_vec[0])
    thetas = np.arctan2(points[:, 1], points[:, 0])
    angles = np.mod(thetas - theta_ref, 2*np.pi)
    return angles


# ---------------------- main class ---------------------- #

class SpatialGraph:
    """
    SpatialGraph

    - Input: nodes, 3D positions, undirected edges
    - Finds a valid rotation + 2D projection (no overlaps / degeneracies)
    - Builds a 2D graph with explicit crossing nodes
    - Computes CCW neighbor indices for each node
    """

    def __init__(self, nodes, pos, edges, rotation=None,
                 max_iter=200,
                 projection_plane_normal=np.array([0.0, -1.0, 0.0]),
                 node_tol=1e-6,
                 node_edge_tol=1e-6,
                 crossing_tol=1e-6):
        """
        Parameters
        ----------
        nodes : list[str]
            Node labels.
        pos : dict[str, tuple[float,float,float]]
            3D positions for each node.
        edges : list[tuple[str,str]]
            Undirected edges.
        rotation : array_like of length 3 or None
            If provided, only this rotation is tried; if it fails, an error is raised.
        max_iter : int
            Number of Halton-sampled rotations to try if rotation is None.
        projection_plane_normal : array_like, shape (3,)
            Normal to the projection plane (in world coordinates).
        node_tol, node_edge_tol, crossing_tol : float
            Tolerances for geometric validity checks.
        """
        self.G = nx.Graph()

        nodes   = self._validate_nodes(nodes)
        edges   = self._validate_edges(edges)
        pos     = self._validate_positions(nodes, pos)
        self.G.add_nodes_from(nodes)
        self.G.add_edges_from(edges)
        nx.set_node_attributes(self.G, pos, "pos")

        self.forced_rotation          = None if rotation is None else np.asarray(rotation, float)
        self.projection_plane_normal  = np.asarray(projection_plane_normal, float)
        self.node_tol                 = float(node_tol)
        self.node_edge_tol            = float(node_edge_tol)
        self.crossing_tol             = float(crossing_tol)
        self.max_iter                 = int(max_iter)

        # 1) Find a valid rotation and projection
        (self.rotation,
         self.pos3d_rot,
         pos2d_original,
         self.basis) = self._find_valid_projection()

        # 2) Build the projected graph with crossings
        (self.H,
         self.pos2d,
         self.crossings,
         self.strand) = self._build_projected_graph_with_crossings(self.pos3d_rot,
                                                                   pos2d_original,
                                                                   self.projection_plane_normal)

        # Tag node types: 'vertex' vs 'crossing'
        for n in self.H.nodes():
            if n in nodes:
                self.H.nodes[n]["node_type"] = "vertex"
            else:
                self.H.nodes[n]["node_type"] = "crossing"

        # 3) Compute CCW adjacency index for each node
        (self.ccw_orderings,
         self.ccw_angles) = self._compute_cyclic_orderings()

    # Delegate unknown attributes to underlying original graph if useful
    def __getattr__(self, name):
        return getattr(self.G, name)

    # -------------------- validation & accessors -------------------- #

    @staticmethod
    def _validate_nodes(nodes):
        assert isinstance(nodes, list), "Nodes must be a list."
        assert all(isinstance(n, str) for n in nodes), "All nodes must be strings."
        assert len(nodes) == len(set(nodes)), "Nodes must be unique."
        return nodes

    @staticmethod
    def _validate_edges(edges):
        assert isinstance(edges, list), "Edges must be a list."
        for e in edges:
            assert isinstance(e, tuple) and len(e) == 2, "Each edge must be (u,v)."
            u, v = e
            assert isinstance(u, str) and isinstance(v, str), "Edge endpoints must be strings."
        assert len(edges) == len(set(edges)), "Edges must be unique."
        return edges

    @staticmethod
    def _validate_positions(nodes, pos):
        assert isinstance(pos, dict), "pos must be a dict node -> (x,y,z)."
        assert set(nodes) == set(pos.keys()), "Every node must have a position and vice versa."
        cleaned = {}
        for k, p in pos.items():
            assert isinstance(p, (tuple, list, np.ndarray)), "Position must be a sequence."
            assert len(p) == 3, "Position must be 3D."
            x, y, z = p
            cleaned[k] = (float(x), float(y), float(z))
        return cleaned

    @property
    def pos3d(self):
        """Original 3D positions."""
        return nx.get_node_attributes(self.G, "pos")

    # -------------------- projection helpers -------------------- #

    @staticmethod
    def _orthonormal_basis_from_normal(n):
        n = np.asarray(n, float)
        n /= np.linalg.norm(n)
        if abs(n[0]) < 0.9:
            tmp = np.array([1.0, 0.0, 0.0])
        else:
            tmp = np.array([0.0, 1.0, 0.0])
        e1 = np.cross(n, tmp)
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(n, e1)
        e2 /= np.linalg.norm(e2)
        return e1, e2, n

    def _project_points(self, pos3d_dict, normal):
        e1, e2, n = self._orthonormal_basis_from_normal(normal)
        pos2d = {}
        for k, p in pos3d_dict.items():
            p = np.asarray(p, float)
            pos2d[k] = (p @ e1, p @ e2)
        return pos2d, {"e1": e1, "e2": e2, "n": n}

    # -------------------- projection validation -------------------- #

    @staticmethod
    def _pt_seg_dist(p, a, b):
        p = np.asarray(p, float)
        a = np.asarray(a, float)
        b = np.asarray(b, float)
        ab = b - a
        denom = float(ab @ ab)
        if denom == 0.0:
            return float(np.linalg.norm(p - a)), 0.0
        t = float((p - a) @ ab / denom)
        t = max(0.0, min(1.0, t))
        proj = a + t * ab
        return float(np.linalg.norm(p - proj)), t

    def _validate_projection(self, G, pos2d):
        """
        Enforce:
        - no node-node overlap
        - no node on edge interior
        - no multiple edges crossing at the same 2D point
        """
        nodes = list(G.nodes())
        edges = list(G.edges())

        # A) node-node overlap
        pts = np.array([pos2d[n] for n in nodes], float)
        diff = pts[:, None, :] - pts[None, :, :]
        dist2 = np.sum(diff**2, axis=-1)
        np.fill_diagonal(dist2, np.inf)
        if np.any(dist2 < self.node_tol**2):
            return False, "node-node overlap"

        # B) node-on-edge
        for n in nodes:
            p = pos2d[n]
            for u, v in edges:
                if n == u or n == v:
                    continue
                d, t = self._pt_seg_dist(p, pos2d[u], pos2d[v])
                if d < self.node_edge_tol and 0.0 < t < 1.0:
                    return False, f"node {n} lies on edge ({u},{v})"

        # C + D) edge-edge intersections & uniqueness of crossing coords
        crossing_points = []
        for (u1, v1), (u2, v2) in combinations(edges, 2):
            if len({u1, v1, u2, v2}) < 4:
                continue
            res = seg_intersection(pos2d[u1], pos2d[v1],
                                   pos2d[u2], pos2d[v2],
                                   atol=1e-12)
            if res is not None:
                p, _, _ = res
                for q in crossing_points:
                    if np.linalg.norm(p - q) < self.crossing_tol:
                        return False, "duplicate crossing point"
                crossing_points.append(p)

        return True, None

    # -------------------- rotation search -------------------- #

    def _find_valid_projection(self):
        """
        Try candidate rotations until we find one that gives a valid projection.
        """
        G = self.G
        pos3d_dict = self.pos3d
        nodes = list(G.nodes())
        pos_arr = np.array([pos3d_dict[n] for n in nodes], float)

        # build rotation candidates
        if self.forced_rotation is not None:
            rotations = [self.forced_rotation]
        else:
            sampler = qmc.Halton(d=3, scramble=False)
            samples = sampler.random(n=self.max_iter)
            rotations = [2*np.pi * row for row in samples]

        for rot in rotations:
            rot = np.asarray(rot, float)
            pos_rot_arr = rotate(pos_arr, rot)
            pos3d_rot = {n: tuple(pos_rot_arr[i]) for i, n in enumerate(nodes)}
            pos2d, basis = self._project_points(pos3d_rot, self.projection_plane_normal)
            ok, reason = self._validate_projection(G, pos2d)
            if ok:
                return rot, pos3d_rot, pos2d, basis

        raise RuntimeError("Failed to find a valid projection rotation")

    # -------------------- crossing graph construction -------------------- #

    def _build_projected_graph_with_crossings(self, pos3d_rot, pos2d, normal):
        """
        Given rotated 3D positions and their 2D projection, build a new graph H
        with crossing nodes inserted, and determine over/under strands.
        """
        G = self.G
        H = nx.Graph()

        # add original nodes
        for n in G.nodes():
            H.add_node(n, pos2d=pos2d[n], pos3d=pos3d_rot[n])

        def edge_key(u, v):
            return tuple(sorted((u, v)))

        edges = list(G.edges())
        n_vec = np.asarray(normal, float)
        n_vec /= np.linalg.norm(n_vec)

        crossings = {}
        edge_crossings = {}  # edge_key -> list of (t, crossing_id)
        strand = {}          # crossing_id -> {neighbor: 'over'/'under'}
        crossing_points = []

        counter = 0
        for (u1, v1), (u2, v2) in combinations(edges, 2):
            if len({u1, v1, u2, v2}) < 4:
                continue

            p1, p2 = pos2d[u1], pos2d[v1]
            q1, q2 = pos2d[u2], pos2d[v2]
            res = seg_intersection(p1, p2, q1, q2, atol=1e-12)
            if res is None:
                continue
            inter2d, t1, t2 = res

            # uniqueness guard (should already hold from validation)
            if any(np.linalg.norm(inter2d - cp) < self.crossing_tol for cp in crossing_points):
                continue
            crossing_points.append(inter2d)

            # 3D positions at intersection along each edge
            P1_3d = (1 - t1) * np.asarray(pos3d_rot[u1]) + t1 * np.asarray(pos3d_rot[v1])
            P2_3d = (1 - t2) * np.asarray(pos3d_rot[u2]) + t2 * np.asarray(pos3d_rot[v2])
            h1 = float(P1_3d @ n_vec)
            h2 = float(P2_3d @ n_vec)

            e1 = edge_key(u1, v1)
            e2 = edge_key(u2, v2)

            if abs(h1 - h2) < 1e-12:
                over_edge, under_edge = e1, e2  # arbitrary tie-break
            elif h1 > h2:
                over_edge, under_edge = e1, e2
            else:
                over_edge, under_edge = e2, e1

            cid = f"crossing_{counter}"
            counter += 1

            crossings[cid] = {
                "pos2d": tuple(inter2d),
                "edges": (e1, e2),
                "over_edge": over_edge,
                "under_edge": under_edge,
                "heights": {e1: h1, e2: h2},
                "t_params": {e1: t1, e2: t2},
            }
            strand[cid] = {}

            # record crossing along each edge
            for (e, t) in ((e1, t1), (e2, t2)):
                edge_crossings.setdefault(e, []).append((t, cid))

        # Add crossing nodes
        for cid, data in crossings.items():
            H.add_node(cid, pos2d=data["pos2d"], node_type="crossing")

        # Subdivide each original edge
        for (u, v) in edges:
            key = edge_key(u, v)
            pts = edge_crossings.get(key, [])
            if not pts:
                H.add_edge(u, v)
                continue

            pts_sorted = sorted(pts, key=lambda x: x[0])
            chain = [u] + [cid for (_, cid) in pts_sorted] + [v]

            for a, b in zip(chain[:-1], chain[1:]):
                H.add_edge(a, b)
                # record strand per crossing neighbor
                for node in (a, b):
                    if node in crossings:
                        cid = node
                        crossing_data = crossings[cid]
                        role = "over" if key == crossing_data["over_edge"] else "under"
                        neighbor = b if node == a else a
                        strand[cid][neighbor] = role

        pos2d_full = {n: H.nodes[n]["pos2d"] for n in H.nodes()}
        return H, pos2d_full, crossings, strand

    # -------------------- CCW adjacency (planar embedding) -------------------- #

    def _compute_cyclic_orderings(self):
        """
        Compute, for every node in H, a CCW neighbor index:

        - Vertices: neighbors ordered CCW from [0,1] and indexed 0..deg-1.
        - Crossings: 4 neighbors; sorted CCW. If the first neighbor is an
          'under' strand, indices are [0,1,2,3]; if the first is 'over',
          indices are [1,2,3,0].
        """
        H      = self.H
        pos2d  = self.pos2d
        strand = self.strand

        ccw_orderings = {}
        ccw_angles    = {}
        # ref_vec = np.array([0.0, 1.0])
        ref_vec = np.array([1.0, 0.0])

        for node in H.nodes():
            nbrs = list(H.neighbors(node))
            if not nbrs:
                ccw_orderings[node] = {}
                ccw_angles[node] = {}
                continue

            origin  = np.asarray(pos2d[node], float)
            nbr_pts = np.array([pos2d[n] for n in nbrs], float)
            rel     = nbr_pts - origin
            angles  = compute_counter_clockwise_angles(ref_vec, rel)

            order         = np.argsort(angles)
            nbrs_sorted   = [nbrs[i] for i in order]
            angles_sorted = [float(angles[i]) for i in order]

            if H.nodes[node].get("node_type", "vertex") == "vertex":
                # regular vertex: 0..deg-1 in CCW order
                idxs = list(range(len(nbrs_sorted)))
            else:
                # crossing: 4 neighbors with over/under info
                oris = [strand[node][nbr] for nbr in nbrs_sorted]
                if oris[0] == "under":
                    idxs = [0, 1, 2, 3]
                else:
                    idxs = [1, 2, 3, 0]

            node_map = {}
            angle_map = {}
            for nbr, idx, ang in zip(nbrs_sorted, idxs, angles_sorted):
                node_map[nbr] = idx
                angle_map[nbr] = ang

            ccw_orderings[node] = node_map
            ccw_angles[node] = angle_map

        return ccw_orderings, ccw_angles

    def to_planar_embedding(self):
        PE = PlanarEmbedding(self.ccw_orderings, pos=self.pos2d)
        return PE

    def to_spatial_graph_diagram(self):


            # Create a list of all nodes and crossings
            # nodes_and_crossings = list(self.nodes) + list(self.crossings.keys())
            nodes     = [node for node in self.H.nodes if "crossing" not in node]
            edges     = list(self.H.edges)
            crossings = [crossing for crossing in self.H.nodes if "crossing" in crossing]
            # crossings = list(self.crossings.keys())

            node_degrees = [self.H.degree(node) for node in nodes]

            # Create the vertex objects
            sgd_vertices = [Vertex(degree, 'v_' + node) for node, degree in zip(nodes, node_degrees)]

            # Create the edges
            # sgd_edges = [Edge('e_' + str(i)) for i in range(len(edges))]

            # Create the crossing objects
            sgd_crossings = [Crossing('c_' + crossing.split('_')[1]) for crossing in crossings]


            # Create a dictionary that contains the cyclical ordering of every node and crossing
            cyclic_ordering_dict = self.ccw_orderings


            # Assign the vertices to each other according to the cyclic orderings
            nodes_and_crossings = nodes + crossings
            vertices_and_crossings = sgd_vertices + sgd_crossings

            for edge in self.H.edges:
                # TODO Use more consistent lookup
                node_a, node_b = edge

                # if "crossing" in node_a:
                #     begin, middle, end = node_a.split("_")
                #     node_a = begin + "_" + middle
                #
                # if "crossing" in node_b:
                #     begin, middle, end = node_b.split("_")
                #     node_b = begin + "_" + middle

                node_a_index = nodes_and_crossings.index(node_a)
                node_b_index = nodes_and_crossings.index(node_b)

                vertex_a = vertices_and_crossings[node_a_index]
                vertex_b = vertices_and_crossings[node_b_index]

                if not vertex_a.already_assigned(vertex_b) and not vertex_b.already_assigned(vertex_a):

                    vertex_b_index_for_vertex_a = cyclic_ordering_dict[node_a][node_b]
                    vertex_a_index_for_vertex_b = cyclic_ordering_dict[node_b][node_a]

                    vertex_a[vertex_b_index_for_vertex_a] = vertex_b[vertex_a_index_for_vertex_b]

                else:
                    raise ValueError('The vertices are already assigned.')


            sgd = SpatialGraphDiagram(vertices=sgd_vertices, crossings=sgd_crossings)

            return sgd

    def plot(self):
        from ..utils.visualization import plot_spatial_graph

        plotter = plot_spatial_graph(self.G.nodes, self.G.edges, self.pos3d,
                                     self.H.nodes, self.H.edges, self.pos2d,
                                     self.projection_plane_normal, self.ccw_orderings, self.ccw_angles)
        plotter.show()








# """Spatial Graphs
#
# This module contains classes and functions for working with spatial graphs.
# """
#
# # Standard Library Imports
# import bisect
# import numpy as np
# import networkx as nx
# from itertools import combinations
# from scipy.stats import qmc
#
# import numpy as np
# import networkx as nx
# from scipy.spatial.distance import cdist
# from itertools import combinations
#
# # Local Imports
# from ..sg.geometry import (rotate,
#                            identify_crossings,
#                            compute_counter_clockwise_angles)
#
#
# from ..sgd.diagram_elements import Vertex, Crossing, Edge
# from ..sgd.spatial_graph_diagrams import SpatialGraphDiagram
# from .planar_embedding import PlanarEmbedding
#
#
# from ..utils.visualization import plot_spatial_graph
#
#
# class SpatialGraph:
#
#     def __init__(self,
#                  nodes: list[str],
#                  pos: dict,
#                  edges: list[tuple[str, str]],
#                  rotation=None):
#
#         # Initialize the underlying NetworkX graphs
#         self.G  = nx.Graph()
#
#         # Validate the inputs
#         nodes = self._validate_nodes(nodes)
#         edges = self._validate_edges(edges)
#         pos   = self._validate_positions(nodes, pos)
#         # TODO Validate rotation
#         self.rotation = rotation
#
#         # Add the inputs to the SpatialGraph
#         self.G.add_nodes_from(nodes)
#         self.G.add_edges_from(edges)
#         nx.set_node_attributes(self.G, pos, 'pos')
#
#
#         # # Calculate the projection
#
#         pos2d, chosen_rot = self.find_valid_projection(
#             G=self.G,
#             pos3d_original=self.pos,
#             projection_plane_normal=np.array([0.0, -1.0, 0.0]),
#         )
#
#         # self.edge_pairs = list(combinations(self.edges, 2))
#         # self.adjacent_edge_pairs = self.get_adjacent_edge_pairs()
#         # self.nonadjacent_edge_pairs = [edge_pair for edge_pair in self.edge_pairs if
#         #                                edge_pair not in self.adjacent_edge_pairs]
#
#
#         # Find the projection
#         # self.rotation, self.projection_plane_normal, self.crossings = self.find_valid_projection_plane(forced_rotation=rotation)
#         # self.subdivide_edges()
#         # self.G2 = self.subdivide_edges()
#         # self.H, self.pos2d, self.crossings = build_projected_graph_with_crossings(self.G, self.pos, normal=self.projection_plane_normal)
#
#
#         # projection_plane_normal, pos_proj, ccw_ordering, ccw_angles = self.to_planar_embedding()
#         # self.projection_plane_normal = projection_plane_normal
#         # self.pos_proj      = pos_proj
#         # self.ccw_orderings = ccw_ordering
#         # self.ccw_angles    = ccw_angles
#         # self.PE            = PlanarEmbedding(ccw_ordering, pos=pos_proj)
#
#
#     def __getattr__(self, name):
#         """
#         Get attributes from the underlying NetworkX graph.
#         """
#         return getattr(self.G, name)
#
#
#     @staticmethod
#     def _validate_nodes(nodes):
#         assert isinstance(nodes, list),                      "Nodes must be a list."
#         assert all(isinstance(node, str) for node in nodes), "All nodes must be strings."
#         assert len(nodes) == len(set(nodes)),                "All nodes must be unique."
#         return nodes
#
#     @staticmethod
#     def _validate_edges(edges):
#         assert isinstance(edges, list),                                          "Edges must be a list."
#         assert all(isinstance(s, str) and isinstance(t, str) for s, t in edges), "All edge nodes must be strings."
#         assert all(isinstance(edge, tuple) for edge in edges),                   "All edges must be tuples."
#         assert all(len(edge) == 2 for edge in edges),                            "All edges must have two nodes."
#         assert len(edges) == len(set(edges)),                                    "All edges must be unique."
#         return edges
#
#     @staticmethod
#     def _validate_positions(nodes, pos):
#         assert isinstance(pos, dict),                                         "Positions must be a dictionary."
#         assert all(isinstance(node, str) for node in pos.keys()),             "All position keys must be strings."
#         assert all(isinstance(position, tuple) for position in pos.values()), "All position values must be lists, tuples, or numpy arrays."
#         assert all(len(pos) == 3 for pos in pos.values()),                    "All position tuples must have three values."
#         assert all(isinstance(coord, (int, float)) for position in pos.values() for coord in position), "All position coordinates must be numbers."
#         assert set(nodes) == set(pos.keys()),                                 "All nodes must have a position and vice versa."
#         return pos
#
#     @property
#     def pos(self):
#         pos = nx.get_node_attributes(self.G, 'pos')
#         return pos
#
#     @property
#     def pos_projected(self):
#         pos = nx.get_node_attributes(self.G, 'pos')
#         pos_rotated = {}
#         for node in pos:
#             position = np.array(pos[node])
#             position_rotated = rotate(position, self.rotation)
#             pos_rotated[node] = tuple(position_rotated)
#         return pos_rotated
#
#
#
#     # def find_valid_projection_plane(self, max_iter=10, forced_rotation=None):
#     #     """
#     #     Project the spatial graph onto a random 2D plane.
#     #
#     #     The projection is done by applying a random 3D rotation to the graph and then projecting it onto a 2D plane.
#     #     For simplicity, we use the transformed XZ plane. When the rotation is complete, the program checks that the
#     #     projected graph for several things.
#     #
#     #     First, it checks to make sure that no combinations of edges and/or nodes are overlapping.
#     #
#     #     Second, it checks to make sure that no edges are perfectly vertical or perfectly horizontal. While neither of
#     #     these cases are technically incorrect, it's easier to implement looping through rotations rather than add edge cases
#     #     in for these cases.
#     #
#     #     """
#     #
#     #     # Define the default XZ plane
#     #     projection_plane_normal = np.array([0.0, -1.0, 0.0])
#     #
#     #     # Convert the node positions to a numpy array
#     #     pos_arr = np.array([self.pos[node] for node in self.nodes])
#     #
#     #     # Either use the forced rotation or generate a random sequence of candidate rotations.
#     #     if forced_rotation is not None:
#     #         rotations = [forced_rotation]
#     #     else:
#     #         # Define the random rotations (in a deterministic manner w/ a Halton sequence)
#     #         sampler        = qmc.Halton(d=3, scramble=False)
#     #         halton_samples = sampler.random(n=max_iter)
#     #         rotations      = 2 * np.pi * halton_samples
#     #
#     #     for rotation in rotations:
#     #
#     #         # Initialize the bad rotation flag
#     #         bad_rotation = False
#     #
#     #         # Rotate the node positions
#     #         pos_arr_rot   = rotate(pos_arr, rotation)
#     #         pos3D_rot = {node: pos_arr_rot[i] for i, node in enumerate(self.nodes)}
#     #
#     #         # First, check that no edges are perfectly vertical or perfectly horizontal.
#     #         # While neither of these cases is technically incorrect, it's easier to implement looping through rotations
#     #         # rather than add edge cases for each 2D and 3D line equation.
#     #
#     #         for (a, b) in self.edges:
#     #             x1, _, z1 = pos3D_rot[a]
#     #             x2, _, z2 = pos3D_rot[b]
#     #
#     #             if np.isclose(x1, x2) or np.isclose(z1, z2):
#     #                 print('An edge is vertical or horizontal. This is not a valid spatial graph.')
#     #                 bad_rotation = True
#     #                 break
#     #
#     #         if bad_rotation:
#     #             continue
#     #
#     #         crossings, invalid = identify_crossings(pos=pos3D_rot, edge_pairs=self.nonadjacent_edge_pairs)
#     #
#     #         if invalid:
#     #             # crossings at endpoints or other invalid conditions
#     #             continue
#     #
#     #         # If all are satisfied
#     #         break
#     #
#     #
#     #     else:
#     #         # No rotation succeeded
#     #         raise RuntimeError("Failed to find a valid projection (all rotations invalid).")
#     #
#     #     # Rotate the projection plane
#     #     rotated_projection_plane_normal = rotate(projection_plane_normal, rotation)
#     #
#     #     return rotation, rotated_projection_plane_normal, crossings
#
#     def orthonormal_basis_from_normal(self, n):
#         """Return e1, e2 spanning plane normal to n."""
#         n = np.asarray(n, float)
#         n /= np.linalg.norm(n)
#
#         if abs(n[0]) < 0.9:
#             tmp = np.array([1, 0, 0])
#         else:
#             tmp = np.array([0, 1, 0])
#
#         e1 = np.cross(n, tmp);
#         e1 /= np.linalg.norm(e1)
#         e2 = np.cross(n, e1);
#         e2 /= np.linalg.norm(e2)
#         return e1, e2, n
#
#     def project_points(self, pos3d_dict, normal):
#         """Return dict node->2D, and basis for debugging."""
#         e1, e2, n = self.orthonormal_basis_from_normal(normal)
#         pos2d = {}
#         for k, p in pos3d_dict.items():
#             p = np.asarray(p)
#             pos2d[k] = (p @ e1, p @ e2)
#         return pos2d, {'e1': e1, 'e2': e2, 'n': n}
#
#     @staticmethod
#     def validate_projection(G, pos2d, atol=1e-8):
#         """
#         Hard constraints:
#         ---------------
#         A. No node-node overlap
#         B. No node lies on edge interior
#         C. No edge-edge degeneracy (multiple crossings, or non-proper)
#         D. No identical crossing coordinates
#         """
#         nodes = list(G.nodes())
#         edges = list(G.edges())
#
#         # ----- A. Node-node overlap
#         pts = np.array([pos2d[n] for n in nodes])
#         d = cdist(pts, pts)
#         np.fill_diagonal(d, 9999)
#         if np.any(d < atol):
#             return False, "node-node collision"
#
#         # helper
#         def pt_seg_dist(p, a, b):
#             p = np.asarray(p);
#             a = np.asarray(a);
#             b = np.asarray(b)
#             t = np.dot(p - a, b - a) / np.dot(b - a, b - a)
#             t = np.clip(t, 0, 1)
#             proj = a + t * (b - a)
#             return np.linalg.norm(p - proj), t
#
#         # for gathering crossings
#         crossing_points = []
#
#         # ----- B. Node on edge
#         for n in nodes:
#             p = np.asarray(pos2d[n])
#             for u, v in edges:
#                 if n in (u, v): continue
#                 dist, t = pt_seg_dist(p, pos2d[u], pos2d[v])
#                 if dist < atol and 0 < t < 1:
#                     return False, f"node {n} lies on edge ({u},{v})"
#
#         # ----- C & D. Edge-edge intersections
#         for (u1, v1), (u2, v2) in combinations(edges, 2):
#             if len({u1, v1, u2, v2}) < 4: continue  # share endpoint -> ignore
#             res = seg_intersection(pos2d[u1], pos2d[v1], pos2d[u2], pos2d[v2], atol)
#             if res:
#                 p, _, _ = res
#                 # Check uniqueness
#                 for q in crossing_points:
#                     if np.linalg.norm(p - q) < atol:
#                         return False, "duplicate crossing point"
#                 crossing_points.append(p)
#
#         return True, None
#
#     def find_valid_projection(self, G, pos3d_original, projection_plane_normal, atol=1e-8, max_iter=10):
#
#         # Either use the forced rotation or generate a random sequence of candidate rotations.
#         if self.rotation is not None:
#             rotation_candidates = [self.rotation]
#         else:
#             # Define the random rotations (in a deterministic manner w/ a Halton sequence)
#             sampler             = qmc.Halton(d=3, scramble=False)
#             halton_samples      = sampler.random(n=max_iter)
#             rotation_candidates = 2 * np.pi * halton_samples
#
#
#         for rot in rotation_candidates:
#
#             # # 1) rotate points
#             # pos_rot = rotate(pos3d_original, rot)
#
#             # consistent ordering of nodes
#             nodes = list(G.nodes())
#             node_index = {n: i for i, n in enumerate(nodes)}
#
#             # (N,3) array of original positions
#             pos_arr = np.array([pos_dict_3d[n] for n in nodes], dtype=float)
#
#             # 2) project to 2D
#             pos2d, _ = self.project_points(pos_rot, projection_plane_normal)
#
#             # 3) validate projection
#             ok, reason = self.validate_projection(G, pos2d, atol)
#
#             if ok:
#                 return pos2d, rot
#
#         raise RuntimeError("Could not find valid rotation.")
#
#     def cyclic_ordering_vertex(self, G, ref_node, pos, node_ordering_dict=None, node_angle_dict=None):
#
#         # If no node ordering dictionary is provided, use the default node ordering dictionary
#         if node_ordering_dict is None:
#             node_ordering_dict = {}
#         if node_angle_dict is None:
#             node_angle_dict = {}
#
#
#         pos_x = np.array(pos[ref_node], dtype=np.float64).reshape((1,2))
#         # nbrs = []
#         # for (a, b) in edges:
#         #     if ref_node == a:
#         #         nbrs.append(b)
#         #     elif ref_node == b:
#         #         nbrs.append(a)
#         nbrs = list(G.neighbors(ref_node))
#         pos_nbrs = np.array([pos[node] for node in nbrs], dtype=np.float64)
#
#
#         # Shift nodes to the origin
#         pos_nbrs -= pos_x
#
#         # Horizontal line (reference for angles)
#         ref_vector = np.array([1.0, 0.0])
#
#         angles = compute_counter_clockwise_angles(ref_vector, pos_nbrs)
#
#
#         ordered_nodes     = [node     for _, node     in sorted(zip(angles, nbrs))]
#         ordered_angles    = [angle    for angle, _ in sorted(zip(angles, nbrs))]
#
#         ordered_indices = [i for i in range(len(ordered_nodes))]
#
#
#         ccw_node_ordering = {}
#         ccw_angle_ordering = {}
#         for node, idx, angle in zip(ordered_nodes, ordered_indices, ordered_angles):
#
#             ccw_node_ordering[node]  = idx
#             ccw_angle_ordering[node] = angle
#
#         node_ordering_dict[ref_node] = ccw_node_ordering
#         node_angle_dict[ref_node]    = ccw_angle_ordering
#
#         return node_ordering_dict, node_angle_dict
#
#
#     def cyclic_ordering_crossing(self, G, ref_node, pos, pos_3D, node_ordering_dict=None, node_angle_dict=None):
#
#         # If no node ordering dictionary is provided, use the default node ordering dictionary
#         if node_ordering_dict is None:
#             node_ordering_dict = {}
#         if node_angle_dict is None:
#             node_angle_dict = {}
#
#
#         # Initialize lists to store the adjacent node and edge information
#         # Crossings are not relevant for this calculation since they exist along edges
#         # FIXME Edges are stale
#         # edge_1, edge_2 = crossings[ref_node]['edges']
#         # ori_ab, ori_cd = crossings[ref_node]['edge_order']
#         # oris           = [ori_ab, ori_ab, ori_cd, ori_cd]
#         # pos_x          = np.array(crossings[ref_node]['pos_2D'], dtype=np.float64)
#         # (a, b), (c, d) = edge_1, edge_2
#         # nbrs           = [a, b, c, d]
#         nbrs = list(G.neighbors(ref_node))
#         pos_nbrs       = np.array([pos[node] for node in nbrs], dtype=np.float64)
#
#         # Shift nodes to the origin
#         pos_x = np.array(pos[ref_node], dtype=np.float64).reshape((1,2))
#         pos_nbrs -= pos_x
#
#         # Horizontal line (reference for angles)
#         ref_vector = np.array([1.0, 0.0])
#
#         angles = compute_counter_clockwise_angles(ref_vector, pos_nbrs)
#
#         ordered_nodes     = [node     for _, node     in sorted(zip(angles, nbrs))]
#         ordered_angles    = [angle    for angle, _ in sorted(zip(angles, nbrs))]
#
#         ordered_ori     = [ori for _, ori in sorted(zip(angles, oris))]
#         ordered_indices = [0, 1, 2, 3] if ordered_ori[0] == 'under' else [1, 2, 3, 0]
#
#         ccw_node_ordering = {}
#         ccw_angle_ordering = {}
#         for node, idx, angle in zip(ordered_nodes, ordered_indices, ordered_angles):
#
#             ccw_node_ordering[node]  = idx
#             ccw_angle_ordering[node] = angle
#
#         node_ordering_dict[ref_node] = ccw_node_ordering
#         node_angle_dict[ref_node]    = ccw_angle_ordering
#
#         return node_ordering_dict, node_angle_dict
#
#     def cyclic_orderings(self, G, positions, positions_3D):
#         node_ordering_dict = {}
#         node_angle_dict    = {}
#
#         # for node, node_type in zip(nodes, node_types):
#         for node in G.nodes:
#
#             node_type = G.nodes[node]['node_type']
#             if node_type == "vertex":
#                 node_ordering_dict, node_angle_dict = self.cyclic_ordering_vertex(G, node, positions, node_ordering_dict, node_angle_dict)
#             elif node_type == "crossing":
#                 node_ordering_dict, node_angle_dict = self.cyclic_ordering_crossing(G, node, positions, positions_3D,node_ordering_dict, node_angle_dict)
#
#         return node_ordering_dict, node_angle_dict
#
#     def to_planar_embedding(self, rotation=None):
#
#         # Define the default XZ plane
#         projection_plane_normal = np.array([0.0, -1.0, 0.0])
#
#         # Find the projection plane
#         rotation, crossings = self.find_valid_projection_plane(forced_rotation=rotation)
#
#         # Rotate the projection plane
#         rotated_projection_plane_normal = rotate(projection_plane_normal, rotation)
#
#         # Rotate the positions
#         pos_2D_rot = {}
#         pos_3D_rot = {}
#         for node in self.nodes:
#             position_3D         = np.array(self.pos[node])
#             position_3D_rotated = rotate(position_3D, rotation)
#             position_2D_rotated = (position_3D_rotated[0], position_3D_rotated[2])
#             pos_2D_rot[node]    = position_2D_rotated
#             pos_3D_rot[node]    = position_3D_rotated
#
#         # Subdivide edges to add crossings
#         # nodes, edges, node_types = self.subdivide_projected_edges(pos, crossings)
#         G = self.subdivide_projected_edges(pos_2D_rot, crossings)
#
#         # Add the crossings
#         pos_2D_rot.update({crossing: tuple(crossings[crossing]['pos_2D']) for crossing in crossings})
#
#         ccw_ordering, ccw_angles = self.cyclic_orderings(G, pos_2D_rot, pos_3D_rot)
#
#         return rotated_projection_plane_normal, pos_2D_rot, ccw_ordering, ccw_angles
#
#     def to_spatial_graph_diagram(self):
#
#
#         # FIXME cyclic not catching adjacent crossins 1 and 2
#         # Create a list of all nodes and crossings
#         # nodes_and_crossings = list(self.nodes) + list(self.crossings.keys())
#         nodes     = [node for node in self.Projection.nodes if "crossing" not in node]
#         edges     = list(self.Projection.edges)
#         crossings = list(self.crossings.keys())
#
#         node_degrees = [self.Projection.degree(node) for node in nodes]
#
#         # Create the vertex objects
#         sgd_vertices = [Vertex(degree, 'v_' + node) for node, degree in zip(nodes, node_degrees)]
#
#         # Create the edges
#         # sgd_edges = [Edge('e_' + str(i)) for i in range(len(edges))]
#
#         # # Create the vertex and crossing objects
#         # vertex_node_degrees = [len([edge for edge in self.edges if node in edge]) for node in self.nodes]
#         # vertices = [Vertex(degree, 'v_' + node) for node, degree in zip(self.nodes,vertex_node_degrees)]
#
#         # if self.crossings is not None:
#         #     crossings = [Crossing('c_' + str(i)) for i in range(len(self.crossings))]
#         # else:
#         #     crossings = []
#
#         # Create the crossing objects
#         sgd_crossings = [Crossing('c_' + crossing.split('_')[1]) for crossing in crossings]
#
#
#         # Create a dictionary that contains the cyclical ordering of every node and crossing
#         # node_ordering_dict = self.cyclic_order_vertices()
#         # crossing_ordering_dict = self.cyclic_order_crossings()
#         # cyclic_ordering_dict = {**node_ordering_dict, **crossing_ordering_dict}
#
#         cyclic_ordering_dict = self.node_ordering_dict
#
#
#
#
#
#
#         # Assign the vertices to each other according to the cyclic orderings
#         nodes_and_crossings = nodes + crossings
#         vertices_and_crossings = sgd_vertices + sgd_crossings
#
#         for edge in self.edges:
#             # TODO Use more consistent lookup
#             node_a, node_b = edge
#
#             if "crossing" in node_a:
#                 begin, middle, end = node_a.split("_")
#                 node_a = begin + "_" + middle
#
#             if "crossing" in node_b:
#                 begin, middle, end = node_b.split("_")
#                 node_b = begin + "_" + middle
#
#             node_a_index = nodes_and_crossings.index(node_a)
#             node_b_index = nodes_and_crossings.index(node_b)
#
#             vertex_a = vertices_and_crossings[node_a_index]
#             vertex_b = vertices_and_crossings[node_b_index]
#
#             if not vertex_a.already_assigned(vertex_b) and not vertex_b.already_assigned(vertex_a):
#
#                 vertex_b_index_for_vertex_a = cyclic_ordering_dict[node_a][node_b]
#                 vertex_a_index_for_vertex_b = cyclic_ordering_dict[node_b][node_a]
#
#                 vertex_a[vertex_b_index_for_vertex_a] = vertex_b[vertex_a_index_for_vertex_b]
#
#             else:
#                 raise ValueError('The vertices are already assigned.')
#
#
#         sgd = SpatialGraphDiagram(vertices=sgd_vertices, crossings=sgd_crossings)
#
#         return sgd
#
#
#
#
#
#
#
#     def plot(self):
#         self.ccw_orderings, self.ccw_angles = {}, {}
#         # plotter = plot_spatial_graph(self.nodes, self.edges, self.pos,
#         #                              self.projection_plane_normal, self.pos_projected, self.ccw_orderings, self.ccw_angles)
#         # plotter.show()
#
#         G = self.H
#         pos = self.pos2d
#         # pos = nx.get_node_attributes(G, 'pos')
#         nodes = G.nodes()
#         edges = G.edges()
#         plotter = plot_spatial_graph(nodes, edges, pos,
#                                      self.projection_plane_normal, self.pos_projected, self.ccw_orderings, self.ccw_angles)
#         plotter.show()
#
#
#
#
#
#
# def seg_intersection(a,b,c,d, atol=1e-10):
#     """Return intersection point + parameters or None."""
#     a=np.asarray(a); b=np.asarray(b); c=np.asarray(c); d=np.asarray(d)
#
#     r=b-a; s=d-c
#     cross=lambda x,y: x[0]*y[1]-x[1]*y[0]
#
#     denom = cross(r,s)
#     if abs(denom)<atol: return None
#
#     t = cross(c-a, s)/denom
#     u = cross(c-a, r)/denom
#
#     if atol < t < 1-atol and atol < u < 1-atol:
#         p=a+t*r
#         return (p,t,u)
#     return None