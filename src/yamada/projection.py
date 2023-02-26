import numpy as np
from numpy import sin, cos
import matplotlib.pyplot as plt
from itertools import combinations
from sympy import symbols, solve, Eq

from calculation import (Vertex, Edge, Crossing, SpatialGraphDiagram)

class InputValidation:
    pass

class SpatialGraph:
    """
    A class to represent a spatial graph.

    TODO Create a SpatialGraphDiagram subclass
    TODO Check that no two intersecting edges are planar
    """

    def __init__(self, nodes, node_positions, edges):
        self.nodes = nodes
        self.node_positions = node_positions
        self.edges = edges

        self.rotation_generator_object = self.rotation_generator()
        self.rotation = None
        self.rotated_node_positions = None
        self.projected_node_positions = None
        self.collision_points = None
        self.colliding_edges = None

    @property
    def edge_pairs(self):
        return list(combinations(self.edges, 2))

    @property
    def adjacent_edge_pairs(self):

        adjacent_edge_pairs = []

        for edge_1, edge_2 in self.edge_pairs:
            if edge_1[0] == edge_2[0] or edge_1[0] == edge_2[1] or edge_1[1] == edge_2[0] or edge_1[1] == edge_2[1]:
                adjacent_edge_pairs += [(edge_1, edge_2)]

        return adjacent_edge_pairs

    @property
    def nonadjacent_edge_pairs(self):
        return [edge_pair for edge_pair in self.edge_pairs if edge_pair not in self.adjacent_edge_pairs]

    @property
    def edge_pairs_with_crossings(self):
        return self.colliding_edges

    @property
    def edge_pairs_without_crossings(self):
        return [edge_pair for edge_pair in self.edge_pairs if edge_pair not in self.edge_pairs_with_crossings]

    def node_degree(self, node):
        return len([edge for edge in self.edges if node in edge])

    @staticmethod
    def rotation_generator():
        """
        A generator to generate random rotations for projecting a spatial graph onto a 2D plane.
        """
        rotation = np.zeros(3)
        while True:
            yield rotation
            rotation = np.random.rand(3) * 2 * np.pi

    def randomize_rotation(self):
        self.rotation = next(self.rotation_generator_object)

    def rotate(self):
        """
        Rotates a set of points about the first 3D point in the array.

        :return: new_positions:
        """

        # Shift the object to origin
        reference_position = self.node_positions[0]
        origin_positions = self.node_positions - reference_position

        alpha, beta, gamma = self.rotation

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

        self.rotated_node_positions = new_positions

    def project_node_positions(self):
        self.projected_node_positions = self.rotated_node_positions[:, [0, 2]]

    @staticmethod
    def get_y_position(a,b,x_int,z_int):
        """
        Get the ... position of line given and intermediate x and y values

        Example: (change)
            a = (0,0,0)
            b = (1,1,1)
            x_int = 0.5
            z_int = 0.5

        """

        x1, y1, z1 = a
        x2, y2, z2 = b

        l = x2 - x1
        m = y2 - y1
        n = z2 - z1

        # Check for vertical line



        # (x-x1)/l = (y-y1)/m = (z-z1)/n
        # EQ1: y = (m/l)(x-x1) + y1
        # EQ2: y = (m/n)(z-z1) + y1

        y = symbols('y')

        eq1 = Eq(m/l*(x_int-x1)+y1-y)
        eq2 = Eq(m/n*(z_int-z1)+y1-y)

        res = solve((eq1, eq2), y)

        # Convert from sympy float to normal float
        y_int = float(res[y])

        return y_int

    def get_edge_overlap_order(self, edge_1, edge_2):
        """
        Get the order of the overlapping nodes in the two edges.

        Use rotated node positions since rotation and project may change the overlap order.

        :param edge_1: Edge 1
        :param edge_2: Edge 2
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

        # TODO Implement checker better

        # Check if edge_1 and edge_2 are planar
        # ...





        return overlap_order

    def get_line_intersection(self, a, b, c, d):
        """
        Get the intersection point of two lines.

        Each line is defined by two points (a, b) and (c, d).
        Each point is represented by a tuple (x, y) or (x, y).

        Important logic:
        1. If the slopes are the same, then the lines are parallel. Check if they overlap. If they do not overlap, then
        there is no crossing. If the lines overlap, then there is an infinite number of crossings. Raise an error.
        2. If the intersection occurs exactly at points a, b, c, or d, then raise an error. Rather than apply complex logic
        to determine which edge case the intersection is, just raise an error and try again with a different random projection.
        3. ...

        :param a: Point A of line 1
        :param b: Point B of line 1
        :param c: Point A of line 2
        :param d: Point B of line 2
        """

        def get_line_equation(p1, p2):
            """
            Get the line equation in the form y = mx + b
            p1 = (x1, y1)
            p2 = (x2, y2)
            m = (y2 - y1) / (x2 - x1)
            y = mx + b --> b = y - mx

            If x2-x1=0, then m = Undefined
            """

            if p2[0]-p1[0] == 0:
                slope = np.NaN
                intercept = np.NaN
            else:
                slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
                intercept = p1[1] - slope * p1[0]

            return slope, intercept

        m1, b1 = get_line_equation(a, b)
        m2, b2 = get_line_equation(c, d)


        # If both lines are vertical and overlapping
        if m1 == np.NaN and m2 == np.NaN and a[0] == c[0]:
            collision_point = np.inf

        # If both lines are vertical but not overlapping
        elif m1 == np.NaN and m2 == np.NaN and a[0] != c[0]:
            collision_point = None

        # If slope and intercept are the same then the lines are overlapping
        elif m1 == m2 and b1 == b2:
            collision_point = None

        # If the slopes are the same but the intercepts are different, then the lines are parallel but not overlapping
        elif m1 == m2 and b1 != b2:
            collision_point = None

        # If the slopes are different, then the lines will intersect (although it may occur out of the segment bounds)
        else:

            # Find the intersection point
            if m1 is np.NaN or m2 is np.NaN:
                if m1 is np.NaN:
                    x = c[0]
                    y = m2 * x + b2
                elif m2 is np.NaN:
                    x = a[0]
                    y = m1 * x + b1
            else:
                # m1 * x + b1 = m2 * x + b2 --> x = (b2 - b1) / (m1 - m2)
                x = (b2 - b1) / (m1 - m2)
                y = m1 * x + b1

            collision_point = np.array([x, y])

        return collision_point

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
        # TODO Capture names of what crosses what...

        valid_projection = False
        iter = 0
        max_iter = 100

        while not valid_projection and iter < max_iter:

            print('LOOPING')

            self.randomize_rotation()
            self.rotate()
            self.project_node_positions()

            vertical_or_horizontal = False
            # Make sure no edge is vertical or horizontal:
            for edge in self.edges:
                x1, z1 = self.projected_node_positions[self.nodes.index(edge[0])]
                x2, z2 = self.projected_node_positions[self.nodes.index(edge[1])]

                if x1 == x2 or z1 == z2:
                    valid_projection = False
                    vertical_or_horizontal = True
                    break

            # Check that adjacent segments aren't overlapping
            # Since adjacent segments are straight lines, the can only intersect at the endpoints or overlap
            # Use better logic than vertical or horizontal. The problem is that the break above
            # wouldn't skip this, and then the valid_projection=True would overwrite the valid_projection=False
            if vertical_or_horizontal == False:

                for line_1, line_2 in self.adjacent_edge_pairs:
                    a = self.projected_node_positions[self.nodes.index(line_1[0])]
                    b = self.projected_node_positions[self.nodes.index(line_1[1])]
                    c = self.projected_node_positions[self.nodes.index(line_2[0])]
                    d = self.projected_node_positions[self.nodes.index(line_2[1])]

                    collision_point = self.get_line_intersection(a, b, c, d)

                    if collision_point is None:
                        valid_projection = True

                    elif collision_point is np.inf:
                        valid_projection = False
                        break

                    else:
                        x, y = collision_point

                        if (x == a[0] and y == a[1]) or (x == b[0] and y == b[1]) or (x == c[0] and y == c[1]) or (
                                x == d[0] and y == d[1]):
                            pass


                # Check nonadjacent segments

                colliding_edges = [] # Ordered under, over
                collision_points = []
                for line_1, line_2 in self.nonadjacent_edge_pairs:
                    a = self.projected_node_positions[self.nodes.index(line_1[0])]
                    b = self.projected_node_positions[self.nodes.index(line_1[1])]
                    c = self.projected_node_positions[self.nodes.index(line_2[0])]
                    d = self.projected_node_positions[self.nodes.index(line_2[1])]

                    collision_point = self.get_line_intersection(a, b, c, d)

                    if collision_point is None:
                        valid_projection = True

                    elif collision_point is np.inf:
                        valid_projection = False
                        break

                    else:
                        x, y = collision_point

                        # If x or y is not between the two points, then the intersection is outside the line segment
                        if (x == a[0] and y == a[1]) or (x == b[0] and y == b[1]) or (x == c[0] and y == c[1]) or (
                                x == d[0] and y == d[1]):
                            pass

                        elif (x < a[0] and x < b[0]) or (x > a[0] and x > b[0]) or (y < a[1] and y < b[1]) or (
                                y > a[1] and y > b[1]):
                            valid_projection = True
                            # collision_point = None

                        else:
                            valid_projection = True
                            collision_point = (x, y)
                            # TODO Check which edge is on top
                            collision_points.append(collision_point)
                            colliding_edges.append((line_1, line_2))

                        if valid_projection is False:
                            break

                self.collision_points = collision_points
                self.colliding_edges = colliding_edges


        if iter == max_iter:
            raise Exception('Could not find a valid rotation after {} iterations'.format(max_iter))


    def create_spatial_graph_diagram(self):

        vertices = [Vertex(self.node_degree(node), 'node_'+node) for node in self.nodes]
        crossings = [Crossing('crossing_'+str(i)) for i in range(len(self.collision_points))]

        # First, connect adjacent edges. Since they are adjacent they cannot have crossings.
        for edge_1, edge_2 in self.adjacent_edge_pairs:

            # Figure out which 2 of the 4 nodes are connected together
            # The nodes must come from opposing edges
            if edge_1[0] == edge_2[0]:
                node_1 = edge_1[0]
                node_2 = edge_2[0]
            elif edge_1[0] == edge_2[1]:
                node_1 = edge_1[0]
                node_2 = edge_2[1]
            elif edge_1[1] == edge_2[0]:
                node_1 = edge_1[1]
                node_2 = edge_2[0]
            elif edge_1[1] == edge_2[1]:
                node_1 = edge_1[1]
                node_2 = edge_2[1]
            else:
                raise Exception('Edges are not adjacent')


            # Get the first available indices for each node
            node_1_index = self.nodes.index(node_1)
            node_2_index = self.nodes.index(node_2)

            node_1_next_available_index = vertices[node_1_index].next_available_index()
            node_2_next_available_index = vertices[node_2_index].next_available_index()

            vertices[node_1_index][node_1_next_available_index] = vertices[node_2_index][node_2_next_available_index]

        for edge_1, edge_2, crossing in zip(self.edge_pairs_with_crossings, crossings):

            # Figure out which 2 of the 4 nodes are connected together
            # The nodes must come from opposing edges
            if edge_1[0] == edge_2[0]:
                node_1 = edge_1[0]
                node_2 = edge_2[0]
            elif edge_1[0] == edge_2[1]:
                node_1 = edge_1[0]
                node_2 = edge_2[1]
            elif edge_1[1] == edge_2[0]:
                node_1 = edge_1[1]
                node_2 = edge_2[0]
            elif edge_1[1] == edge_2[1]:
                node_1 = edge_1[1]
                node_2 = edge_2[1]
            else:
                raise Exception('Edges are not adjacent')

            # TODO Figure out how to obtian order... do at crossing findign time

            # Get the first available indices for each node
            node_1_index = self.nodes.index(node_1)
            node_2_index = self.nodes.index(node_2)

            node_1_next_available_index = vertices[node_1_index].next_available_index()
            node_2_next_available_index = vertices[node_2_index].next_available_index()

            vertices[node_1_index][node_1_next_available_index] = vertices[node_2_index][
                node_2_next_available_index]

        return vertices, crossings



    def plot(self):

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
        plt.tight_layout(pad=2, w_pad=5, h_pad=0)

        # Plot 3D
        for edge in self.edges:
            point_1 = self.node_positions[self.nodes.index(edge[0])]
            point_2 = self.node_positions[self.nodes.index(edge[1])]
            ax1.plot3D([point_1[0], point_2[0]], [point_1[1], point_2[1]], [point_1[2], point_2[2]])
        ax1.legend(self.edges)

        # Plot 3D
        for edge in self.edges:
            point_1 = self.rotated_node_positions[self.nodes.index(edge[0])]
            point_2 = self.rotated_node_positions[self.nodes.index(edge[1])]
            ax3.plot3D([point_1[0], point_2[0]], [point_1[1], point_2[1]], [point_1[2], point_2[2]])
        ax3.legend(self.edges)


        # Plot 2D
        for edge in self.edges:
            point_1 = self.projected_node_positions[self.nodes.index(edge[0])]
            point_2 = self.projected_node_positions[self.nodes.index(edge[1])]
            ax2.plot([point_1[0], point_2[0]], [point_1[1], point_2[1]])
        ax2.legend(self.edges)


        # Plot collision points
        for collision_point in self.collision_points:
            ax2.scatter(collision_point[0], collision_point[1],
                        marker='o', s=500, facecolors='none', edgecolors='r', linewidths=2)

        plt.show()

        return None


# Set random seed for consistency
np.random.seed(1)

sp1 = SpatialGraph(nodes=['a', 'b', 'c', 'd'],
                   node_positions=np.array([[0, 0.5, 0], [1, 0.5, 1], [1, 0, 0], [0, 0, 1]]),
                   edges=[['a', 'b'], ['b', 'c'], ['c', 'd'], ['d', 'a']])


sp1.project()

sp1.plot()


# sp1.edge_pairs_with_crossings

# a = Vertex(2, 'a')

# sp1.create_spatial_graph_diagram()

# sp1.get_y_position([0,0,0],[0,0,1],0,0.5)


# Alternative method of calculating the Yamada Polynomial of an Infinity Symbol
# a, b, c, d = [Vertex(2, L) for L in 'abcd']
# x = Crossing('x')
#
# a[0] = x[2]
# b[0] = x[0]
# b[1] = c[0]
# c[1] = x[3]
# d[0] = x[1]
# d[1] = a[1]
#
# D = SpatialGraphDiagram([a,b,c,d,x])
#
# yamada_polynomial_infinity_symbol = D.yamada_polynomial()
#
# print("Infinity Symbol Yamada Polynomial:", yamada_polynomial_infinity_symbol)






