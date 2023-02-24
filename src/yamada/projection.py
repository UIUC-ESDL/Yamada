import numpy as np
from numpy import sin, cos

import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def get_line_intersection(a, b, c, d):
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

    def get_line_equation(a, b):
        m = (b[1] - a[1]) / (b[0] - a[0])
        b = a[1] - m * a[0]
        return m, b

    m1, b1 = get_line_equation(a, b)
    m2, b2 = get_line_equation(c, d)

    # If slope is the same, then the lines are parallel. Check if overlapping or not.
    if m1 == m2 and b1 == b2:
        raise ValueError('Lines are overlapping, try another random projection surface')

    # If the slope is the same but the offsets are different, then the lines are parallel but not overlapping
    elif m1 == m2 and b1 != b2:
        collision_point = None

    # If the slopes are different, then the lines will intersect (although it may occur out of the segment bounds)
    else:
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1

        # If x or y is not between the two points, then the intersection is outside the line segment
        if (x == a[0] and y == a[1]) or (x == b[0] and y == b[1]) or (x == c[0] and y == c[1]) or (x == d[0] and y == d[1]):
            raise ValueError('Lines are overlapping at vertices, try another random projection surface')
        elif (x < a[0] and x < b[0]) or (x > a[0] and x > b[0]) or (y < a[1] and y < b[1]) or (y > a[1] and y > b[1]):
            collision_point = None
        else:
            collision_point = (x, y)

    return collision_point

# TODO Write Boolean collision check function
# TODO Wrtie funcction to project 2D points...

# Initialize the graph

def generate_spatial_transformation_graph():

    fig = plt.figure()

    ax1 = fig.add_subplot(221, projection='3d')
    ax2 = fig.add_subplot(222, projection='3d')
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)


    # Axis 1

    ax1.set_xlim(-0.5, 1.5)
    ax1.set_ylim(-0.5, 1.5)
    ax1.set_zlim(-0.5, 1.5)

    ax1.title.set_text('Spatial Graph')
    ax1.xaxis.label.set_text('x')
    ax1.yaxis.label.set_text('y')
    ax1.zaxis.label.set_text('z')


    # Axis 2

    ax2.set_xlim(-0.5, 1.5)
    ax2.set_ylim(-0.5, 1.5)
    ax2.set_zlim(-0.5, 1.5)

    ax2.title.set_text('Spatial Graph \n (Random 3D Rotation)')
    ax2.xaxis.label.set_text('x')
    ax2.yaxis.label.set_text('y')
    ax2.zaxis.label.set_text('z')

    # Axis 3

    ax3.title.set_text('Spatial Graph Diagram 1 \n (XZ Plane Projection)')
    ax3.xaxis.label.set_text('x')
    ax3.yaxis.label.set_text('z')

    ax3.set_xlim(-0.5, 1.5)
    ax3.set_ylim(-0.5, 1.5)

    # Axis 4

    ax4.title.set_text('Spatial Graph Diagram 2 \n (Random 3D Rotation)')
    ax4.xaxis.label.set_text('x')
    ax4.yaxis.label.set_text('z')

    ax4.set_xlim(-0.5, 1.5)
    ax4.set_ylim(-0.5, 1.5)

    # Figure layout
    plt.tight_layout(pad=2, w_pad=2, h_pad=4.0)

    return ax1, ax2, ax3, ax4


ax1, ax2, ax3, ax4 = generate_spatial_transformation_graph()


# Create graph

class SpatialTopology:

    def __init__(self, nodes, node_positions, edges, ax1, ax2, ax3, ax4):
        self.nodes = nodes
        self.node_positions = node_positions
        self.edges = edges

        # Initialize the rotation generator

        def rotation_generator():
            rotation = np.zeros(3)
            while True:
                yield rotation
                rotation = np.random.rand(3) * 2 * np.pi

        self.rotation_generator_object = rotation_generator()

        # Positions for the 2D projections / rotation


    @property
    def rotation(self):
        return next(self.rotation_generator_object)




    def rotate(self):
        """
        Rotates a set of points about the first 3D point in the array.

        :param positions:
        :param rotation: Angle in radians
        :return: new_positions:
        """

        # Shift the object to origin
        reference_position = self.node_positions[0]
        origin_positions = self.node_positions - reference_position

        alpha, beta, gamma = self.random_rotation

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

        return new_positions

    def project_to_2d(self, positions):
        # Project to 2D, index the x and z coordinates
        return positions[:, [0, 2]]


    def project_to_2ds(self):

        valid_rotation = False
        iter = 0
        max_iter = 100

        while not valid_rotation and iter < max_iter:

            positions = self.rotate()

            # Project to 2D, index the x and z coordinates
            projection_positions = positions[:, [0, 2]]

        if iter == max_iter:
            raise Exception('Could not find a valid rotation after {} iterations'.format(max_iter))

        return projection_positions


    def plot(self):

        # Plot 3D
        for edge in self.edges:
            point_1 = self.node_positions[self.nodes.index(edge[0])]
            point_2 = self.node_positions[self.nodes.index(edge[1])]
            ax1.plot3D([point_1[0], point_2[0]], [point_1[1], point_2[1]], [point_1[2], point_2[2]], 'blue')


sp1 = SpatialTopology(nodes=['a', 'b', 'c', 'd'],
                      node_positions=np.array([[0, 0.5, 0], [1, 0.5, 1], [1, 0, 0], [0, 0, 1]]),
                      edges=[['a', 'b'], ['b', 'c'], ['c', 'd'], ['d', 'a']],
                      ax1=ax1, ax2=ax2, ax3=ax3, ax4=ax4)

sp1.plot()

# Plot 3D points

#
# a3 = np.array([[0, 0.5, 0], [1, 0.5, 1]])
# b3 = np.array([[1, 0.5, 1], [1, 0, 0]])
# c3 = np.array([[1, 0, 0], [0, 0, 1]])
# d3 = np.array([[0, 0, 1], [0, 0.5, 0]])

# ax1.plot3D(a3[:, 0], a3[:, 1], a3[:, 2], 'blue')
# ax1.plot3D(b3[:, 0], b3[:, 1], b3[:, 2], 'blue')
# ax1.plot3D(c3[:, 0], c3[:, 1], c3[:, 2], 'blue')
# ax1.plot3D(d3[:, 0], d3[:, 1], d3[:, 2], 'blue')


# Plot the 2D projection

# a2 = LineString([(a3[0][0], a3[0][2]), (a3[1][0], a3[1][2])])
# b2 = LineString([(b3[0][0], b3[0][2]), (b3[1][0], b3[1][2])])
# c2 = LineString([(c3[0][0], c3[0][2]), (c3[1][0], c3[1][2])])
# d2 = LineString([(d3[0][0], d3[0][2]), (d3[1][0], d3[1][2])])
#
# i1 = a2.intersection(c2)
#
# ax3.plot([a3[0][0], a3[1][0]], [a3[0][2], a3[1][2]], 'blue')
# ax3.plot([b3[0][0], b3[1][0]], [b3[0][2], b3[1][2]], 'blue')
# ax3.plot([c3[0][0], c3[1][0]], [c3[0][2], c3[1][2]], 'blue')
# ax3.plot([d3[0][0], d3[1][0]], [d3[0][2], d3[1][2]], 'blue')
#
#
# # plot_line(a2, ax=ax3)
# # plot_line(b2, ax=ax3)
# # plot_line(c2, ax=ax3)
# # plot_line(d2, ax=ax3)
#
# plot_points(i1, ax=ax3,
#             marker='o',
#             markersize=40,
#             markerfacecolor='none',
#             markeredgecolor='red',
#             markeredgewidth=4)
#
#
#
# # Apply a random 3D transformation
#
# positions = np.concatenate((a3, b3, c3, d3), axis=0)
#
# np.random.seed(1)
# angles = np.random.rand(3) * 2 * np.pi
#
# new_positions = rotate_about_point(positions, angles)
#
# a3 = new_positions[0:2]
# b3 = new_positions[2:4]
# c3 = new_positions[4:6]
# d3 = new_positions[6:8]
#
# ax2.plot3D(a3[:, 0], a3[:, 1], a3[:, 2], 'blue')
# ax2.plot3D(b3[:, 0], b3[:, 1], b3[:, 2], 'blue')
# ax2.plot3D(c3[:, 0], c3[:, 1], c3[:, 2], 'blue')
# ax2.plot3D(d3[:, 0], d3[:, 1], d3[:, 2], 'blue')
#
# a2 = LineString([(a3[0][0], a3[0][2]), (a3[1][0], a3[1][2])])
# b2 = LineString([(b3[0][0], b3[0][2]), (b3[1][0], b3[1][2])])
# c2 = LineString([(c3[0][0], c3[0][2]), (c3[1][0], c3[1][2])])
# d2 = LineString([(d3[0][0], d3[0][2]), (d3[1][0], d3[1][2])])
#
# i1 = a2.intersection(c2)
#
# plot_line(a2, ax=ax4)
# plot_line(b2, ax=ax4)
# plot_line(c2, ax=ax4)
# plot_line(d2, ax=ax4)
#
# plot_points(i1, ax=ax4,
#             marker='o',
#             markersize=40,
#             markerfacecolor='none',
#             markeredgecolor='red',
#             markeredgewidth=4)

def mygen():

    # Initialize the counter
    i = 0

    while True:
        yield i
        i += 1


plt.show()
