"""Spatial Graphs

This module contains classes and functions for working with spatial graphs.
"""

# Standard Library Imports
import bisect
import numpy as np
import networkx as nx
from itertools import combinations
from scipy.stats import qmc
import pyvista as pv

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


from ..utils.visualization import draw_spatial_graph_3d


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
                 max_iter=25,
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

    def _count_crossings_2d(self, G, pos2d, atol=1e-12):
        """
        Count proper edge-edge crossings in the 2D projection.

        Only counts intersections between non-adjacent edges
        (i.e., edges that don't share a node).
        """
        edges = list(G.edges())
        count = 0
        for (u1, v1), (u2, v2) in combinations(edges, 2):
            # Skip edges that share a node
            if len({u1, v1, u2, v2}) < 4:
                continue

            if seg_intersection(pos2d[u1], pos2d[v1],
                                pos2d[u2], pos2d[v2],
                                atol=atol) is not None:
                count += 1
        return count


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

        best_data = None
        best_crossings = None
        for i, rot in enumerate(rotations):
            rot = np.asarray(rot, float)
            pos_rot_arr = rotate(pos_arr, rot)
            pos3d_rot = {n: tuple(pos_rot_arr[i]) for i, n in enumerate(nodes)}
            pos2d, basis = self._project_points(pos3d_rot, self.projection_plane_normal)
            ok, reason = self._validate_projection(G, pos2d)
            # if ok:
            #     return rot, pos3d_rot, pos2d, basis
            if not ok:
                continue

            n_cross = self._count_crossings_2d(G, pos2d)

            if (best_crossings is None) or (n_cross < best_crossings):
                best_crossings = n_cross
                best_data = (rot, pos3d_rot, pos2d, basis)

                # Best-case scenario
                if n_cross == 0:
                    break

        if best_data is None:
            raise RuntimeError("Failed to find a valid projection rotation")
        else:
            return best_data

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
            nodes     = [node for node in self.H.nodes if "crossing" not in node]
            edges     = list(self.H.edges)
            crossings = [crossing for crossing in self.H.nodes if "crossing" in crossing]

            node_degrees = [self.H.degree(node) for node in nodes]

            # Create the vertex objects
            sgd_vertices = [Vertex(degree, 'v_' + node) for node, degree in zip(nodes, node_degrees)]

            # Create the edges
            sgd_edges    = [Edge('e_' + str(i)) for i in range(len(edges))]

            # Create the crossing objects
            sgd_crossings = [Crossing('c_' + crossing.split('_')[1]) for crossing in crossings]

            # Create a dictionary that contains the cyclical ordering of every node and crossing
            cyclic_ordering_dict = self.ccw_orderings

            # Assign the vertices to each other according to the cyclic orderings
            nodes_and_crossings = nodes + crossings
            vertices_and_crossings = sgd_vertices + sgd_crossings

            for edge, sgd_edge in zip(edges, sgd_edges):
                # TODO Use more consistent lookup
                node_a, node_b = edge

                node_a_index = nodes_and_crossings.index(node_a)
                node_b_index = nodes_and_crossings.index(node_b)

                vertex_a = vertices_and_crossings[node_a_index]
                vertex_b = vertices_and_crossings[node_b_index]

                if not vertex_a.already_assigned(vertex_b) and not vertex_b.already_assigned(vertex_a):

                    vertex_b_index_for_vertex_a = cyclic_ordering_dict[node_a][node_b]
                    vertex_a_index_for_vertex_b = cyclic_ordering_dict[node_b][node_a]

                    vertex_a[vertex_b_index_for_vertex_a] = sgd_edge[0]
                    vertex_b[vertex_a_index_for_vertex_b] = sgd_edge[1]

                else:
                    raise ValueError('The vertices are already assigned.')

            sgd = SpatialGraphDiagram(vertices=sgd_vertices, crossings=sgd_crossings, edges=sgd_edges)

            return sgd

    def plot(self):
        from ..utils.visualization import draw_spatial_graph_3d, draw_spatial_graph_2d

        plotter = pv.Plotter(shape=(1, 2), window_size=[2000, 1000])
        # plotter.camera.SetClippingRange(0.0001, 100000)

        # Plot the 3D Spatial Graph in the first subplot
        plotter.subplot(0, 0)
        plotter.add_title("3D Spatial Graph")
        draw_spatial_graph_3d(plotter, self.G.nodes, self.G.edges, self.pos3d, self.projection_plane_normal)

        # Plot the 2D Projection in the second subplot
        plotter.subplot(0, 1)
        plotter.add_title("2D Projection")
        draw_spatial_graph_2d(plotter, self.H.nodes, self.H.edges, self.pos2d,self.ccw_orderings, self.ccw_angles)

        plotter.show()
        plotter.close()
