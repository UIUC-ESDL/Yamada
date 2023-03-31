"""Spatial Graphs

This module contains classes and functions for working with spatial graphs.
"""

import numpy as np
from numpy import sin, cos
import matplotlib.pyplot as plt
from itertools import combinations

from .spatial_graph_diagrams import (Vertex, Crossing, SpatialGraphDiagram)


class AbstractGraph:
    """
    TODO Figure out what happens if the graph has dangling edges
    """

    def __init__(self,
                 nodes: list[str],
                 edges: list[tuple[str, str]]):

        self.nodes = self._validate_nodes(nodes)
        self.edges = self._validate_edges(edges)

    @staticmethod
    def _validate_nodes(nodes: list[str]) -> list[str]:
        """
        Validates the user's input and returns a list of nodes.

        Checks:
        1. The input is a list
        2. Each node is a string
        3. Each node string only contains alphanumeric characters
        4. All nodes are unique
        """

        if type(nodes) != list:
            raise TypeError('Nodes must be a list.')

        for node in nodes:
            if type(node) != str:
                raise TypeError('Nodes must be strings.')

        for node in nodes:
            if len(node) == 0:
                raise ValueError('Nodes must be a at least a single character.')

        if len(nodes) != len(set(nodes)):
            raise ValueError('All nodes must be unique.')

        # TODO Temporarily disabled for nodes like crossing "C1+" and "C1-".
        # for node in nodes:
        #     if not node.isalnum():
        #         raise ValueError('Nodes must be alphanumeric.')

        return nodes

    def _validate_edges(self, edges: list[tuple[str, str]]) -> list[tuple[str, str]]:
        """
        Validates the user's input and returns a list of edges.

        Checks:
        1. The input is a list
        2. Each edge is a tuple
        3. Each edge contains two valid nodes
        4. All edges are unique
        """

        if type(edges) != list:
            raise TypeError('Edges must be a list.')

        for edge in edges:
            if type(edge) != tuple:
                raise TypeError('Edge must be tuples.')

        for edge in edges:
            if len(edge) != 2:
                raise ValueError('Edges must contain two nodes.')

        for edge in edges:
            for node in edge:
                if node not in self.nodes:
                    raise ValueError('Edges must contain valid nodes.')

        if len(edges) != len(set(edges)):
            raise ValueError('All edges must be unique.')

        return edges

    def node_degree(self, node: str) -> int:
        """
        Returns the degree of a node.

        The node degree is the number of edges that are incident to the node.
        """
        return len([edge for edge in self.edges if node in edge])

    def get_adjacent_nodes(self, reference_node: str) -> list[str]:
        """
        Get the adjacent nodes to a given node.
        """

        adjacent_nodes = []

        for edge in self.edges:
            if reference_node == edge[0] or reference_node == edge[1]:
                adjacent_nodes += [node for node in edge if node != reference_node]

        return adjacent_nodes

    @property
    def edge_pairs(self):
        return list(combinations(self.edges, 2))

    @property
    def adjacent_edge_pairs(self):

        adjacent_edge_pairs = []

        for edge_1, edge_2 in self.edge_pairs:

            a, b = edge_1
            c, d = edge_2

            assertion_1 = a in [c, d]
            assertion_2 = b in [c, d]

            if assertion_1 or assertion_2:
                adjacent_edge_pairs += [(edge_1, edge_2)]

        return adjacent_edge_pairs


class LinearAlgebra:
    """
    A class that contains static methods for necessary linear algebra calculations.
    """

    def __init__(self):
        self.rotated_node_positions = None
        self.rotation_generator_object = self.rotation_generator()
        self.rotation = self.random_rotation()

    @staticmethod
    def rotation_generator():
        """
        A generator to generate random rotations for projecting a spatial graph onto a 2D plane. Angles in radians.
        """

        # Set the initial generator state to zero.
        rotation = np.zeros(3)

        while True:
            yield rotation
            rotation = np.random.rand(3) * 2 * np.pi

    def random_rotation(self):
        """
        Query the rotation generator for a new rotation.
        """
        return next(self.rotation_generator_object)

    @staticmethod
    def rotate(positions: np.ndarray,
               rotation:  np.ndarray) -> np.ndarray:
        """
        Rotates a set of points about the first 3D point in the array.

        :param positions: A numpy array of 3D points.
        :param rotation: A numpy array of 3 Euler angles in radians.

        :return: new_positions:
        """

        # Shift the object to origin
        reference_position = positions[0]
        origin_positions = positions - reference_position

        alpha, beta, gamma = rotation

        # Rotation matrix Euler angle convention r = r_z(gamma) @ r_y(beta) @ r_x(alpha)

        r_x = np.array([[1., 0., 0.],
                        [0., cos(alpha), -sin(alpha)],
                        [0., sin(alpha), cos(alpha)]])

        r_y = np.array([[cos(beta), 0., sin(beta)],
                        [0., 1., 0.],
                        [-sin(beta), 0., cos(beta)]])

        r_z = np.array([[cos(gamma), -sin(gamma), 0.],
                        [sin(gamma), cos(gamma), 0.],
                        [0., 0., 1.]])

        # TODO Replace with explicitly formulated matrix
        r = r_z @ r_y @ r_x

        # Transpose positions from [[x1,y1,z1],[x2... ] to [[x1,x2,x3],[y1,... ]
        rotated_origin_positions = (r @ origin_positions.T).T

        # Shift back from origin
        new_positions = rotated_origin_positions + reference_position

        rotated_node_positions = new_positions

        return rotated_node_positions

    @staticmethod
    def get_line_segment_intersection(a: np.ndarray,
                                      b: np.ndarray,
                                      c: np.ndarray,
                                      d: np.ndarray) -> tuple[float, np.ndarray]:
        """
        Returns the minimum Euclidean distance between two line segments and its position.

        This function also works for calculating the distance between a line segment and a point and a point and point.

        Based on the algorithm described in:

        Vladimir J. Lumelsky,
        "On Fast Computation of Distance Between Line Segments",
        Information Processing Letters 21 (1985) 55-61
        https://doi.org/10.1016/0020-0190(85)90032-8

        Values 0 <= t <= 1 correspond to points being inside segment AB whereas values < 0  correspond to being 'left' of AB
        and values > 1 correspond to being 'right' of AB.

        Values 0 <= u <= 1 correspond to points being inside segment CD whereas values < 0  correspond to being 'left' of CD
        and values > 1 correspond to being 'right' of CD.

        Step 1: Check for special cases; compute D1, D2, and the denominator in (11)
            (a) If one of the two segments degenerates into a point, assume that this segment corresponds to the parameter
            u, take u=0, and go to Step 4.
            (b) If both segments degenerate into points, take t=u=0, and go to Step 5.
            (c) If neither of two segments degenerates into a point and the denominator in (11) is zero, take t=0 and go to
            Step 3.
            (d) If none of (a), (b), (c) takes place, go to Step 2.
        Step 2: Using (11) compute t. If t is not in the range [0,1], modify t using (12).
        Step 3: Using (10) compute u. If u is not in the range [0,1], modify u using (12); otherwise, go to Step 5.
        Step 4: Using (10) compute t. If t is not in the range [0,1], modify t using (12).
        Step 5: With current values of t and u, compute the actual MinD using (7).

        :param a: (1,3) numpy array
        :param b: (1,3) numpy array
        :param c: (1,3) numpy array
        :param d: (1,3) numpy array

        :return: Minimum distance between line segments, float
        :return: Position of minimum distance, (1,3) numpy array
        """

        def clamp_bound(num):
            """
            If the number is outside the range [0,1] then clamp it to the nearest boundary.
            """
            if num < 0.:
                return 0.
            elif num > 1.:
                return 1.
            else:
                return num

        d1  = b - a
        d2  = d - c
        d12 = c - a

        D1  = np.dot(d1, d1.T)
        D2  = np.dot(d2, d2.T)
        S1  = np.dot(d1, d12.T)
        S2  = np.dot(d2, d12.T)
        R   = np.dot(d1, d2.T)
        den = np.dot(D1, D2) - np.square(R)

        # Check if one or both line segments are points
        if D1 == 0. or D2 == 0.:

            # Both AB and CD are points
            if D1 == 0. and D2 == 0.:
                t = 0.
                u = 0.

            # AB is a line segment and CD is a point
            elif D1 != 0.:
                u = 0.
                t = S1 / D1
                t = clamp_bound(t)

            # AB is a point and CD is a line segment
            elif D2 != 0.:
                t = 0.
                u = -S2 / D2
                u = clamp_bound(u)

        # Check if line segments are parallel
        elif den == 0.:
            t = 0.
            u = -S2 / D2
            uf = clamp_bound(u)

            if uf != u:
                t = (uf * R + S1) / D1
                t = clamp_bound(t)
                u = uf

        # General case for calculating the minimum distance between two line segments
        else:

            t = (S1 * D2 - S2 * R) / den

            t = clamp_bound(t)

            u = (t * R - S2) / D2
            uf = clamp_bound(u)

            if uf != u:
                t = (uf * R + S1) / D1
                t = clamp_bound(t)

                u = uf

        min_dist = np.linalg.norm(d1 * t - d2 * u - d12)

        if not np.isclose(min_dist, 0):
            min_dist_position = None
        else:
            min_dist_position = np.array([a + d1 * t]).reshape(-1)

        return min_dist, min_dist_position


    @staticmethod
    def calculate_intermediate_y_position(a:     np.ndarray,
                                          b:     np.ndarray,
                                          x_int: float,
                                          z_int: float) -> float:
        """
        Calculates the intermediate y position given two points and the intermediate x and z position.
        """

        x1, y1, z1 = a
        x2, y2, z2 = b

        delta_x = x2 - x1
        delta_y = y2 - y1
        delta_z = z2 - z1

        ratio_x = (x_int - x1) / delta_x
        ratio_z = (z_int - z1) / delta_z

        assert np.isclose(ratio_x, ratio_z, rtol=1e-3)

        y_int = y1 + ratio_x * delta_y

        return y_int

    @property
    def projected_node_positions(self):
        return self.rotated_node_positions[:, [0, 2]]


    @staticmethod
    def calculate_counter_clockwise_angle(vector_a: np.ndarray,
                                          vector_b: np.ndarray) -> float:
        """
        Returns the angle in degrees between vectors 'A' and 'B'.

        :param vector_a: A numpy array of shape (2,) representing containing positions x_a and y_a.
        :param vector_b: A numpy array of shape (2,) representing containing positions x_b and y_b.
        :return: The angle in degrees between vectors A and B, where 0 <= angle < 360.
        """

        def length(v):
            return np.sqrt(v[0] ** 2 + v[1] ** 2)

        def dot_product(v, w):
            return v[0] * w[0] + v[1] * w[1]

        def determinant(v, w):
            return v[0] * w[1] - v[1] * w[0]

        def inner_angle(v, w):
            cosx = dot_product(v, w) / (length(v) * length(w))
            rad = np.arccos(cosx)     # in radians
            return rad * 180 / np.pi  # returns degrees

        inner = inner_angle(vector_a, vector_b)
        det = determinant(vector_a, vector_b)

        if det > 0:  # this is a property of the det. If the det < 0 then B is clockwise of A
            return inner
        else:  # if the det > 0 then A is immediately clockwise of B
            return 360 - inner


class SpatialGraph(AbstractGraph, LinearAlgebra):
    """
    A class to represent a spatial graph.

    Notes:
        1. Component ports must be individually represented as nodes. In other words, a control valve servicing an
        actuator must employ separate nodes for the supply and return ports, along with their associated edges.
    """

    def __init__(self,
                 nodes: list[str],
                 node_positions: np.ndarray,
                 edges: list[tuple[str, str]]):

        # Initialize AbstractGraph Class
        AbstractGraph.__init__(self, nodes, edges)

        # Initialize Node positions
        self.node_positions = self._validate_node_positions(node_positions)

        # Initialize attributes necessary for geometric calculations
        LinearAlgebra.__init__(self)

        # Initialize a first rotation
        self.rotated_node_positions = self.rotate(self.node_positions, self.rotation)

        # Initialize attributes that are calculated later
        self.crossings = None
        self.crossing_positions = None
        self.crossing_edge_pairs = None

        # Project the spatial graph onto a random the xz-plane
        self.project()

    def _validate_node_positions(self,
                                 node_positions: np.ndarray) -> np.ndarray:
        """
        Validates the user's input and returns an array of node positions.

        Checks:
        1. The input is a np.ndarray
        2. The array size matches the number of nodes
        3. Each row contains 3 real numbers
        4. Each row is unique
        """

        if type(node_positions) != np.ndarray:

            # TODO Check for if elements in list are not numbers, etc.
            if type(node_positions) == list:
                node_positions = np.array(node_positions)

            else:
                raise TypeError('Node positions must be a numpy array.')

        if node_positions.shape[0] != len(self.nodes):
            raise ValueError('Node positions must contain a position for each node.')

        if node_positions.shape[1] != 3:
            raise ValueError('Node positions must contain 3D coordinates.')

        valid_types = [float, int, np.float32, np.int32, np.float64, np.int64]
        for row in node_positions:
            for element in row:
                if type(element) not in valid_types:
                    raise TypeError('Node positions must contain real numbers.')

        if node_positions.shape[0] != np.unique(node_positions, axis=0).shape[0]:
            raise ValueError('All nodes must have a position.')

        return node_positions

    def get_vertices_and_crossings_of_edge(self, reference_edge: tuple[str, str]):
        """
        Returns the vertices and crossings of an edge, ordered from left to right.
        """

        # Get edge nodes and positions
        edge_nodes = [node for node in reference_edge]
        edge_node_positions = [self.projected_node_positions[self.nodes.index(node)] for node in edge_nodes]

        # Get crossing and positions (if applicable)
        edge_crossings = []
        edge_crossing_positions = []

        for edge_pair, position, crossing in zip(self.crossing_edge_pairs, self.crossing_positions, self.crossings):
            if reference_edge in edge_pair:
                edge_crossings.append(crossing)
                edge_crossing_positions.append(position)

        if len(edge_crossings) > 0:
            # Merge the vertices and crossings
            adjacent_nodes = edge_nodes + edge_crossings
            adjacent_positions = np.vstack((edge_node_positions, edge_crossing_positions))

        else:
            adjacent_nodes = edge_nodes
            adjacent_positions = edge_node_positions

        # Order vertices and crossings from left to right by x position (i.e., ascending position index 0)
        ordered_nodes = [node for _, node in
                         sorted(zip(adjacent_positions, adjacent_nodes), key=lambda pair: pair[0][0])]

        return ordered_nodes

    def get_adjacent_nodes_or_crossings(self, reference_node):
        """
        Get the adjacent nodes to a given node.
        """

        adjacent_nodes = []

        for edge in self.get_sub_edges():
            if reference_node == edge[0] or reference_node == edge[1]:
                adjacent_nodes += [node for node in edge if node != reference_node]

        return adjacent_nodes

    def get_adjacent_nodes_projected_positions(self, reference_node: str):
        """
        Get the adjacent nodes to a given node.
        """
        adjacent_nodes = self.get_adjacent_nodes(reference_node)

        node_indices = [self.nodes.index(node) for node in adjacent_nodes]

        return self.projected_node_positions[node_indices]

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
        reference_node_position = self.projected_node_positions[self.nodes.index(reference_node)]

        # Initialize lists to store the adjacent node and edge information
        # Crossings are not relevant for this calculation since they exist along edges
        adjacent_nodes = self.get_adjacent_nodes_or_crossings(reference_node)
        adjacent_node_positions = self.get_adjacent_nodes_projected_positions(reference_node)

        # Shift nodes to the origin
        shifted_adjacent_node_positions = adjacent_node_positions - reference_node_position

        # Horizontal line (reference for angles)
        reference_vector = np.array([1, 0])

        rotations = []
        for shifted_adjacent_node_position in shifted_adjacent_node_positions:
            rotations.append(self.calculate_counter_clockwise_angle(reference_vector, shifted_adjacent_node_position))

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

    def get_sub_edges(self):
        """
        Sub-edges constitute:
        1. Edges that are not incident of a crossing (i.e., the edge is the sub-edge)
        2. When an edge is incident to a crossing(s), the edge is divided into one or more sub-edges depending on the
        number of crossings that the edge is incident to.
        """

        # Get the nodes and crossings of each edge, ordered from left to right
        edge_nodes_and_crossings = {}
        for edge in self.edges:
            edge_nodes_and_crossings[edge] = self.get_vertices_and_crossings_of_edge(edge)

        # Subdivide each edge if necessary.
        # If there are 2 nodes then there is one sub-edge, 3 nodes means 2 sub-edges, etc.

        sub_edges = []

        for edge, nodes_and_crossings in edge_nodes_and_crossings.items():

            if len(nodes_and_crossings) == 2:
                sub_edges.append(edge)

            else:
                sub_edges += [(nodes_and_crossings[i], nodes_and_crossings[i + 1]) for i in
                              range(len(nodes_and_crossings) - 1)]

        return sub_edges


    def get_node_or_crossing_projected_position(self, reference_node: str) -> np.ndarray:

        if reference_node in self.nodes:
            return self.projected_node_positions[self.nodes.index(reference_node)]

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
        edge_1_nodes_and_crossings = self.get_vertices_and_crossings_of_edge(edge_1)
        edge_2_nodes_and_crossings = self.get_vertices_and_crossings_of_edge(edge_2)

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

        edge_1_left_vertex_position  = self.rotated_node_positions[self.nodes.index(edge_1_left_vertex)]
        edge_1_right_vertex_position = self.rotated_node_positions[self.nodes.index(edge_1_right_vertex)]
        edge_2_left_vertex_position  = self.rotated_node_positions[self.nodes.index(edge_2_left_vertex)]
        edge_2_right_vertex_position = self.rotated_node_positions[self.nodes.index(edge_2_right_vertex)]

        crossing_position = self.crossing_positions[self.crossings.index(crossing)]

        y_crossing_edge_1 = self.calculate_intermediate_y_position(edge_1_left_vertex_position,
                                                                   edge_1_right_vertex_position,
                                                                   crossing_position[0],
                                                                   crossing_position[1])

        y_crossing_edge_2 = self.calculate_intermediate_y_position(edge_2_left_vertex_position,
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
            rotations.append(self.calculate_counter_clockwise_angle(reference_vector, shifted_adjacent_node_position))

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

    def get_crossing_edge_order(self,
                                edge_1,
                                edge_2,
                                crossing_position):
        """
        Get the order of the overlapping nodes in the two edges. First is under, second is over.

        Use rotated node positions since rotation and project may change the overlap order.

        :param edge_1: Edge 1
        :param edge_2: Edge 2
        :param crossing_position: The point of intersection between the projections of edge 1 and edge 2

        :return: overlap_order: The order of the overlapping nodes in edge 1 and edge 2
        """

        overlap_order = []

        node_1, node_2 = edge_1
        node_3, node_4 = edge_2

        node_1_index = self.nodes.index(node_1)
        node_2_index = self.nodes.index(node_2)
        node_3_index = self.nodes.index(node_3)
        node_4_index = self.nodes.index(node_4)

        node_1_position = self.rotated_node_positions[node_1_index]
        node_2_position = self.rotated_node_positions[node_2_index]
        node_3_position = self.rotated_node_positions[node_3_index]
        node_4_position = self.rotated_node_positions[node_4_index]

        x_crossing, z_crossing = crossing_position

        y_crossing_1 = self.calculate_intermediate_y_position(node_1_position, node_2_position, x_crossing, z_crossing)
        y_crossing_2 = self.calculate_intermediate_y_position(node_3_position, node_4_position, x_crossing, z_crossing)

        # todo Only check if crossing is in bounds!
        if y_crossing_1 == y_crossing_2:
            raise RuntimeError('The edges are planar and therefore the interconnects they represent physically '
                               'intersect. This is not a valid spatial graph. Edges: {}, {}.'.format(edge_1, edge_2))

        elif y_crossing_1 > y_crossing_2:
            overlap_order.append(edge_2)
            overlap_order.append(edge_1)

        elif y_crossing_1 < y_crossing_2:
            overlap_order.append(edge_1)
            overlap_order.append(edge_2)

        else:
            raise NotImplementedError('There should be no else case.')

        # Convert list to tuple for hashing later on...
        overlap_order = tuple(overlap_order)

        return overlap_order

    def get_crossings(self):

        crossing_num = 0
        crossings = []
        crossing_edge_pairs = []
        crossing_positions = []

        nonadjacent_edge_pairs = [edge_pair for edge_pair in self.edge_pairs if
                                  edge_pair not in self.adjacent_edge_pairs]

        for line_1, line_2 in nonadjacent_edge_pairs:

            a = self.projected_node_positions[self.nodes.index(line_1[0])]
            b = self.projected_node_positions[self.nodes.index(line_1[1])]
            c = self.projected_node_positions[self.nodes.index(line_2[0])]
            d = self.projected_node_positions[self.nodes.index(line_2[1])]

            min_dist, crossing_position = self.get_line_segment_intersection(a, b, c, d)

            if crossing_position is np.inf:
                raise ValueError('The edges are overlapping. This is not a valid spatial graph.')

            elif crossing_position is None:
                pass

            elif type(crossing_position) is np.ndarray and np.isclose(min_dist, 0):
                crossings.append('crossing_' + str(crossing_num))
                crossing_num += 1
                crossing_positions.append(crossing_position)
                crossing_edge_pair = self.get_crossing_edge_order(line_1, line_2, crossing_position)
                crossing_edge_pairs.append(crossing_edge_pair)


        return crossings, crossing_positions, crossing_edge_pairs

    def project(self, max_iter=100):
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

        rotations = []
        num_crossings = []

        for _ in range(max_iter):

            try:

                # First, check that no edges are perfectly vertical or perfectly horizontal.
                # While neither of these cases technically incorrect, it's easier to implement looping through rotations
                # rather than add edge cases for each 2D and 3D line equation.

                for edge in self.edges:
                    x1, z1 = self.projected_node_positions[self.nodes.index(edge[0])]
                    x2, z2 = self.projected_node_positions[self.nodes.index(edge[1])]

                    if x1 == x2 or z1 == z2:
                        raise ValueError('An edge is vertical or horizontal. This is not a valid spatial graph.')

                # Second, check adjacent edge pairs for validity.
                # Since adjacent segments are straight lines, they should only intersect at a single endpoint.
                # The only other possibility is for them to infinitely overlap, which is not a valid spatial graph.

                for line_1, line_2 in self.adjacent_edge_pairs:
                    a = self.projected_node_positions[self.nodes.index(line_1[0])]
                    b = self.projected_node_positions[self.nodes.index(line_1[1])]
                    c = self.projected_node_positions[self.nodes.index(line_2[0])]
                    d = self.projected_node_positions[self.nodes.index(line_2[1])]
                    min_dist, crossing_position = self.get_line_segment_intersection(a, b, c, d)

                    if crossing_position is not None and crossing_position is not np.inf:
                        assertion_1 = all(np.isclose(crossing_position, a))
                        assertion_2 = all(np.isclose(crossing_position, b))
                        assertion_3 = all(np.isclose(crossing_position, c))
                        assertion_4 = all(np.isclose(crossing_position, d))
                        if not any([assertion_1, assertion_2, assertion_3, assertion_4]):
                            raise ValueError('Adjacent edges must intersect at the endpoints.')

                    elif crossing_position is np.inf:
                        raise ValueError('The edges are overlapping. This is not a valid spatial graph.')


                # Third, Check nonadjacent edge pairs for validity.
                # Since nonadjacent segments are straight lines, they should only intersect at zero or one points.
                # Since adjacent segments should only overlap at endpoints, nonadjacent segments should only overlap
                # between endpoints.
                # The only other possibility is for them to infinitely overlap, which is not a valid spatial graph.

                self.crossings, self.crossing_positions, self.crossing_edge_pairs = self.get_crossings()

                rotations.append(self.rotation)
                num_crossings.append(len(self.crossings))

            except ValueError:
                self.rotation = self.random_rotation()
                self.rotated_node_positions = self.rotate(self.node_positions, self.rotation)

            # If there is no error in the projection rotate anyways
            self.rotation = self.random_rotation()
            self.rotated_node_positions = self.rotate(self.node_positions, self.rotation)



        if len(rotations) == 0:
            raise Exception('Could not find a valid rotation after {} iterations'.format(max_iter))
        else:
            min_crossings = min(num_crossings)
            min_crossings_index = num_crossings.index(min_crossings)
            self.rotation = rotations[min_crossings_index]
            self.rotated_node_positions = self.rotate(self.node_positions, self.rotation)
            self.crossings, self.crossing_positions, self.crossing_edge_pairs = self.get_crossings()


    def create_vertices(self):
        """
        Create the vertices of the spatial graph.
        """

        vertices = [Vertex(self.node_degree(node), 'node_' + node) for node in self.nodes]

        return vertices

    def create_crossings(self):
        """
        Create the crossings of the spatial graph.
        """

        if self.crossing_positions is not None:
            crossings = [Crossing('crossing_object_' + str(i)) for i in range(len(self.crossing_positions))]
        else:
            crossings = []

        return crossings

    def create_spatial_graph_diagram(self):
        """
        Create a diagram of the spatial graph.
        """

        nodes_and_crossings = self.nodes + self.crossings

        # Create the vertex and crossing objects
        vertices = self.create_vertices()
        crossings = self.create_crossings()
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

        inputs = vertices + crossings

        sgd = SpatialGraphDiagram(inputs)

        return sgd

    def plot(self):
        """
        Plot the spatial graph and spatial graph diagram.
        """

        fig = plt.figure()
        # ax2 = plt.subplot()

        ax1 = plt.subplot(221, projection='3d')
        ax2 = plt.subplot(222)
        # ax3 = plt.subplot(223, projection='3d')
        #
        # # Axis 1
        #
        # # ax1.set_xlim(-1.5, 2)
        # # ax1.set_ylim(-1.5, 2)
        # # ax1.set_zlim(-1.5, 2)
        #
        # ax1.title.set_text('Spatial Graph')
        # ax1.xaxis.label.set_text('x')
        # ax1.yaxis.label.set_text('y')
        # ax1.zaxis.label.set_text('z')
        #
        # ax1.set_yticklabels([])
        # ax1.set_xticklabels([])
        #
        # # Axis 2
        #
        # ax2.title.set_text('Spatial Graph Diagram 1 \n (XZ Plane Projection)')
        # ax2.xaxis.label.set_text('x')
        # ax2.yaxis.label.set_text('z')
        #
        # ax2.set_yticklabels([])
        # ax2.set_xticklabels([])
        #
        # # ax2.set_xlim(-0.5, 1.5)
        # # ax2.set_ylim(-0.5, 1.5)
        #
        # # Axis 3
        #
        # # ax3.set_xlim(-1.25, 2)
        # # ax3.set_ylim(-1.25, 2)
        # # ax3.set_zlim(-1.25, 2)
        #
        # ax3.title.set_text('Spatial Graph Rotated')
        # ax3.xaxis.label.set_text('x')
        # ax3.yaxis.label.set_text('y')
        # ax3.zaxis.label.set_text('z')
        #
        # # Figure layout
        # # plt.tight_layout(pad=2, w_pad=7, h_pad=0)
        #
        # Plot 3D
        for edge in self.edges:
            point_1 = self.node_positions[self.nodes.index(edge[0])]
            point_2 = self.node_positions[self.nodes.index(edge[1])]
            ax1.plot3D([point_1[0], point_2[0]], [point_1[1], point_2[1]], [point_1[2], point_2[2]])
        #
        # # Shrink current axis by 40%
        # box = ax1.get_position()
        # ax1.set_position([box.x0, box.y0, box.width * 0.75, box.height])
        #
        # # Put a legend to the right of the current axis
        # # ax1.legend(self.edges, loc='center left', bbox_to_anchor=(1.5, 0.5))
        #
        # # Plot 3D
        # for edge in self.edges:
        #     point_1 = self.rotated_node_positions[self.nodes.index(edge[0])]
        #     point_2 = self.rotated_node_positions[self.nodes.index(edge[1])]
        #     ax3.plot3D([point_1[0], point_2[0]], [point_1[1], point_2[1]], [point_1[2], point_2[2]])
        # # ax3.legend(self.edges)
        #
        # # Shrink current axis by 40%
        # box = ax3.get_position()
        # ax3.set_position([box.x0, box.y0, box.width * 0.75, box.height])

        # Put a legend to the right of the current axis
        # ax3.legend(self.edges, loc='center left', bbox_to_anchor=(1.5, 0.5))
        # ax3.legend(self.edges)

        # Plot 2D
        for edge in self.edges:
            point_1 = self.projected_node_positions[self.nodes.index(edge[0])]
            point_2 = self.projected_node_positions[self.nodes.index(edge[1])]
            ax2.plot([point_1[0], point_2[0]], [point_1[1], point_2[1]])
        # ax2.legend(self.edges)

        # Shrink current axis by 40%
        box = ax2.get_position()
        # ax2.set_position([box.x0, box.y0, box.width * 0.6, box.height])

        # Put a legend to the right of the current axis
        # ax2.legend(self.edges, loc='center left', bbox_to_anchor=(1, -0.25))
        # ax2.legend(self.edges, loc='center left', bbox_to_anchor=(0.75, 0.5), fontsize=9)
        # ax2.legend(self.edges)


        # Plot crossing positions
        if self.crossing_positions is not None:
            for crossing_position in self.crossing_positions:
                ax2.scatter(crossing_position[0], crossing_position[1],
                            marker='o', s=500, facecolors='none', edgecolors='r', linewidths=2)

        plt.show()
