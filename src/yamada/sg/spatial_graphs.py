"""Spatial Graphs

This module contains classes and functions for working with spatial graphs.
"""


import numpy as np
import networkx as nx
from itertools import combinations
from scipy.stats import qmc

from ..sg.geometry import (rotate,
                                compute_line_segment_intersection,
                                compute_intermediate_y_position,
                                compute_3D_intersection,
                                compute_counter_clockwise_angle)

from ..sgd.diagram_elements import Vertex, Crossing
from ..sgd.spatial_graph_diagrams import SpatialGraphDiagram
from ..utils.visualization import plot_spatial_graph


class SpatialGraph:
    """
    A class to represent a spatial graph.

    TODO Add an input checker
    TODO Fundamentally switch from rotating positions to defining rotating plane
    """



    def __init__(self,
                 nodes: list[str],
                 pos: dict,
                 edges: list[tuple[str, str]],
                 rotation=None):

        # Initialize the underlying NetworkX graph
        self.SG = nx.Graph()

        # Validate the inputs
        nodes = self._validate_nodes(nodes)
        edges = self._validate_edges(edges)
        pos   = self._validate_positions(nodes, pos)

        # Add the inputs to the SpatialGraph
        self.SG.add_nodes_from(nodes)
        self.SG.add_edges_from(edges)
        nx.set_node_attributes(self.SG, pos, 'pos')

        # self.nodes = nodes
        # self.edges = edges
        self.edge_pairs = list(combinations(self.edges, 2))

        self.adjacent_edge_pairs = self.get_adjacent_edge_pairs()
        self.nonadjacent_edge_pairs = [edge_pair for edge_pair in self.edge_pairs if
                                       edge_pair not in self.adjacent_edge_pairs]

        # Project the spatial graph onto a random the xz-plane
        # self.node_positions_3d = self.project(forced_rotation=rotation)
        pos, crossings = self.project(forced_rotation=rotation)
        nx.set_node_attributes(self.SG, pos, 'pos')
        self.crossings = crossings


    def __getattr__(self, name):
        """
        Get attributes from the underlying NetworkX graph.
        """
        return getattr(self.SG, name)


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
    def pos3D(self):
        pos = nx.get_node_attributes(self.SG, 'pos')
        return pos

    @property
    def pos2D(self):
        pos    = nx.get_node_attributes(self.SG, 'pos')
        pos_2d = {node: (position[0], position[2]) for node, position in pos.items()}
        return pos_2d


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

    def get_contiguous_edges(self):
        # TODO Same...
        # Get the sub-edges and their positions
        sub_edges, sub_edge_positions = self.subdivide_edges()

        # Get the nodes and crossings
        nodes = []
        for node_a, node_b in sub_edges:
            if node_a not in nodes:
                nodes.append(node_a)
            if node_b not in nodes:
                nodes.append(node_b)

        nodes_dict = {node: {'valency': 0, 'adjacent': []} for node in nodes}
        for sub_edge in sub_edges:
            a, b = sub_edge
            if a in nodes:
                nodes_dict[a]['valency'] += 1
                nodes_dict[a]['adjacent'].append(b)
            if b in nodes:
                nodes_dict[b]['valency'] += 1
                nodes_dict[b]['adjacent'].append(a)

        two_valent_nodes = [node for node in nodes if nodes_dict[node]['valency'] == 2]
        other_nodes_and_crossings = [node for node in nodes if node not in two_valent_nodes]

        # Start with a non-two-valent node or crossing, and then accumulate the sub-edges until another
        # non-two-valent node or crossing is reached. These are contiguous sub-edges.
        entry_points = []
        for node in other_nodes_and_crossings:
            node_entry_points = [(node, i) for i in range(nodes_dict[node]['valency'])]
            entry_points += node_entry_points

        unvisited_entry_points = entry_points.copy()

        max_iter = 1000
        iter_count = 0
        contiguous_sub_edges = []
        contiguous_sub_edge_positions = []
        while len(unvisited_entry_points) > 0:

            contiguous_sub_edge = []

            # Entry point
            entry_point = unvisited_entry_points[0]
            entry_node, entry_node_index = entry_point
            unvisited_entry_points.remove(entry_point)
            contiguous_sub_edge.append(entry_node)

            # Intermediate points
            previous_node = entry_node
            current_node = nodes_dict[entry_node]['adjacent'][entry_node_index]
            contiguous_sub_edge.append(current_node)

            while nodes_dict[current_node]['valency'] == 2:
                if nodes_dict[current_node]['adjacent'][0] == previous_node:
                    previous_node = current_node
                    current_node = nodes_dict[previous_node]['adjacent'][1]
                    contiguous_sub_edge.append(current_node)
                elif nodes_dict[current_node]['adjacent'][1] == previous_node:
                    previous_node = current_node
                    current_node = nodes_dict[previous_node]['adjacent'][0]
                    contiguous_sub_edge.append(current_node)
                else:
                    raise ValueError("Error in adjacent nodes.")

            # Exit point
            exit_node = current_node
            exit_node_index = nodes_dict[exit_node]['adjacent'].index(previous_node)
            unvisited_entry_points.remove((exit_node, exit_node_index))

            contiguous_sub_edges.append(contiguous_sub_edge)

            iter_count += 1
            if iter_count > max_iter:
                raise ValueError("Max iteration count reached.")

        # Now we will have the contiguous sub-edges, we can get their positions
        for contiguous_sub_edge in contiguous_sub_edges:
            contiguous_sub_edge_positions_i = []
            for i in range(len(contiguous_sub_edge) - 1):
                node_a = contiguous_sub_edge[i]
                node_b = contiguous_sub_edge[i + 1]
                edge = [node_a, node_b]
                edge_reversed = [node_b, node_a]
                if edge in sub_edges:
                    edge_index = sub_edges.index(edge)
                    contiguous_sub_edge_positions_i.append(sub_edge_positions[edge_index])
                elif edge_reversed in sub_edges:
                    edge_index = sub_edges.index(edge_reversed)
                    positions = sub_edge_positions[edge_index]
                    positions_reversed = [positions[1], positions[0]]
                    contiguous_sub_edge_positions_i.append(positions_reversed)
                else:
                    raise ValueError("Edge not found.")

            contiguous_sub_edge_positions.append(contiguous_sub_edge_positions_i)

        return contiguous_sub_edges,  contiguous_sub_edge_positions


    # def get_edge_vertices_and_or_crossings(self, edge):
    #     """
    #     Returns a list of the vertices and crossings along a give edge, specifically ordered from -x to +x.
    #     FIXME What if the edge is perfectly vertical?
    #     """
    #
    #
    #
    #     # Get edge's two nodes and their positions
    #     edge_nodes             = [node for node in edge]
    #     edge_node_positions_2D = [self.pos2D[node] for node in edge_nodes]
    #     edge_node_positions_3D = [self.pos3D[node] for node in edge_nodes]
    #
    #     # Get crossing and positions (if applicable)
    #     edge_crossings = []
    #     edge_crossing_positions_2D = []
    #     edge_crossing_positions_3D = []
    #     for crossing, crossing_values in self.crossings.items():
    #         edge_pair = crossing_values['edges']
    #         if edge in edge_pair:
    #             idx       = edge_pair.index(edge)
    #             orientation = crossing_values['orientation'][idx]
    #             pos2D     = crossing_values['pos_2D']
    #             pos3D     = crossing_values['pos_3D'][idx]
    #             label     = f"{crossing}_{orientation}"
    #
    #             edge_crossings.append(label)
    #             edge_crossing_positions_2D.append(pos2D)
    #             edge_crossing_positions_3D.append(pos3D)
    #
    #     if len(edge_crossings) > 0:
    #         # Merge the vertices and crossings
    #         adjacent_nodes        = edge_nodes + edge_crossings
    #         adjacent_positions_2D = np.vstack((edge_node_positions_2D, edge_crossing_positions_2D))
    #         adjacent_positions_3D = np.vstack((edge_node_positions_3D, edge_crossing_positions_3D))
    #
    #     else:
    #         adjacent_nodes        = edge_nodes
    #         adjacent_positions_2D = edge_node_positions_2D
    #         adjacent_positions_3D = edge_node_positions_3D
    #
    #     # Order vertices and crossings from left to right by x position (i.e., ascending position index 0)
    #     x_positions = np.array(adjacent_positions_2D)[:, 0]
    #     idx_sorted  = np.argsort(x_positions)
    #
    #     ordered_nodes = [adjacent_nodes[i] for i in idx_sorted]
    #     ordered_positions_2D = [adjacent_positions_2D[i] for i in idx_sorted]
    #     ordered_positions_3D = [adjacent_positions_3D[i] for i in idx_sorted]
    #
    #
    #     return ordered_nodes, ordered_positions_2D, ordered_positions_3D

    def _canon_edge(self, e: tuple[str, str]) -> tuple[str, str]:
        a, b = e
        return (a, b) if a <= b else (b, a)

    def _edge_index_in_pair_undirected(self, edge: tuple[str, str],
                                       pair: tuple[tuple[str, str], tuple[str, str]]) -> int | None:
        """Return 0 or 1 if edge matches either member of pair up to direction; else None."""
        e0, e1 = pair
        ce = self._canon_edge(edge)
        if ce == self._canon_edge(e0):
            return 0
        if ce == self._canon_edge(e1):
            return 1
        return None

    def get_edge_vertices_and_or_crossings(self, edge):
        """
        Returns ordered list of labels along the edge (endpoints + crossings),
        plus dicts mapping each label to its 2D and 3D positions.
        Ordering is left-to-right by X in the projected XZ plane.
        """
        # Endpoints
        a, b = edge
        node_labels = [a, b]
        node_pos_2d = {a: np.array(self.pos2D[a], dtype=float),
                       b: np.array(self.pos2D[b], dtype=float)}
        node_pos_3d = {a: np.array(self.pos3D[a], dtype=float),
                       b: np.array(self.pos3D[b], dtype=float)}

        # Crossings on this edge
        crossing_labels = []
        crossing_pos_2d = {}
        crossing_pos_3d = {}

        for crossing, cr in self.crossings.items():
            idx = self._edge_index_in_pair_undirected(edge, cr['edges'])
            if idx is None:
                continue

            # 2D crossing location (single point)
            p2 = np.array(cr['pos_2D'], dtype=float)
            # 3D point for this edge’s strand (over/under specific)
            p3 = np.array(cr['pos_3D'][idx], dtype=float)

            # Name this strand explicitly (you already do “crossing_k_over/under”)
            label = f"{crossing}_{cr['orientation'][idx]}"
            crossing_labels.append(label)
            crossing_pos_2d[label] = p2
            crossing_pos_3d[label] = p3

        if not crossing_labels:
            # Only endpoints
            ordered = [a, b]
            pos2d = node_pos_2d
            pos3d = node_pos_3d
            return ordered, pos2d, pos3d

        # Merge endpoints + crossings into arrays for sorting by x
        all_labels = node_labels + crossing_labels
        all_x = []
        for L in all_labels:
            if L in node_pos_2d:
                all_x.append(node_pos_2d[L][0])
            else:
                all_x.append(crossing_pos_2d[L][0])

        order = np.argsort(np.asarray(all_x))
        ordered = [all_labels[i] for i in order]

        # Build unified mapping dicts after ordering (labels remain authoritative)
        pos2d = {}
        pos3d = {}
        for L in ordered:
            if L in node_pos_2d:
                pos2d[L] = node_pos_2d[L]
                pos3d[L] = node_pos_3d[L]
            else:
                pos2d[L] = crossing_pos_2d[L]
                pos3d[L] = crossing_pos_3d[L]

        return ordered, pos2d, pos3d

    def cyclic_order_vertex(self,
                            reference_node:     str,
                            node_ordering_dict: dict = None) -> dict:
        """
        Get the cyclical order of adjacent vertexes and crossings for a given vertex.

        The spatial-topological calculations presume that nodes are ordered in a CCW rotation. While it does not matter
        which node is used as index zero, it is important that the node order is consistent.

        :param reference_node: The node to use as the reference node.
        :param node_ordering_dict: A dictionary of the node order.
        :return: A dictionary of the node order.
        """

        # If no node ordering dictionary is provided, use the default node ordering dictionary
        if node_ordering_dict is None:
            node_ordering_dict = {}

        # Get the projected node positions
        reference_node_position = np.array(self.pos2D[reference_node])

        # Initialize lists to store the adjacent node and edge information
        # Crossings are not relevant for this calculation since they exist along edges
        adjacent_nodes = list(self.neighbors(reference_node))
        adjacent_node_positions = np.array([self.pos2D[node] for node in adjacent_nodes])

        # Shift nodes to the origin
        shifted_adjacent_node_positions = adjacent_node_positions - reference_node_position

        # Horizontal line (reference for angles)
        reference_vector = np.array([1, 0])

        rotations = []
        for shifted_adjacent_node_position in shifted_adjacent_node_positions:
            rotations.append(compute_counter_clockwise_angle(reference_vector, shifted_adjacent_node_position))

        ordered_nodes = [node for _, node in sorted(zip(rotations, adjacent_nodes))]

        ccw_node_ordering = {}
        for node in ordered_nodes:
            ccw_node_ordering[node] = ordered_nodes.index(node)

        node_ordering_dict[reference_node] = ccw_node_ordering

        return node_ordering_dict

    def cyclic_order_vertices(self):
        node_ordering_dict = {}
        for node in self.nodes:
            node_ordering_dict = self.cyclic_order_vertex(node, node_ordering_dict)
        return node_ordering_dict

    # def subdivide_edge(self, edge):
    #
    #     edge_nodes_and_or_crossings, positions_2D, positions_3D = self.get_edge_vertices_and_or_crossings(edge)
    #
    #     # If there are no crossings, return empty lists
    #     if len(edge_nodes_and_or_crossings) == 2:
    #         return [], [], [], []
    #
    #     else:
    #         # Sanity check nodes are only first and last
    #         old_edges = [edge]
    #         new_nodes = [node for node in edge_nodes_and_or_crossings[1:-1]]
    #         new_edges = [(edge_nodes_and_or_crossings[i], edge_nodes_and_or_crossings[i + 1]) for i in
    #                         range(len(edge_nodes_and_or_crossings) - 1)]
    #         new_positions_3D = [tuple(positions_3D[i]) for i in range(1, len(positions_3D) - 1)]
    #
    #         return old_edges, new_nodes, new_edges, new_positions_3D

    def subdivide_edge(self, edge):
        ordered_labels, pos2d_map, pos3d_map = self.get_edge_vertices_and_or_crossings(edge)

        # No crossings → nothing to do
        if len(ordered_labels) == 2:
            return [], {}, []

        # old edge to remove
        old_edges = [edge]

        # internal labels (crossings)
        inner = ordered_labels[1:-1]

        # new edges between consecutive labels (including endpoints)
        new_edges = [(ordered_labels[i], ordered_labels[i + 1]) for i in range(len(ordered_labels) - 1)]

        # crossing positions (3D) as a dict
        new_pos_map = {L: tuple(pos3d_map[L]) for L in inner}

        return old_edges, new_pos_map, new_edges

    # def subdivide_edges(self):
    #
    #     all_edges_to_remove = []
    #     all_nodes_to_add    = []
    #     all_edges_to_add    = []
    #     all_pos_to_add      = []
    #     for edge in self.edges:
    #         edges_to_remove, nodes_to_add, edges_to_add, pos_to_add = self.subdivide_edge(edge)
    #         all_edges_to_remove += edges_to_remove
    #         all_nodes_to_add    += nodes_to_add
    #         all_edges_to_add    += edges_to_add
    #         all_pos_to_add      += pos_to_add
    #
    #     # Update the Spatial Graph (remove old edges, add crossing nodes, add new edges)
    #     self.SG.remove_edges_from(all_edges_to_remove)
    #     self.SG.add_nodes_from(all_nodes_to_add)
    #     self.SG.add_edges_from(all_edges_to_add)
    #     nx.set_node_attributes(self.SG, {node: pos for node, pos in zip(all_nodes_to_add, all_pos_to_add)}, 'pos')
    #     print("Done")

    def subdivide_edges(self):
        all_edges_to_remove = []
        all_edges_to_add = []
        pos_map_to_add = {}  # crossing_label -> 3D tuple

        for edge in self.edges:
            edges_to_remove, pos_map, edges_to_add = self.subdivide_edge(edge)
            all_edges_to_remove += edges_to_remove
            all_edges_to_add += edges_to_add
            # Later entries for the same key will overwrite earlier ones, which is fine
            # (over/under names are unique per crossing)
            pos_map_to_add.update(pos_map)

        # Mutate the graph in one shot
        self.SG.remove_edges_from(all_edges_to_remove)

        # Ensure all crossing nodes exist before setting pos
        self.SG.add_nodes_from(pos_map_to_add.keys())
        self.SG.add_edges_from(all_edges_to_add)

        # Assign positions for crossings
        nx.set_node_attributes(self.SG, pos_map_to_add, 'pos')

        print("Done")

    def get_node_or_crossing_projected_position(self, reference_node: str) -> np.ndarray:

        if reference_node in self.nodes:
            return self.pos2D[reference_node]

        elif reference_node in self.crossings:
            return self.crossing_positions[self.crossings.index(reference_node)]

        else:
            raise ValueError("Node or crossing not found.")


    def cyclic_order_crossing(self,
                              crossing:           str,
                              node_ordering_dict: dict = None):
        """
        Get the order of the overlapping nodes in the two edges. First is under, second is over.

        Use rotated node positions since rotation and project may change the overlap order.

        :param crossing: The crossing
        :param node_ordering_dict: A dictionary of node ordering for each node
        :return: overlap_order: The order of the overlapping nodes in edge 1 and edge 2
        """

        # If no node ordering dictionary is provided, use the default node ordering dictionary
        if node_ordering_dict is None:
            node_ordering_dict = {}

        # Get the edges that are connected to the crossing
        # Assumption: get_edges_of_crossing returns the edges in the order of the nodes
        edge_1, edge_2 = self.crossing_edge_pairs[self.crossings.index(crossing)]
        edge_1_nodes_and_crossings, _ = self.get_edge_vertices_and_or_crossings(edge_1)
        edge_2_nodes_and_crossings,_ = self.get_edge_vertices_and_or_crossings(edge_2)

        # Get the nodes that are adjacent to the crossing (whether a vertex or another crossing)
        # Assumption: The crossing is not the first or last node of the edge
        crossing_index_edge_1 = edge_1_nodes_and_crossings.index(crossing)
        crossing_index_edge_2 = edge_2_nodes_and_crossings.index(crossing)

        edge_1_left_node  = edge_1_nodes_and_crossings[crossing_index_edge_1 - 1]
        edge_1_right_node = edge_1_nodes_and_crossings[crossing_index_edge_1 + 1]
        edge_2_left_node  = edge_2_nodes_and_crossings[crossing_index_edge_2 - 1]
        edge_2_right_node = edge_2_nodes_and_crossings[crossing_index_edge_2 + 1]


        # Get the vertices that the beginning and end of each edge
        # While the crossing might be adjoined be other crossings, crossings only occur in 2D.
        # The 3D positions of the vertices are required to determine which edge is in front of the other.

        # Determine which vertex is the left and right vertex of each edge.
        # Assumption: Edges are ordered nodes left to right

        edge_1_left_vertex  = edge_1_nodes_and_crossings[0]
        edge_1_right_vertex = edge_1_nodes_and_crossings[-1]
        edge_2_left_vertex  = edge_2_nodes_and_crossings[0]
        edge_2_right_vertex = edge_2_nodes_and_crossings[-1]

        edge_1_left_vertex_position  = self.pos3D[edge_1_left_vertex]
        edge_1_right_vertex_position = self.pos3D[edge_1_right_vertex]
        edge_2_left_vertex_position  = self.pos3D[edge_2_left_vertex]
        edge_2_right_vertex_position = self.pos3D[edge_2_right_vertex]

        crossing_position = self.crossing_positions[self.crossings.index(crossing)]

        y_crossing_edge_1 = compute_intermediate_y_position(edge_1_left_vertex_position,
                                                            edge_1_right_vertex_position,
                                                            crossing_position[0],
                                                            crossing_position[1])

        y_crossing_edge_2 = compute_intermediate_y_position(edge_2_left_vertex_position,
                                                            edge_2_right_vertex_position,
                                                            crossing_position[0],
                                                            crossing_position[1])

        # Get the projected node positions
        reference_node_position = self.get_node_or_crossing_projected_position(crossing)

        # Initialize lists to store the adjacent node and edge information
        # Crossings are not relevant for this calculation since they exist along edges

        edge_1_left_vertex_position_projected  = self.get_node_or_crossing_projected_position(edge_1_left_vertex)
        edge_1_right_vertex_position_projected = self.get_node_or_crossing_projected_position(edge_1_right_vertex)
        edge_2_left_vertex_position_projected  = self.get_node_or_crossing_projected_position(edge_2_left_vertex)
        edge_2_right_vertex_position_projected = self.get_node_or_crossing_projected_position(edge_2_right_vertex)

        adjacent_vertex_positions_projected = [edge_1_left_vertex_position_projected, edge_1_right_vertex_position_projected, edge_2_left_vertex_position_projected, edge_2_right_vertex_position_projected]

        adjacent_nodes    = [edge_1_left_node, edge_1_right_node, edge_2_left_node, edge_2_right_node]
        adjacent_vertices = [edge_1_left_vertex, edge_1_right_vertex, edge_2_left_vertex, edge_2_right_vertex]

        # Shift nodes to the origin
        shifted_adjacent_vertex_positions = adjacent_vertex_positions_projected - reference_node_position

        # Horizontal line (reference for angles)
        reference_vector = np.array([1, 0])

        rotations = []

        # Convention: +y goes into the screen and -y goes out of the screen
        # Therefore the edge that is in front of the other is the edge that has the lower y value
        if y_crossing_edge_2 < y_crossing_edge_1:
            under_edge = edge_1
            over_edge  = edge_2
        elif y_crossing_edge_2 > y_crossing_edge_1:
            under_edge = edge_2
            over_edge  = edge_1
        else:
            raise Exception('These crossings should not intersect in 3D')

        # Calculate the angle of each node
        for shifted_adjacent_node_position in shifted_adjacent_vertex_positions:
            rotations.append(compute_counter_clockwise_angle(reference_vector, shifted_adjacent_node_position))

        # Sort the nodes by their angle
        ordered_nodes = [node for _, node in sorted(zip(rotations, adjacent_nodes))]

        # Sort the vertices by their angle (used for reference)
        ordered_vertices = [node for _, node in sorted(zip(rotations, adjacent_vertices))]

        # Check if the first node after the reference vector is on the under edge or the over edge
        first_vertex = ordered_vertices[0]
        if first_vertex in under_edge:
            crossing_indices = [0, 1, 2, 3]
        elif first_vertex in over_edge:
            crossing_indices = [1, 2, 3, 0]
        else:
            raise Exception("First node is not on either edge")

        # Assign the cyclic ordering
        ccw_crossing_ordering = {}
        for node, index in zip(ordered_nodes, crossing_indices):
            ccw_crossing_ordering[node] = index

        node_ordering_dict[crossing] = ccw_crossing_ordering

        return node_ordering_dict

    def cyclic_order_crossings(self):
        """
        Get the node ordering of the graph with crossings.

        TODO Replace crossing indices with crossings
        """
        # Create a dictionary that contains the cyclical ordering of every crossing
        crossing_ordering_dict = {}
        for crossing in self.crossings:
            crossing_ordering_dict = self.cyclic_order_crossing(crossing, crossing_ordering_dict)
        return crossing_ordering_dict


    def get_crossings(self, positions):

        crossings = {}

        for edge_1, edge_2 in self.nonadjacent_edge_pairs:

            # Get the crossing in 2D and 3D
            a, b = edge_1
            c, d = edge_2
            pos_a_3D = positions[list(self.nodes).index(a)]
            pos_b_3D = positions[list(self.nodes).index(b)]
            pos_c_3D = positions[list(self.nodes).index(c)]
            pos_d_3D = positions[list(self.nodes).index(d)]

            pos_a_2D = pos_a_3D[[0, 2]]
            pos_b_2D = pos_b_3D[[0, 2]]
            pos_c_2D = pos_c_3D[[0, 2]]
            pos_d_2D = pos_d_3D[[0, 2]]


            # First, in 2D
            min_dist, min_dist_pos, _ = compute_line_segment_intersection(pos_a_2D, pos_b_2D, pos_c_2D, pos_d_2D)
            y_ab = compute_intermediate_y_position(pos_a_3D, pos_b_3D, x_int=min_dist_pos[0], z_int=min_dist_pos[1])
            y_cd = compute_intermediate_y_position(pos_c_3D, pos_d_3D, x_int=min_dist_pos[0], z_int=min_dist_pos[1])
            pos_x_ab = np.array([min_dist_pos[0], y_ab, min_dist_pos[1]])
            pos_x_cd = np.array([min_dist_pos[0], y_cd, min_dist_pos[1]])

            if np.isclose(min_dist, 0., atol=1e-4):

                # Ensure that the crossing does not occur at an endpoint
                assert_1 = np.allclose(min_dist_pos, pos_a_2D, atol=1e-4)
                assert_2 = np.allclose(min_dist_pos, pos_b_2D, atol=1e-4)
                assert_3 = np.allclose(min_dist_pos, pos_c_2D, atol=1e-4)
                assert_4 = np.allclose(min_dist_pos, pos_d_2D, atol=1e-4)
                if any([assert_1, assert_2, assert_3, assert_4]):
                    raise ValueError('These crossings should not intersect at endpoints.')

                # elif crossing_position is np.inf:
                #     raise ValueError('The edges are overlapping. This is not a valid spatial graph.')

                # Now in 3D
                # _, pos_x_ab, pos_x_cd = compute_line_segment_intersection(pos_a_3D, pos_b_3D, pos_c_3D, pos_d_3D)


                # pos_midpoint = 0.5 * (pos_x_ab + pos_x_cd)

                edges = (edge_1, edge_2)
                label = f"crossing_{len(crossings)}"

                # Define the over and under strands, based on y position
                idx_over = np.argmax([pos_x_ab[1], pos_x_cd[1]])
                idx_under = np.argmin([pos_x_ab[1], pos_x_cd[1]])
                assert idx_over != idx_under, "Error in determining over and under strands."

                orientation = ['over', 'under'] if pos_x_ab[1] > pos_x_cd[1] else ['under', 'over']

                crossings[label] = {'edges':    edges,
                                    'pos_3D':   [pos_x_ab,pos_x_cd],
                                    'orientation': orientation,
                                    'pos_2D':   np.array([min_dist_pos[0], min_dist_pos[1]])}

                                    # 'idx_over': idx_over,
                                    # 'idx_under': idx_under,
                                    # 'pos_over': pos_x_ab if idx_over == 0 else pos_x_cd,
                                    # 'pos_under': pos_x_ab if idx_under == 0 else pos_x_cd,
                                    # 'pos_midpoint': pos_midpoint,
                                    # 'pos_2D': (pos_midpoint[0], pos_midpoint[2])}

        return crossings



    def project(self, max_iter=10, forced_rotation=None):
        """
        Project the spatial graph onto a random 2D plane.

        The projection is done by applying a random 3D rotation to the graph and then projecting it onto a 2D plane.
        For simplicity, we use the transformed XZ plane. When the rotation is complete, the program checks that the
        projected graph for several things.

        First, it checks to make sure that no combinations of edges and/or nodes are overlapping.

        Second, it checks to make sure that no edges are perfectly vertical or perfectly horizontal. While neither of
        these cases technically incorrect, it's easier to implement looping through rotations rather than add edge cases
        in for these cases.

        """

        # Convert the node positions to a numpy array
        pos_arr = np.array([self.pos3D[node] for node in self.nodes])

        # Either use the forced rotation or generate a random sequence of candidate rotations.
        if forced_rotation is not None:
            rotations = [forced_rotation]
        else:
            # Define the random rotations (in a deterministic manner w/ a Halton sequence)
            sampler        = qmc.Halton(d=3, scramble=False)
            halton_samples = sampler.random(n=max_iter)
            rotations      = 2 * np.pi * halton_samples

        for rotation in rotations:

            # Initialize the bad rotation flag
            bad_rotation = False

            # Rotate the node positions
            pos_arr_rot   = rotate(pos_arr, rotation)

            # First, check that no edges are perfectly vertical or perfectly horizontal.
            # While neither of these cases is technically incorrect, it's easier to implement looping through rotations
            # rather than add edge cases for each 2D and 3D line equation.

            for edge in self.edges:
                a, b      = edge
                x1, _, z1 = pos_arr_rot[list(self.nodes).index(a)]
                x2, _, z2 = pos_arr_rot[list(self.nodes).index(b)]

                if np.isclose(x1, x2) or np.isclose(z1, z2):
                    print('An edge is vertical or horizontal. This is not a valid spatial graph.')
                    bad_rotation = True
                    break

            if bad_rotation:
                continue

            # Second, check adjacent edge pairs for validity.
            # Since adjacent segments are straight lines, they should only intersect at a single endpoint.
            # The only other possibility is for them to infinitely overlap, which is not a valid spatial graph.

            crossings = self.get_crossings(pos_arr_rot)

            # If all are satisfied
            break


        else:
            # No rotation succeeded
            raise RuntimeError("Failed to find a valid projection (all rotations invalid).")

        # Convert back to dictionary
        pos_rot = {node: pos_arr_rot[i] for i, node in enumerate(self.nodes)}

        return pos_rot, crossings

    def to_spatial_graph_diagram(self):

        # Create a list of all nodes and crossings
        nodes_and_crossings = list(self.nodes) + list(self.crossings.keys())

        # Create the vertex and crossing objects
        vertex_node_degrees = [len([edge for edge in self.edges if node in edge]) for node in self.nodes]
        vertices = [Vertex(degree, 'v_' + node) for node, degree in zip(self.nodes,vertex_node_degrees)]

        if self.crossings is not None:
            crossings = [Crossing('c_' + str(i)) for i in range(len(self.crossings))]
        else:
            crossings = []

        vertices_and_crossings = vertices + crossings

        # Create a dictionary that contains the cyclical ordering of every node and crossing
        node_ordering_dict = self.cyclic_order_vertices()
        crossing_ordering_dict = self.cyclic_order_crossings()

        cyclic_ordering_dict = {**node_ordering_dict, **crossing_ordering_dict}

        for sub_edge in self.get_sub_edges():
            node_a, node_b = sub_edge

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


        sgd = SpatialGraphDiagram(vertices=vertices, crossings=crossings)

        return sgd

    def plot(self):

        edges = self.edges
        nodes = self.nodes
        pos = self.pos3D

        # contiguous_sub_edges, contiguous_sub_edge_positions = self.get_contiguous_edges()

        # plotter = plot_spatial_graph(nodes, node_positions, edges,contiguous_sub_edges, contiguous_sub_edge_positions)
        plotter = plot_spatial_graph(nodes, edges, pos)
        plotter.show()

