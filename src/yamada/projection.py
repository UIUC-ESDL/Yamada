"""

TODO Create AbstractGraph Subclass
TODO Create SpatialGraphDiagram Subclass
"""

import numpy as np
from numpy import sin, cos
import matplotlib.pyplot as plt
from itertools import combinations
from sympy import symbols, solve, Eq
from math import acos
from math import sqrt
from math import pi
import numpy.typing as npt

from .calculation import (Vertex, Crossing, SpatialGraphDiagram)


class InputValidation:
    """
    TODO Check that all nodes adjoin at least 2 edges (no braids)
    TODO Check if dangling nodes impact calculator
    """

    def __init__(self,
                 nodes:          list[str],
                 node_positions: np.ndarray,
                 edges:          list[tuple[str, str]]):

        self.nodes          = self._validate_nodes(nodes)
        self.node_positions = self._validate_node_positions(node_positions)
        self.edges          = self._validate_edges(edges)

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

        for node in nodes:
            if not node.isalnum():
                raise ValueError('Nodes must be alphanumeric.')

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
                raise TypeError('Edges must be tuples.')

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

    def _validate_node_positions(self, node_positions: np.ndarray) -> np.ndarray:
        """
        Validates the user's input and returns an array of node positions.

        Checks:
        1. The input is a np.ndarray
        2. The array size matches the number of nodes
        3. Each row contains 3 real numbers
        4. Each row is unique
        """

        if type(node_positions) != np.ndarray:
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


class LinearAlgebra:
    """
    A class that contains static methods for necessary linear algebra calculations.
    """
    def __init__(self):
        self.rotated_node_positions    = None
        self.projected_node_positions  = None
        self.rotation_generator_object = self.rotation_generator()
        self.rotation                  = self.random_rotation()


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
               rotation: np.ndarray) -> np.ndarray:
        """
        Rotates a set of points about the first 3D point in the array.

        :return: new_positions:
        """

        # Shift the object to origin
        reference_position = positions[0]
        origin_positions   = positions - reference_position

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

        r = r_z @ r_y @ r_x

        # Transpose positions from [[x1,y1,z1],[x2... ] to [[x1,x2,x3],[y1,... ]
        rotated_origin_positions = (r @ origin_positions.T).T

        # Shift back from origin
        new_positions = rotated_origin_positions + reference_position

        rotated_node_positions = new_positions

        return rotated_node_positions

    @staticmethod
    def get_line_equation(p1: np.ndarray,
                          p2: np.ndarray) -> tuple[float, float]:
        """
        Get the line equation in the form y = mx + b

        This function assumes lines are not vertical or horizontal since the projection method generates
        random projections until one contains no vertical or horizontal lines.

        p1 = (x1, y1)
        p2 = (x2, y2)
        m = (y2 - y1) / (x2 - x1)
        y = mx + b --> b = y - mx
        """

        slope     = (p2[1] - p1[1]) / (p2[0] - p1[0])
        intercept = p1[1] - slope * p1[0]

        return slope, intercept

    def get_line_segment_intersection(self,
                                      a: np.ndarray,
                                      b: np.ndarray,
                                      c: np.ndarray,
                                      d: np.ndarray) -> np.ndarray:
        """
        Get the intersection point of two line segments, if it exists. Otherwise, return None.

        Each line is defined by two points (a, b) and (c, d).
        Each point is represented by a tuple (x, y) or (x, y).

        Important logic:
        1. If slope and intercept are the same then the lines are overlapping and there are infinite overlapping points
        2. If the slopes are the same but the intercepts are different, then the lines are parallel but not overlapping
        3. If the slopes are different, then the lines will intersect (although it may occur out of the segment bounds)

        :param a: Point A of line 1
        :param b: Point B of line 1
        :param c: Point A of line 2
        :param d: Point B of line 2
        """

        m1, b1 = self.get_line_equation(a, b)
        m2, b2 = self.get_line_equation(c, d)

        if m1 == m2 and b1 == b2:
            crossing_position = np.inf

        elif m1 == m2 and b1 != b2:
            crossing_position = None

        else:
            x = (b2 - b1) / (m1 - m2)
            y = m1 * x + b1

            x_outside_ab = (x < a[0] and x < b[0]) or (x > a[0] and x > b[0])
            y_outside_ab = (y < a[1] and y < b[1]) or (y > a[1] and y > b[1])
            x_outside_cd = (x < c[0] and x < d[0]) or (x > c[0] and x > d[0])
            y_outside_cd = (y < c[1] and y < d[1]) or (y > c[1] and y > d[1])

            crossing_point_outside_ab = x_outside_ab or y_outside_ab
            crossing_point_outside_cd = x_outside_cd or y_outside_cd

            if crossing_point_outside_ab or crossing_point_outside_cd:
                crossing_position = None
            else:
                crossing_position = np.array([x, y])

        return crossing_position

    @staticmethod
    def calculate_intermediate_y_position(a:     np.ndarray,
                                          b:     np.ndarray,
                                          x_int: float,
                                          z_int: float) -> float:
        """
        Calculates the intermediate y position given two points and the intermediate x and z position.

        Assumes that lines are not vertical or horizontal per the projection method input checks.

        Example:
            a = (0,0,0)
            b = (1,1,1)
            x_int = 0.5
            z_int = 0.5
            Therefore y_int = 0.5
        """

        x1, y1, z1 = a
        x2, y2, z2 = b

        l = x2 - x1
        m = y2 - y1
        n = z2 - z1

        # (x-x1)/l = (y-y1)/m = (z-z1)/n
        # EQ1: y = (m/l)(x-x1) + y1
        # EQ2: y = (m/n)(z-z1) + y1

        y = symbols('y')

        # Round to 5 decimal places to avoid sympy errors
        eq1 = Eq(round(m / l * (x_int - x1) + y1,5), y)
        eq2 = Eq(round(m / n * (z_int - z1) + y1,5), y)

        res = solve((eq1, eq2), y)

        # Convert from sympy float to normal float
        y_int = float(res[y])

        return y_int

    def project_node_positions(self):
        """
        Project the node positions onto the x-z plane
        """
        self.projected_node_positions = self.rotated_node_positions[:, [0, 2]]

    def get_projected_node_position(self,
                                    node: str) -> np.ndarray:
        """
        Get the projected node position
        """
        return self.projected_node_positions[self.nodes.index(node)]


    def get_projected_node_positions(self,
                                     nodes: list[str]) -> np.ndarray:
        """
        Get the projected node positions
        """
        projected_node_positions = []

        for node in nodes:
            projected_node_positions.append(self.get_projected_node_position(node))

        return np.array(projected_node_positions)

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
            return sqrt(v[0] ** 2 + v[1] ** 2)

        def dot_product(v, w):
            return v[0] * w[0] + v[1] * w[1]

        def determinant(v, w):
            return v[0] * w[1] - v[1] * w[0]

        def inner_angle(v, w):
            cosx = dot_product(v, w) / (length(v) * length(w))
            rad  = acos(cosx)  # in radians
            return rad * 180 / pi  # returns degrees

        inner = inner_angle(vector_a, vector_b)
        det   = determinant(vector_a, vector_b)
        if det > 0:  # this is a property of the det. If the det < 0 then B is clockwise of A
            return inner
        else:  # if the det > 0 then A is immediately clockwise of B
            return 360 - inner



class SpatialGraph(InputValidation, LinearAlgebra):
    """
    A class to represent a spatial graph.

    Notes:
        1. Component ports must be individually represented as nodes. In other words, a control valve servicing an
        actuator must employ separate nodes for the supply and return ports, along with their associated edges.
    """

    def __init__(self,
                 nodes:          list[str],
                 node_positions: np.ndarray,
                 edges:          list[tuple[str, str]]):

        # Initialize validated inputs
        InputValidation.__init__(self, nodes, node_positions, edges)

        # Initialize attributes necessary for geometric calculations
        LinearAlgebra.__init__(self)

        self.rotated_node_positions = self.rotate(self.node_positions, self.rotation)
        self.project_node_positions()

        # Initialize attributes that are calculated later
        self.crossings = None
        self.crossing_positions = None
        self.crossing_edge_pairs = None

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


    def get_vertices_and_crossings_of_edge(self, edge):
        """
        Returns the vertices and crossings of an edge, ordered from left to right.
        """

        # Get edge nodes
        edge_nodes = [node for node in edge]

        # Get node positions
        edge_node_positions = self.get_projected_node_positions(edge_nodes)

        # Unordered Edge Crossings
        edge_crossings = []


        if self.crossing_edge_pairs is not None:

            for edge_pair, position, crossing in zip(self.crossing_edge_pairs, self.crossing_positions, self.crossings):
                if edge in edge_pair:
                    edge_crossings.append([crossing, position])

            # Order edge crossings from left to right
            # Since we are using straight lines, we can simply compare x-coordinates.
            edge_crossings = [edge_crossing for _, edge_crossing in sorted(zip(self.crossing_positions, edge_crossings), key=lambda pair: pair[0][0])]

        # Prepend the first node
        edge_crossings.insert(0, [edge_nodes[0], edge_node_positions[0]])

        # Add the final node
        edge_crossings.append([edge_nodes[1], edge_node_positions[1]])

        return edge_crossings

    def node_degree(self, node):
        """
        Returns the degree of a node.

        The node degree is the number of edges that are incident to the node.
        """
        return len([edge for edge in self.edges if node in edge])

    def cyclical_edge_order_vertex(self,
                                   reference_node,
                                   node_ordering_dict=None):
        """
        Get the cyclical edge order for a given node.

        The spatial-topological calculations presume that nodes are ordered in a CCW rotation. While it does not matter
        which node is used as index zero, it is important that the node order is consistent.
        """

        if node_ordering_dict is None:
            node_ordering_dict = {}

        reference_node_position = self.get_projected_node_position(reference_node)

        adjacent_nodes = []
        adjacent_node_positions = []

        # Get the adjacent edges
        adjacent_edges = []
        for edge in self.edges:
            if reference_node == edge[0] or reference_node == edge[1]:
                adjacent_edges.append(edge)

        for edge in adjacent_edges:
            nodes_and_crossings = self.get_vertices_and_crossings_of_edge(edge)
            nodes, positions = zip(*nodes_and_crossings)

            positions_list = [tuple(position) for position in positions]

            reference_node_index = positions_list.index(tuple(reference_node_position))

            # If the reference node is the first node in the edge
            if reference_node_index == 0:
                adjacent_node = nodes[reference_node_index + 1]
                adjacent_nodes.append(adjacent_node)
                adjacent_node_positions.append(positions[reference_node_index + 1])

            # If the reference node is the last node in the edge
            elif reference_node_index == len(nodes) - 1:
                adjacent_node = nodes[reference_node_index - 1]
                adjacent_nodes.append(adjacent_node)
                adjacent_node_positions.append(positions[reference_node_index - 1])

            else:
                raise ValueError('Reference node is not the first or last node in the edge.')


        # Shift nodes to the origin
        shifted_adjacent_node_positions = adjacent_node_positions - reference_node_position

        # Horizontal line (reference for angles)
        reference_vector = np.array([1, 0])

        rotations = []

        for shifted_adjacent_node_position in shifted_adjacent_node_positions:
            rotations.append(self.calculate_counter_clockwise_angle(reference_vector, shifted_adjacent_node_position))

        # Sort the nodes in CCW order
        sorted_index = np.argsort(rotations)

        ccw_edge_ordering = {}
        for edge, order in zip(adjacent_nodes, sorted_index):
            ccw_edge_ordering[edge] = order

        node_ordering_dict[reference_node] = ccw_edge_ordering

        return node_ordering_dict


    def cyclical_edge_order_crossing(self,
                                     crossing,
                                     node_ordering_dict=None):
        """
        Get the order of the overlapping nodes in the two edges. First is under, second is over.

        Use rotated node positions since rotation and project may change the overlap order.

        :param crossing: The crossing
        :param node_ordering_dict: A dictionary of node ordering for each node
        :return: overlap_order: The order of the overlapping nodes in edge 1 and edge 2
        """

        if node_ordering_dict is None:
            node_ordering_dict = {}

        # Get the edges that are connected to the crossing
        edge_1, edge_2    = self.crossing_edge_pairs[crossing]
        crossing_position = self.crossing_positions[crossing]

        # Figure out which nodes and crossings directly adjoin the crossing

        # Edge 1: What is to the left and right of this crossing?
        edge_1_nodes_and_crossings = self.get_vertices_and_crossings_of_edge(edge_1)

        edge_1_nodes, edge_1_positions = zip(*edge_1_nodes_and_crossings)

        # Find the index of the numpy array in a list
        edge_1_positions_list = [tuple(position) for position in edge_1_positions]
        edge_1_crossing_index = edge_1_positions_list.index(tuple(crossing_position))

        edge_1_left_node = edge_1_nodes[edge_1_crossing_index - 1]
        edge_1_right_node = edge_1_nodes[edge_1_crossing_index + 1]

        edge_1_left_node_position = edge_1_positions[edge_1_crossing_index - 1]
        edge_1_right_node_position = edge_1_positions[edge_1_crossing_index + 1]

        # Swap the left and right nodes if the left node is to the right of the right node
        if edge_1_left_node_position[0] > edge_1_right_node_position[0]:
            edge_1_left_node, edge_1_right_node = edge_1_right_node, edge_1_left_node
            edge_1_left_node_position, edge_1_right_node_position = edge_1_right_node_position, edge_1_left_node_position

        if edge_1_crossing_index == 0 or edge_1_crossing_index == len(edge_1_positions) - 1:
            raise ValueError("Crossing is at the end of the edge. This is not supported.")

        # Edge 2: What is to the left and right of this crossing?
        edge_2_nodes_and_crossings = self.get_vertices_and_crossings_of_edge(edge_2)

        edge_2_nodes, edge_2_positions = zip(*edge_2_nodes_and_crossings)

        edge_2_positions_list = [tuple(position) for position in edge_2_positions]
        edge_2_crossing_index = edge_2_positions_list.index(tuple(crossing_position))

        edge_2_left_node = edge_2_nodes[edge_2_crossing_index - 1]
        edge_2_right_node = edge_2_nodes[edge_2_crossing_index + 1]


        edge_2_left_node_position = edge_2_positions[edge_2_crossing_index - 1]
        edge_2_right_node_position = edge_2_positions[edge_2_crossing_index + 1]

        # Swap "left" and "right" if indexing went negative
        if edge_2_left_node_position[0] > edge_2_right_node_position[0]:
            edge_2_left_node, edge_2_right_node = edge_2_right_node, edge_2_left_node
            edge_2_left_node_position, edge_2_right_node_position = edge_2_right_node_position, edge_2_left_node_position

        if edge_2_crossing_index == 0 or edge_2_crossing_index == len(edge_2_positions) - 1:
            raise ValueError("Crossing is at the end of the edge. This is not supported.")


        # Figure out which left edge is TL and which is BL
        if edge_1_left_node_position[1] > edge_2_left_node_position[1]:
            top_left_edge = edge_1_left_node
            bottom_left_edge = edge_2_left_node
            top_right_edge = edge_2_right_node
            bottom_right_edge = edge_1_right_node
        elif edge_1_left_node_position[1] < edge_2_left_node_position[1]:
            top_left_edge = edge_2_left_node
            bottom_left_edge = edge_1_left_node
            top_right_edge = edge_1_right_node
            bottom_right_edge = edge_2_right_node
        else:
            raise ValueError("Top left edge cannot be determined.")

        # Now figure out which one is in front
        # Get the 3D positions of the nodes

        top_left_edge_position_3d = self.rotated_node_positions[self.nodes.index(top_left_edge)]
        top_right_edge_position_3d = self.rotated_node_positions[self.nodes.index(top_right_edge)]
        bottom_left_edge_position_3d = self.rotated_node_positions[self.nodes.index(bottom_left_edge)]
        bottom_right_edge_position_3d = self.rotated_node_positions[self.nodes.index(bottom_right_edge)]


        y_crossing_tl_br = self.calculate_intermediate_y_position(top_left_edge_position_3d,
                                                                  bottom_right_edge_position_3d,
                                                                  crossing_position[0],
                                                                  crossing_position[1])

        y_crossing_tr_bl = self.calculate_intermediate_y_position(top_right_edge_position_3d,
                                                                  bottom_left_edge_position_3d,
                                                                  crossing_position[0],
                                                                  crossing_position[1])

        crossing_order_dict = {}

        if y_crossing_tl_br == y_crossing_tr_bl:
            raise RuntimeError('The edges are planar and therefore the interconnects they represent physically '
                             'intersect. This is not a valid spatial graph. Edges: {}, {}.'.format(edge_1, edge_2))

        elif y_crossing_tl_br > y_crossing_tr_bl:
            # Top right edge is under and should be zero, then follow CCW rotation
            crossing_order_dict[top_right_edge] = 0
            crossing_order_dict[top_left_edge] = 1
            crossing_order_dict[bottom_left_edge] = 2
            crossing_order_dict[bottom_right_edge] = 3

        elif y_crossing_tl_br < y_crossing_tr_bl:
            # Top left edge is under and should be zero, then follow CCW rotation
            crossing_order_dict[top_left_edge] = 0
            crossing_order_dict[bottom_left_edge] = 1
            crossing_order_dict[bottom_right_edge] = 2
            crossing_order_dict[top_right_edge] = 3

        else:
            raise NotImplementedError('There should be no else case.')

        node_ordering_dict[crossing] = crossing_order_dict

        return node_ordering_dict

    def get_crossing_edge_pairs(self,
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

    def project(self):
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

        # Initialize while loop exit conditions
        valid_projection = False
        iter             = 0
        max_iter         = 10

        while not valid_projection and iter < max_iter:

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
                    crossing_position = self.get_line_segment_intersection(a, b, c, d)

                    if crossing_position is not None and crossing_position is not np.inf:
                        x, y = crossing_position
                        assertion_1 = np.isclose(x, a[0]) and np.isclose(y, a[1])
                        assertion_2 = np.isclose(x, b[0]) and np.isclose(y, b[1])
                        assertion_3 = np.isclose(x, c[0]) and np.isclose(y, c[1])
                        assertion_4 = np.isclose(x, d[0]) and np.isclose(y, d[1])
                        if not any([assertion_1, assertion_2, assertion_3, assertion_4]):
                            raise ValueError('Adjacent edges must intersect at the endpoints.')

                    elif crossing_position is np.inf:
                        raise ValueError('The edges are overlapping. This is not a valid spatial graph.')


                # Third, Check nonadjacent edge pairs for validity.
                # Since nonadjacent segments are straight lines, they should only intersect at zero or one points.
                # Since adjacent segments should only overlap at endpoints, nonadjacent segments should only overlap
                # between endpoints.
                # The only other possibility is for them to infinitely overlap, which is not a valid spatial graph.

                crossing_num = 0
                crossings = []
                crossing_edge_pairs = []
                crossing_positions     = []

                nonadjacent_edge_pairs = [edge_pair for edge_pair in self.edge_pairs if edge_pair not in self.adjacent_edge_pairs]

                for line_1, line_2 in nonadjacent_edge_pairs:

                    a = self.projected_node_positions[self.nodes.index(line_1[0])]
                    b = self.projected_node_positions[self.nodes.index(line_1[1])]
                    c = self.projected_node_positions[self.nodes.index(line_2[0])]
                    d = self.projected_node_positions[self.nodes.index(line_2[1])]

                    crossing_position = self.get_line_segment_intersection(a, b, c, d)


                    if crossing_position is np.inf:
                        raise ValueError('The edges are overlapping. This is not a valid spatial graph.')

                    elif crossing_position is None:
                        pass

                    elif type(crossing_position) is np.ndarray:
                        crossings.append(crossing_num)
                        crossing_num += 1
                        crossing_positions.append(crossing_position)
                        crossing_edge_pair = self.get_crossing_edge_pairs(line_1, line_2, crossing_position)
                        crossing_edge_pairs.append(crossing_edge_pair)

                    else:
                        raise NotImplementedError('There should be no else case.')


                    self.crossings = crossings
                    self.crossing_positions = crossing_positions
                    self.crossing_edge_pairs = crossing_edge_pairs

                # If we made it this far without raising an exception, then we have a valid projection
                valid_projection = True

            except ValueError:
                self.rotation = self.random_rotation()
                self.rotated_node_positions = self.rotate(self.node_positions, self.rotation)
                self.project_node_positions()
                iter += 1


        if iter == max_iter:
            raise Exception('Could not find a valid rotation after {} iterations'.format(max_iter))


    def create_spatial_graph_diagram(self):
        """
        Create a diagram of the spatial graph.
        """

        # Create the vertex and crossing objects
        vertices = [Vertex(self.node_degree(node), 'node_'+node) for node in self.nodes]

        if self.crossing_positions is not None:
            crossings = [Crossing('crossing_'+str(i)) for i in range(len(self.crossing_positions))]
        else:
            crossings = []

        # Create a dictionary that contains the cyclical ordering of every node
        node_ordering_dict = {}
        for node in self.nodes:
            node_ordering_dict = self.cyclical_edge_order_vertex(node, node_ordering_dict)


        # First, connect adjacent nodes that are not separated by a crossing


        for node in self.nodes:

            adjacent_nodes = list(node_ordering_dict[node].keys())

            for adjacent_node in adjacent_nodes:


                # Only if not int which is crossing
                if type(adjacent_node) is not int:
                    vertex_1_index = self.nodes.index(node)
                    vertex_2_index = self.nodes.index(adjacent_node)

                    vertex_1 = vertices[vertex_1_index]
                    vertex_2 = vertices[vertex_2_index]

                    if not vertex_1.already_assigned(vertex_2):

                        adjacent_index_for_node = node_ordering_dict[node][adjacent_node]
                        node_index_for_adjacent = node_ordering_dict[adjacent_node][node]

                        vertex_1[adjacent_index_for_node] = vertex_2[node_index_for_adjacent]
                else:
                    pass


        # Second, connect nodes to adjoining crossings

        if len(crossings) > 0:

            # Create a dictionary that contains the cyclical ordering of every crossing
            crossing_ordering_dict = {}
            for crossing in self.crossings:
                crossing_ordering_dict = self.cyclical_edge_order_crossing(crossing, crossing_ordering_dict)



            # Assumption, if a crossing adjoins a Vertex, and all other valencies are already assigned... no N/A
            # Since one node can adjoin multiple crossings.

            for crossing in self.crossings:

                adjacent_nodes = list(crossing_ordering_dict[crossing].keys())
                # assign to both strings (vertices) and ints (crossings)

                crossing_1_index = crossing  # Crossing name is the index
                crossing_object = crossings[crossing_1_index]

                for adjacent_node in adjacent_nodes:

                    if type(adjacent_node) == str:
                        vertex_2_index = self.nodes.index(adjacent_node)
                        vertex_2 = vertices[vertex_2_index]

                        if not crossing_object.already_assigned(vertex_2):
                            adjacent_index_for_node = crossing_ordering_dict[crossing][adjacent_node]
                            node_index_for_adjacent = node_ordering_dict[adjacent_node][crossing]
                            crossing_object[adjacent_index_for_node] = vertex_2[node_index_for_adjacent]

                    elif type(adjacent_node) == int:
                        crossing_2 = adjacent_node
                        crossing_2_object = crossings[crossing_2]

                        if not crossing.already_assigned(crossing_2):
                            adjacent_index_for_crossing = crossing_ordering_dict[crossing][crossing_2]
                            crossing_index_for_crossing_2 = node_ordering_dict[crossing_2][crossing]
                            crossing_object[adjacent_index_for_crossing] = crossing_2_object[crossing_index_for_crossing_2]

                    else:
                        raise ValueError('Adjacent node must be a string or an integer.')


        inputs = vertices + crossings

        sgd = SpatialGraphDiagram(inputs)

        return sgd



    def plot(self):
        """
        Plot the spatial graph and spatial graph diagram.
        """

        fig = plt.figure()

        ax1 = plt.subplot(221, projection='3d')
        ax2 = plt.subplot(222)
        ax3 = plt.subplot(223, projection='3d')

        # Axis 1

        ax1.set_xlim(-0.5, 1.5)
        ax1.set_ylim(-0.5, 1.5)
        ax1.set_zlim(-0.5, 1.5)

        ax1.title.set_text('Spatial Graph')
        ax1.xaxis.label.set_text('x')
        ax1.yaxis.label.set_text('y')
        ax1.zaxis.label.set_text('z')

        # Axis 2

        ax2.title.set_text('Spatial Graph Diagram 1 \n (XZ Plane Projection)')
        ax2.xaxis.label.set_text('x')
        ax2.yaxis.label.set_text('z')

        # ax2.set_xlim(-0.5, 1.5)
        # ax2.set_ylim(-0.5, 1.5)

        # Axis 3

        ax3.set_xlim(-0.5, 1.5)
        ax3.set_ylim(-0.5, 1.5)
        ax3.set_zlim(-0.5, 1.5)

        ax3.title.set_text('Spatial Graph Rotated')
        ax3.xaxis.label.set_text('x')
        ax3.yaxis.label.set_text('y')
        ax3.zaxis.label.set_text('z')

        # Figure layout
        plt.tight_layout(pad=2, w_pad=7, h_pad=0)

        # Plot 3D
        for edge in self.edges:
            point_1 = self.node_positions[self.nodes.index(edge[0])]
            point_2 = self.node_positions[self.nodes.index(edge[1])]
            ax1.plot3D([point_1[0], point_2[0]], [point_1[1], point_2[1]], [point_1[2], point_2[2]])

        # Shrink current axis by 40%
        box = ax1.get_position()
        ax1.set_position([box.x0, box.y0, box.width * 0.75, box.height])

        # Put a legend to the right of the current axis
        # ax1.legend(self.edges, loc='center left', bbox_to_anchor=(1.5, 0.5))

        # Plot 3D
        for edge in self.edges:
            point_1 = self.rotated_node_positions[self.nodes.index(edge[0])]
            point_2 = self.rotated_node_positions[self.nodes.index(edge[1])]
            ax3.plot3D([point_1[0], point_2[0]], [point_1[1], point_2[1]], [point_1[2], point_2[2]])
        # ax3.legend(self.edges)

        # Shrink current axis by 40%
        box = ax3.get_position()
        ax3.set_position([box.x0, box.y0, box.width * 0.75, box.height])

        # Put a legend to the right of the current axis
        # ax3.legend(self.edges, loc='center left', bbox_to_anchor=(1.5, 0.5))

        # Plot 2D
        for edge in self.edges:
            point_1 = self.projected_node_positions[self.nodes.index(edge[0])]
            point_2 = self.projected_node_positions[self.nodes.index(edge[1])]
            ax2.plot([point_1[0], point_2[0]], [point_1[1], point_2[1]])
        # ax2.legend(self.edges)

        # Shrink current axis by 40%
        box = ax2.get_position()
        ax2.set_position([box.x0, box.y0, box.width * 0.6, box.height])

        # Put a legend to the right of the current axis
        ax2.legend(self.edges, loc='center left', bbox_to_anchor=(1, 0.5))


        # Plot crossing positions
        if self.crossing_positions is not None:
            for crossing_position in self.crossing_positions:
                ax2.scatter(crossing_position[0], crossing_position[1],
                            marker='o', s=500, facecolors='none', edgecolors='r', linewidths=2)

        plt.show()


