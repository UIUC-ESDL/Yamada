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


class SpatialGraph:

    def __init__(self,
                 nodes: list[str],
                 pos: dict,
                 edges: list[tuple[str, str]],
                 rotation=None):

        # Initialize the underlying NetworkX graphs
        self.G  = nx.Graph()

        # Validate the inputs
        nodes = self._validate_nodes(nodes)
        edges = self._validate_edges(edges)
        pos   = self._validate_positions(nodes, pos)

        # Add the inputs to the SpatialGraph
        self.G.add_nodes_from(nodes)
        self.G.add_edges_from(edges)
        nx.set_node_attributes(self.G, pos, 'pos')

        # Calculate the projection
        self.edge_pairs = list(combinations(self.edges, 2))
        self.adjacent_edge_pairs = self.get_adjacent_edge_pairs()
        self.nonadjacent_edge_pairs = [edge_pair for edge_pair in self.edge_pairs if
                                       edge_pair not in self.adjacent_edge_pairs]


        # Find the projection
        self.rotation, self.projection_plane_normal, self.crossings = self.find_valid_projection_plane(forced_rotation=rotation)
        # self.subdivide_edges()
        # self.G2 = self.subdivide_edges()
        self.H, self.pos2d, self.crossings = build_projected_graph_with_crossings(self.G, self.pos, normal=self.projection_plane_normal)


        # projection_plane_normal, pos_proj, ccw_ordering, ccw_angles = self.to_planar_embedding()
        # self.projection_plane_normal = projection_plane_normal
        # self.pos_proj      = pos_proj
        # self.ccw_orderings = ccw_ordering
        # self.ccw_angles    = ccw_angles
        # self.PE            = PlanarEmbedding(ccw_ordering, pos=pos_proj)


    def __getattr__(self, name):
        """
        Get attributes from the underlying NetworkX graph.
        """
        return getattr(self.G, name)


    @staticmethod
    def _validate_nodes(nodes):
        assert isinstance(nodes, list),                      "Nodes must be a list."
        assert all(isinstance(node, str) for node in nodes), "All nodes must be strings."
        assert len(nodes) == len(set(nodes)),                "All nodes must be unique."
        return nodes

    @staticmethod
    def _validate_edges(edges):
        assert isinstance(edges, list),                                          "Edges must be a list."
        assert all(isinstance(s, str) and isinstance(t, str) for s, t in edges), "All edge nodes must be strings."
        assert all(isinstance(edge, tuple) for edge in edges),                   "All edges must be tuples."
        assert all(len(edge) == 2 for edge in edges),                            "All edges must have two nodes."
        assert len(edges) == len(set(edges)),                                    "All edges must be unique."
        return edges

    @staticmethod
    def _validate_positions(nodes, pos):
        assert isinstance(pos, dict),                                         "Positions must be a dictionary."
        assert all(isinstance(node, str) for node in pos.keys()),             "All position keys must be strings."
        assert all(isinstance(position, tuple) for position in pos.values()), "All position values must be lists, tuples, or numpy arrays."
        assert all(len(pos) == 3 for pos in pos.values()),                    "All position tuples must have three values."
        assert all(isinstance(coord, (int, float)) for position in pos.values() for coord in position), "All position coordinates must be numbers."
        assert set(nodes) == set(pos.keys()),                                 "All nodes must have a position and vice versa."
        return pos

    @property
    def pos(self):
        pos = nx.get_node_attributes(self.G, 'pos')
        return pos

    @property
    def pos_projected(self):
        pos = nx.get_node_attributes(self.G, 'pos')
        pos_rotated = {}
        for node in pos:
            position = np.array(pos[node])
            position_rotated = rotate(position, self.rotation)
            pos_rotated[node] = tuple(position_rotated)
        return pos_rotated


    def get_adjacent_edge_pairs(self):
        # TODO Replace with nx functions?
        adjacent_edge_pairs = set()  # Using a set to avoid duplicates

        # Create a dictionary that maps each node to the edges that contain it
        node_to_edges = {}

        for edge in self.edges:
            a, b = edge
            if a not in node_to_edges:
                node_to_edges[a] = []
            if b not in node_to_edges:
                node_to_edges[b] = []
            node_to_edges[a].append(edge)
            node_to_edges[b].append(edge)

        # Loop through each node and find pairs of edges connected to that node
        for node, edges in node_to_edges.items():
            for i in range(len(edges)):
                for j in range(i + 1, len(edges)):
                    # Add the pair of edges to the set (unordered pair)
                    adjacent_edge_pairs.add((edges[i], edges[j]))

        return list(adjacent_edge_pairs)  # Convert set to list for the result



    # @staticmethod
    # def subdivide_projected_edge(edge:      tuple[str, str],
    #                              positions: dict,
    #                              crossings: dict):
    #     """
    #     Returns a list of the vertices and crossings along a give edge
    #     specifically ordered from -x to +x.
    #     """
    #
    #     # Get edge's two nodes and their positions
    #     a, b         = edge
    #     pos_a, pos_b = positions[a], positions[b]
    #     if pos_a[0] < pos_b[0]:
    #         leftmost_node, leftmost_pos = a, pos_a
    #         rightmost_node, rightmost_pos = b, pos_b
    #     elif pos_b[0] < pos_a[0]:
    #         leftmost_node, leftmost_pos = b, pos_b
    #         rightmost_node, rightmost_pos = a, pos_a
    #     else:
    #         raise ValueError(f"Edge {edge} is vertical in the projection; cannot subdivide.")
    #
    #     # Get the crossings, if applicable
    #     node_labels    = [leftmost_node, rightmost_node]
    #     node_positions = [leftmost_pos, rightmost_pos]
    #     node_types     = ["vertex", "vertex"]
    #
    #     for crossing, crossing_values in crossings.items():
    #         edge_pair = crossing_values['edges']
    #         if edge in edge_pair:
    #             node_label    = f"{crossing}"
    #             node_position = crossing_values['pos_2D']
    #             node_type     = "crossing"
    #
    #             is_between_x = leftmost_pos[0]  < node_position[0] < rightmost_pos[0]
    #             assert is_between_x, f"Crossing {crossing} must occur between the X endpoints of edge {edge}."
    #
    #             is_between_y = leftmost_pos[1]  < node_position[1] < rightmost_pos[1] or \
    #                            rightmost_pos[1] < node_position[1] < leftmost_pos[1]
    #             assert is_between_y, f"Crossing {crossing} must occur between the Y endpoints of edge {edge}."
    #
    #             node_labels.append(node_label)
    #             node_positions.append(node_position)
    #             node_types.append(node_type)
    #
    #     # Convert positions from dictionary to list
    #     node_positions = np.array(node_positions)
    #
    #     # Order vertices and crossings from left to right by x position (i.e., ascending position index 0)
    #     x_positions = np.array(node_positions)[:, 0]
    #     idx_sorted  = np.argsort(x_positions)
    #
    #     ordered_nodes     = [node_labels[i] for i in idx_sorted]
    #     ordered_types     = [node_types[i] for i in idx_sorted]
    #     ordered_edges     = [(ordered_nodes[i], ordered_nodes[i+1]) for i in range(len(ordered_nodes)-1)]
    #
    #     # TODO Update crossing dictionary
    #
    #     return ordered_nodes, ordered_edges, ordered_types
    #
    #
    # def subdivide_projected_edges(self, positions, crossings):
    #     all_nodes = []
    #     all_edges = []
    #     all_types = []
    #     for edge in self.edges:
    #         nodes, edges, types = self.subdivide_projected_edge(edge, positions, crossings)
    #         all_nodes += nodes
    #         all_edges += edges
    #         all_types += types
    #
    #     # Remove any repeated nodes
    #     # E.g., subdividing two edges that share the same node.
    #     seen = set()
    #     keep_indices = []
    #
    #     for i, node in enumerate(all_nodes):
    #         if node not in seen:
    #             seen.add(node)
    #             keep_indices.append(i)
    #
    #     all_nodes = [all_nodes[i] for i in keep_indices]
    #     all_types = [all_types[i] for i in keep_indices]
    #
    #     # Construct a networkx graph
    #     G = nx.Graph()
    #     for node, node_type in zip(all_nodes, all_types):
    #         G.add_node(node, node_type=node_type)
    #     G.add_edges_from(all_edges)
    #
    #     return G

    @staticmethod
    def subdivide_edge(edge:      tuple[str, str],
                       pos:       dict,
                       crossings: dict):
        """
        Returns a list of the vertices and crossings along a give edge
        specifically ordered from -x to +x.
        """

        # Get edge's two nodes and their positions
        a, b         = edge
        pos_a, pos_b = pos[a], pos[b]
        if pos_a[0] < pos_b[0]:
            leftmost_node,  leftmost_pos  = a, pos_a
            rightmost_node, rightmost_pos = b, pos_b
        elif pos_b[0] < pos_a[0]:
            leftmost_node,  leftmost_pos  = b, pos_b
            rightmost_node, rightmost_pos = a, pos_a
        else:
            raise ValueError(f"Edge {edge} is vertical in the projection; cannot subdivide.")

        # Get the crossings, if applicable
        node_labels    = [leftmost_node, rightmost_node]
        node_positions = [leftmost_pos, rightmost_pos]
        node_types     = ["vertex", "vertex"]

        for crossing, crossing_values in crossings.items():
            (edge_1, edge_2) = crossing_values['edges']

            if edge == edge_1 or edge == edge_2:

                edge_order   = crossing_values['edge_order']
                positions_3D = crossing_values['pos_3D']
                over_under   = edge_order[0] if edge == edge_1 else edge_order[1]

                node_label    = f"{crossing}_{over_under}"
                node_position = positions_3D[0] if edge == edge_1 else positions_3D[1]


                # node_position = crossing_values['pos_2D']
                node_type = "crossing"

                # is_between_x = leftmost_pos[0] < node_position[0] < rightmost_pos[0]
                # assert is_between_x, f"Crossing {crossing} must occur between the X endpoints of edge {edge}."
                #
                # is_between_y = leftmost_pos[1] < node_position[1] < rightmost_pos[1] or \
                #                rightmost_pos[1] < node_position[1] < leftmost_pos[1]
                # assert is_between_y, f"Crossing {crossing} must occur between the Y endpoints of edge {edge}."

                node_labels.append(node_label)
                node_positions.append(node_position)
                node_types.append(node_type)

        # Convert positions from dictionary to list
        node_positions = np.array(node_positions)

        # Order vertices and crossings from left to right by x position (i.e., ascending position index 0)
        x_positions = np.array(node_positions)[:, 0]
        idx_sorted = np.argsort(x_positions)


        ordered_nodes = [node_labels[i] for i in idx_sorted]
        ordered_positions = [node_positions[i] for i in idx_sorted]
        ordered_types = [node_types[i] for i in idx_sorted]
        ordered_edges = [(ordered_nodes[i], ordered_nodes[i + 1]) for i in range(len(ordered_nodes) - 1)]

        return ordered_nodes, ordered_positions, ordered_edges, ordered_types

    def subdivide_edges(self):
        all_nodes = []
        all_positions = []
        all_edges = []
        all_types = []
        for edge in self.edges:
            nodes, node_positions, edges, types = self.subdivide_edge(edge, self.pos_projected, self.crossings)
            all_nodes += nodes
            all_positions += node_positions
            all_edges += edges
            all_types += types

        # Remove any repeated nodes
        # E.g., subdividing two edges that share the same node.
        seen = set()
        keep_indices = []

        for i, node in enumerate(all_nodes):
            if node not in seen:
                seen.add(node)
                keep_indices.append(i)

        all_nodes = [all_nodes[i] for i in keep_indices]
        all_positions = [all_positions[i] for i in keep_indices]
        all_types = [all_types[i] for i in keep_indices]

        # Construct a networkx graph
        G = nx.Graph()
        for node, node_pos, node_type in zip(all_nodes, all_positions, all_types):
            G.add_node(node, pos=node_pos, node_type=node_type)
        G.add_edges_from(all_edges)
        return G

        # # Update the Spatial Graph
        # self.remove_edges_from(self.edges)
        # for node, node_position, node_type in zip(all_nodes, all_positions, all_types):
        #     if node not in self.nodes:
        #         self.add_node(node, pos=node_position, node_type=node_type)
        # self.add_edges_from(all_edges)


    # def find_valid_projection_plane(self, max_iter=10, forced_rotation=None):
    #     """
    #     Project the spatial graph onto a random 2D plane.
    #
    #     The projection is done by applying a random 3D rotation to the graph and then projecting it onto a 2D plane.
    #     For simplicity, we use the transformed XZ plane. When the rotation is complete, the program checks that the
    #     projected graph for several things.
    #
    #     First, it checks to make sure that no combinations of edges and/or nodes are overlapping.
    #
    #     Second, it checks to make sure that no edges are perfectly vertical or perfectly horizontal. While neither of
    #     these cases are technically incorrect, it's easier to implement looping through rotations rather than add edge cases
    #     in for these cases.
    #
    #     """
    #
    #     # Define the default XZ plane
    #     projection_plane_normal = np.array([0.0, -1.0, 0.0])
    #
    #     # Convert the node positions to a numpy array
    #     pos_arr = np.array([self.pos[node] for node in self.nodes])
    #
    #     # Either use the forced rotation or generate a random sequence of candidate rotations.
    #     if forced_rotation is not None:
    #         rotations = [forced_rotation]
    #     else:
    #         # Define the random rotations (in a deterministic manner w/ a Halton sequence)
    #         sampler        = qmc.Halton(d=3, scramble=False)
    #         halton_samples = sampler.random(n=max_iter)
    #         rotations      = 2 * np.pi * halton_samples
    #
    #     for rotation in rotations:
    #
    #         # Initialize the bad rotation flag
    #         bad_rotation = False
    #
    #         # Rotate the node positions
    #         pos_arr_rot   = rotate(pos_arr, rotation)
    #         pos3D_rot = {node: pos_arr_rot[i] for i, node in enumerate(self.nodes)}
    #
    #         # First, check that no edges are perfectly vertical or perfectly horizontal.
    #         # While neither of these cases is technically incorrect, it's easier to implement looping through rotations
    #         # rather than add edge cases for each 2D and 3D line equation.
    #
    #         for (a, b) in self.edges:
    #             x1, _, z1 = pos3D_rot[a]
    #             x2, _, z2 = pos3D_rot[b]
    #
    #             if np.isclose(x1, x2) or np.isclose(z1, z2):
    #                 print('An edge is vertical or horizontal. This is not a valid spatial graph.')
    #                 bad_rotation = True
    #                 break
    #
    #         if bad_rotation:
    #             continue
    #
    #         crossings, invalid = identify_crossings(pos=pos3D_rot, edge_pairs=self.nonadjacent_edge_pairs)
    #
    #         if invalid:
    #             # crossings at endpoints or other invalid conditions
    #             continue
    #
    #         # If all are satisfied
    #         break
    #
    #
    #     else:
    #         # No rotation succeeded
    #         raise RuntimeError("Failed to find a valid projection (all rotations invalid).")
    #
    #     # Rotate the projection plane
    #     rotated_projection_plane_normal = rotate(projection_plane_normal, rotation)
    #
    #     return rotation, rotated_projection_plane_normal, crossings

    def orthonormal_basis_from_normal(self, n):
        """Return e1, e2 spanning plane normal to n."""
        n = np.asarray(n, float)
        n /= np.linalg.norm(n)

        if abs(n[0]) < 0.9:
            tmp = np.array([1, 0, 0])
        else:
            tmp = np.array([0, 1, 0])

        e1 = np.cross(n, tmp);
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(n, e1);
        e2 /= np.linalg.norm(e2)
        return e1, e2, n

    def project_points(self, pos3d_dict, normal):
        """Return dict node->2D, and basis for debugging."""
        e1, e2, n = self.orthonormal_basis_from_normal(normal)
        pos2d = {}
        for k, p in pos3d_dict.items():
            p = np.asarray(p)
            pos2d[k] = (p @ e1, p @ e2)
        return pos2d, {'e1': e1, 'e2': e2, 'n': n}

    @staticmethod
    def validate_projection(G, pos2d, atol=1e-8):
        """
        Hard constraints:
        ---------------
        A. No node-node overlap
        B. No node lies on edge interior
        C. No edge-edge degeneracy (multiple crossings, or non-proper)
        D. No identical crossing coordinates
        """
        nodes = list(G.nodes())
        edges = list(G.edges())

        # ----- A. Node-node overlap
        pts = np.array([pos2d[n] for n in nodes])
        d = cdist(pts, pts)
        np.fill_diagonal(d, 9999)
        if np.any(d < atol):
            return False, "node-node collision"

        # helper
        def pt_seg_dist(p, a, b):
            p = np.asarray(p);
            a = np.asarray(a);
            b = np.asarray(b)
            t = np.dot(p - a, b - a) / np.dot(b - a, b - a)
            t = np.clip(t, 0, 1)
            proj = a + t * (b - a)
            return np.linalg.norm(p - proj), t

        # for gathering crossings
        crossing_points = []

        # ----- B. Node on edge
        for n in nodes:
            p = np.asarray(pos2d[n])
            for u, v in edges:
                if n in (u, v): continue
                dist, t = pt_seg_dist(p, pos2d[u], pos2d[v])
                if dist < atol and 0 < t < 1:
                    return False, f"node {n} lies on edge ({u},{v})"

        # ----- C & D. Edge-edge intersections
        for (u1, v1), (u2, v2) in combinations(edges, 2):
            if len({u1, v1, u2, v2}) < 4: continue  # share endpoint -> ignore
            res = seg_intersection(pos2d[u1], pos2d[v1], pos2d[u2], pos2d[v2], atol)
            if res:
                p, _, _ = res
                # Check uniqueness
                for q in crossing_points:
                    if np.linalg.norm(p - q) < atol:
                        return False, "duplicate crossing point"
                crossing_points.append(p)

        return True, None

    def find_valid_projection(self, G, pos3d_original, rotation_candidates, projection_plane_normal, atol=1e-8):

        for rot in rotation_candidates:

            # 1) rotate points
            pos_rot = rotate(pos3d_original, rot)

            # 2) project to 2D
            pos2d, _ = project_points(pos_rot, projection_plane_normal)

            # 3) validate projection
            ok, reason = self.validate_projection(G, pos2d, atol)

            if ok:
                return pos2d, rot

        raise RuntimeError("Could not find valid rotation.")

    def cyclic_ordering_vertex(self, G, ref_node, pos, node_ordering_dict=None, node_angle_dict=None):

        # If no node ordering dictionary is provided, use the default node ordering dictionary
        if node_ordering_dict is None:
            node_ordering_dict = {}
        if node_angle_dict is None:
            node_angle_dict = {}


        pos_x = np.array(pos[ref_node], dtype=np.float64).reshape((1,2))
        # nbrs = []
        # for (a, b) in edges:
        #     if ref_node == a:
        #         nbrs.append(b)
        #     elif ref_node == b:
        #         nbrs.append(a)
        nbrs = list(G.neighbors(ref_node))
        pos_nbrs = np.array([pos[node] for node in nbrs], dtype=np.float64)


        # Shift nodes to the origin
        pos_nbrs -= pos_x

        # Horizontal line (reference for angles)
        ref_vector = np.array([1.0, 0.0])

        angles = compute_counter_clockwise_angles(ref_vector, pos_nbrs)


        ordered_nodes     = [node     for _, node     in sorted(zip(angles, nbrs))]
        ordered_angles    = [angle    for angle, _ in sorted(zip(angles, nbrs))]

        ordered_indices = [i for i in range(len(ordered_nodes))]


        ccw_node_ordering = {}
        ccw_angle_ordering = {}
        for node, idx, angle in zip(ordered_nodes, ordered_indices, ordered_angles):

            ccw_node_ordering[node]  = idx
            ccw_angle_ordering[node] = angle

        node_ordering_dict[ref_node] = ccw_node_ordering
        node_angle_dict[ref_node]    = ccw_angle_ordering

        return node_ordering_dict, node_angle_dict


    def cyclic_ordering_crossing(self, G, ref_node, pos, pos_3D, node_ordering_dict=None, node_angle_dict=None):

        # If no node ordering dictionary is provided, use the default node ordering dictionary
        if node_ordering_dict is None:
            node_ordering_dict = {}
        if node_angle_dict is None:
            node_angle_dict = {}


        # Initialize lists to store the adjacent node and edge information
        # Crossings are not relevant for this calculation since they exist along edges
        # FIXME Edges are stale
        # edge_1, edge_2 = crossings[ref_node]['edges']
        # ori_ab, ori_cd = crossings[ref_node]['edge_order']
        # oris           = [ori_ab, ori_ab, ori_cd, ori_cd]
        # pos_x          = np.array(crossings[ref_node]['pos_2D'], dtype=np.float64)
        # (a, b), (c, d) = edge_1, edge_2
        # nbrs           = [a, b, c, d]
        nbrs = list(G.neighbors(ref_node))
        pos_nbrs       = np.array([pos[node] for node in nbrs], dtype=np.float64)

        # Shift nodes to the origin
        pos_x = np.array(pos[ref_node], dtype=np.float64).reshape((1,2))
        pos_nbrs -= pos_x

        # Horizontal line (reference for angles)
        ref_vector = np.array([1.0, 0.0])

        angles = compute_counter_clockwise_angles(ref_vector, pos_nbrs)

        ordered_nodes     = [node     for _, node     in sorted(zip(angles, nbrs))]
        ordered_angles    = [angle    for angle, _ in sorted(zip(angles, nbrs))]

        ordered_ori     = [ori for _, ori in sorted(zip(angles, oris))]
        ordered_indices = [0, 1, 2, 3] if ordered_ori[0] == 'under' else [1, 2, 3, 0]

        ccw_node_ordering = {}
        ccw_angle_ordering = {}
        for node, idx, angle in zip(ordered_nodes, ordered_indices, ordered_angles):

            ccw_node_ordering[node]  = idx
            ccw_angle_ordering[node] = angle

        node_ordering_dict[ref_node] = ccw_node_ordering
        node_angle_dict[ref_node]    = ccw_angle_ordering

        return node_ordering_dict, node_angle_dict

    def cyclic_orderings(self, G, positions, positions_3D):
        node_ordering_dict = {}
        node_angle_dict    = {}

        # for node, node_type in zip(nodes, node_types):
        for node in G.nodes:

            node_type = G.nodes[node]['node_type']
            if node_type == "vertex":
                node_ordering_dict, node_angle_dict = self.cyclic_ordering_vertex(G, node, positions, node_ordering_dict, node_angle_dict)
            elif node_type == "crossing":
                node_ordering_dict, node_angle_dict = self.cyclic_ordering_crossing(G, node, positions, positions_3D,node_ordering_dict, node_angle_dict)

        return node_ordering_dict, node_angle_dict

    def to_planar_embedding(self, rotation=None):

        # Define the default XZ plane
        projection_plane_normal = np.array([0.0, -1.0, 0.0])

        # Find the projection plane
        rotation, crossings = self.find_valid_projection_plane(forced_rotation=rotation)

        # Rotate the projection plane
        rotated_projection_plane_normal = rotate(projection_plane_normal, rotation)

        # Rotate the positions
        pos_2D_rot = {}
        pos_3D_rot = {}
        for node in self.nodes:
            position_3D         = np.array(self.pos[node])
            position_3D_rotated = rotate(position_3D, rotation)
            position_2D_rotated = (position_3D_rotated[0], position_3D_rotated[2])
            pos_2D_rot[node]    = position_2D_rotated
            pos_3D_rot[node]    = position_3D_rotated

        # Subdivide edges to add crossings
        # nodes, edges, node_types = self.subdivide_projected_edges(pos, crossings)
        G = self.subdivide_projected_edges(pos_2D_rot, crossings)

        # Add the crossings
        pos_2D_rot.update({crossing: tuple(crossings[crossing]['pos_2D']) for crossing in crossings})

        ccw_ordering, ccw_angles = self.cyclic_orderings(G, pos_2D_rot, pos_3D_rot)

        return rotated_projection_plane_normal, pos_2D_rot, ccw_ordering, ccw_angles

    def to_spatial_graph_diagram(self):


        # FIXME cyclic not catching adjacent crossins 1 and 2
        # Create a list of all nodes and crossings
        # nodes_and_crossings = list(self.nodes) + list(self.crossings.keys())
        nodes     = [node for node in self.Projection.nodes if "crossing" not in node]
        edges     = list(self.Projection.edges)
        crossings = list(self.crossings.keys())

        node_degrees = [self.Projection.degree(node) for node in nodes]

        # Create the vertex objects
        sgd_vertices = [Vertex(degree, 'v_' + node) for node, degree in zip(nodes, node_degrees)]

        # Create the edges
        # sgd_edges = [Edge('e_' + str(i)) for i in range(len(edges))]

        # # Create the vertex and crossing objects
        # vertex_node_degrees = [len([edge for edge in self.edges if node in edge]) for node in self.nodes]
        # vertices = [Vertex(degree, 'v_' + node) for node, degree in zip(self.nodes,vertex_node_degrees)]

        # if self.crossings is not None:
        #     crossings = [Crossing('c_' + str(i)) for i in range(len(self.crossings))]
        # else:
        #     crossings = []

        # Create the crossing objects
        sgd_crossings = [Crossing('c_' + crossing.split('_')[1]) for crossing in crossings]


        # Create a dictionary that contains the cyclical ordering of every node and crossing
        # node_ordering_dict = self.cyclic_order_vertices()
        # crossing_ordering_dict = self.cyclic_order_crossings()
        # cyclic_ordering_dict = {**node_ordering_dict, **crossing_ordering_dict}

        cyclic_ordering_dict = self.node_ordering_dict






        # Assign the vertices to each other according to the cyclic orderings
        nodes_and_crossings = nodes + crossings
        vertices_and_crossings = sgd_vertices + sgd_crossings

        for edge in self.edges:
            # TODO Use more consistent lookup
            node_a, node_b = edge

            if "crossing" in node_a:
                begin, middle, end = node_a.split("_")
                node_a = begin + "_" + middle

            if "crossing" in node_b:
                begin, middle, end = node_b.split("_")
                node_b = begin + "_" + middle

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
        self.ccw_orderings, self.ccw_angles = {}, {}
        # plotter = plot_spatial_graph(self.nodes, self.edges, self.pos,
        #                              self.projection_plane_normal, self.pos_projected, self.ccw_orderings, self.ccw_angles)
        # plotter.show()

        G = self.H
        pos = self.pos2d
        # pos = nx.get_node_attributes(G, 'pos')
        nodes = G.nodes()
        edges = G.edges()
        plotter = plot_spatial_graph(nodes, edges, pos,
                                     self.projection_plane_normal, self.pos_projected, self.ccw_orderings, self.ccw_angles)
        plotter.show()






def seg_intersection(a,b,c,d, atol=1e-10):
    """Return intersection point + parameters or None."""
    a=np.asarray(a); b=np.asarray(b); c=np.asarray(c); d=np.asarray(d)

    r=b-a; s=d-c
    cross=lambda x,y: x[0]*y[1]-x[1]*y[0]

    denom = cross(r,s)
    if abs(denom)<atol: return None

    t = cross(c-a, s)/denom
    u = cross(c-a, r)/denom

    if atol < t < 1-atol and atol < u < 1-atol:
        p=a+t*r
        return (p,t,u)
    return None