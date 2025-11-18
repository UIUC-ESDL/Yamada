"""Spatial Graphs

This module contains classes and functions for working with spatial graphs.
"""


import numpy as np
import networkx as nx
from itertools import combinations
from scipy.stats import qmc

from ..sg.geometry import (rotate,
                                identify_overlapping_edges,
                           compute_counter_clockwise_angles)


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
        projection_plane_normal, pos_proj, ccw_ordering, ccw_angles = self.to_planar_embedding()
        self.projection_plane_normal = projection_plane_normal
        self.pos_proj      = pos_proj
        self.ccw_orderings = ccw_ordering
        self.ccw_angles    = ccw_angles


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
        return nx.get_node_attributes(self.G, 'pos')


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



    @staticmethod
    def subdivide_projected_edge(edge:      tuple[str, str],
                                 positions: dict,
                                 crossings: dict):
        """
        Returns a list of the vertices and crossings along a give edge
        specifically ordered from -x to +x.
        """

        # Get edge's two nodes and their positions
        leftmost_node  = edge[0] if positions[edge[0]][0] < positions[edge[1]][0] else edge[1]
        rightmost_node = edge[1] if leftmost_node == edge[0] else edge[0]
        leftmost_pos   = positions[leftmost_node]
        rightmost_pos  = positions[rightmost_node]

        # Get the crossings, if applicable
        node_labels    = [leftmost_node, rightmost_node]
        node_positions = [leftmost_pos, rightmost_pos]
        node_types     = ["vertex", "vertex"]

        for crossing, crossing_values in crossings.items():
            edge_pair = crossing_values['edges']
            if edge in edge_pair:
                node_label    = f"{crossing}"
                node_position = crossing_values['pos_2D']
                node_type     = "crossing"

                # assert leftmost_pos[0] < node_position[0] < rightmost_pos[0], \
                #        f"Crossing {crossing} must occur between the endpoints of edge {edge}."

                node_labels.append(node_label)
                node_positions.append(node_position)
                node_types.append(node_type)

        # Convert positions from dictionary to list
        node_positions = np.array(node_positions)

        # Order vertices and crossings from left to right by x position (i.e., ascending position index 0)
        x_positions = np.array(node_positions)[:, 0]
        idx_sorted  = np.argsort(x_positions)

        ordered_nodes     = [node_labels[i] for i in idx_sorted]
        ordered_types     = [node_types[i] for i in idx_sorted]
        ordered_edges     = [(ordered_nodes[i], ordered_nodes[i+1]) for i in range(len(ordered_nodes)-1)]

        return ordered_nodes, ordered_edges, ordered_types


    def subdivide_edges(self, positions, crossings):

        all_nodes = []
        all_edges = []
        all_types = []
        for edge in self.edges:
            if edge == ("comp_f", "w_ef"):
                print("HERE")
            nodes, edges, types = self.subdivide_projected_edge(edge, positions, crossings)
            all_nodes += nodes
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
        all_types = [all_types[i] for i in keep_indices]

        return all_nodes, all_edges, all_types


    def find_valid_projection_plane(self, max_iter=10, forced_rotation=None):
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
        pos_arr = np.array([self.pos[node] for node in self.nodes])

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
            pos3D_rot = {node: pos_arr_rot[i] for i, node in enumerate(self.nodes)}

            # First, check that no edges are perfectly vertical or perfectly horizontal.
            # While neither of these cases is technically incorrect, it's easier to implement looping through rotations
            # rather than add edge cases for each 2D and 3D line equation.

            for (a, b) in self.edges:
                x1, _, z1 = pos3D_rot[a]
                x2, _, z2 = pos3D_rot[b]

                if np.isclose(x1, x2) or np.isclose(z1, z2):
                    print('An edge is vertical or horizontal. This is not a valid spatial graph.')
                    bad_rotation = True
                    break

            if bad_rotation:
                continue

            crossings, invalid = identify_overlapping_edges(pos=pos3D_rot, edge_pairs=self.nonadjacent_edge_pairs)

            if invalid:
                # crossings at endpoints or other invalid conditions
                continue

            # If all are satisfied
            break


        else:
            # No rotation succeeded
            raise RuntimeError("Failed to find a valid projection (all rotations invalid).")


        return rotation, crossings


    def cyclic_ordering_vertex(self, ref_node, edges, pos, node_ordering_dict=None, node_angle_dict=None):

        # If no node ordering dictionary is provided, use the default node ordering dictionary
        if node_ordering_dict is None:
            node_ordering_dict = {}
        if node_angle_dict is None:
            node_angle_dict = {}


        pos_x = np.array(pos[ref_node], dtype=np.float64).reshape((1,2))
        nbrs = []
        for (a, b) in edges:
            if ref_node == a:
                nbrs.append(b)
            elif ref_node == b:
                nbrs.append(a)
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


    def cyclic_ordering_crossing(self, ref_node, pos, crossings, node_ordering_dict=None, node_angle_dict=None):

        # If no node ordering dictionary is provided, use the default node ordering dictionary
        if node_ordering_dict is None:
            node_ordering_dict = {}
        if node_angle_dict is None:
            node_angle_dict = {}


        # Initialize lists to store the adjacent node and edge information
        # Crossings are not relevant for this calculation since they exist along edges

        edge_1, edge_2 = crossings[ref_node]['edges']
        ori_ab, ori_cd = crossings[ref_node]['edge_order']
        oris = [ori_ab, ori_ab, ori_cd, ori_cd]
        pos_x = np.array(crossings[ref_node]['pos_2D'], dtype=np.float64)
        (a, b), (c, d) = edge_1, edge_2
        nbrs     = [a, b, c, d]
        pos_nbrs = np.array([pos[node] for node in nbrs], dtype=np.float64)

        # Shift nodes to the origin
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

    def cyclic_orderings(self, nodes, edges, node_types, positions, crossings):
        node_ordering_dict = {}
        node_angle_dict    = {}

        for node, node_type in zip(nodes, node_types):
            if node == "comp_f":
                print("HERE")

            if node_type == "vertex":
                node_ordering_dict, node_angle_dict = self.cyclic_ordering_vertex(node, edges, positions, node_ordering_dict, node_angle_dict)
            elif node_type == "crossing":
                node_ordering_dict, node_angle_dict = self.cyclic_ordering_crossing(node, positions, crossings,node_ordering_dict, node_angle_dict)

        return node_ordering_dict, node_angle_dict

    def to_planar_embedding(self, rotation=None):

        # Define the default XZ plane
        projection_plane_normal = np.array([0.0, -1.0, 0.0])

        # Find the projection plane
        rotation, crossings = self.find_valid_projection_plane(forced_rotation=rotation)

        # Rotate the projection plane
        rotated_projection_plane_normal = rotate(projection_plane_normal, rotation)

        # Rotate the positions
        pos = {}
        for node in self.nodes:
            position_3D         = np.array(self.pos[node])
            position_3D_rotated = rotate(position_3D, rotation)
            position_2D_rotated = (position_3D_rotated[0], position_3D_rotated[2])
            pos[node]           = position_2D_rotated

        # Subdivide edges to add crossings
        nodes, edges, node_types = self.subdivide_edges(pos, crossings)

        # Add the crossings
        pos.update({crossing: tuple(crossings[crossing]['pos_2D']) for crossing in crossings})

        ccw_ordering, ccw_angles = self.cyclic_orderings(nodes, edges, node_types, pos, crossings)

        return rotated_projection_plane_normal, pos, ccw_ordering, ccw_angles







    def plot(self):

        plotter = plot_spatial_graph(self.nodes, self.edges, self.pos,
                                     self.projection_plane_normal, self.pos_proj, self.ccw_orderings, self.ccw_angles)
        plotter.show()
