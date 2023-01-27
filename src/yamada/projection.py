import numpy as np
from numpy import sin, cos
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from shapely.plotting import plot_line, plot_points

def rotate_about_point(positions, rotation):
    """
    Rotates a set of points about the first 3D point in the array.

    :param positions:
    :param rotation: Angle in radians
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

    r = r_z @ r_y @ r_x

    # Transpose positions from [[x1,y1,z1],[x2... ] to [[x1,x2,x3],[y1,... ]
    rotated_origin_positions = (r @ origin_positions.T).T

    # Shift back from origin
    new_positions = rotated_origin_positions + reference_position

    return new_positions

# Plot 3D points

a3 = np.array([[0, 0.1, 0], [1, 0.1, 1]])
b3 = np.array([[1, 0.1, 1], [1, 0, 0]])
c3 = np.array([[1, 0, 0], [0, 0, 1]])
d3 = np.array([[0, 0, 1], [0, 0.1, 0]])


# fig = plt.figure()
fig, (ax1, ax2) = plt.subplots()

ax1.set_xlim(-1, 1)
ax1.set_ylim(-1, 1)
ax1.set_zlim(-1, 1)

ax1.title.set_text('3D points')
ax1.xaxis.label.set_text('x')
ax1.yaxis.label.set_text('y')
ax1.zaxis.label.set_text('z')

ax1.plot3D(a3[:, 0], a3[:, 1], a3[:, 2], 'blue')
ax1.plot3D(b3[:, 0], b3[:, 1], b3[:, 2], 'blue')
ax1.plot3D(c3[:, 0], c3[:, 1], c3[:, 2], 'blue')
ax1.plot3D(d3[:, 0], d3[:, 1], d3[:, 2], 'blue')

# plt.show()

# Apply a random 3D transformation

# # fig = plt.figure()
# ax = plt.axes(projection='3d')
#
# ax.set_xlim(-1, 1)
# ax.set_ylim(-1, 1)
# ax.set_zlim(-1, 1)
#
# ax.title.set_text('3D points')
# ax.xaxis.label.set_text('x')
# ax.yaxis.label.set_text('y')
# ax.zaxis.label.set_text('z')
#
# positions = np.concatenate((a3, b3, c3, d3), axis=0)
#
# angles = np.random.rand(3) * 2 * np.pi
#
# new_positions = rotate_about_point(positions, angles)
#
# a3 = new_positions[0:2]
# b3 = new_positions[2:4]
# c3 = new_positions[4:6]
# d3 = new_positions[6:8]
#
# ax.plot3D(a3[:, 0], a3[:, 1], a3[:, 2], 'blue')
# ax.plot3D(b3[:, 0], b3[:, 1], b3[:, 2], 'blue')
# ax.plot3D(c3[:, 0], c3[:, 1], c3[:, 2], 'blue')
# ax.plot3D(d3[:, 0], d3[:, 1], d3[:, 2], 'blue')
#



plt.show()

# # Project 3D points to 2D on the XZ plane
#
# fig = plt.figure()
# ax = fig.add_subplot()
#
# a2 = LineString([(a3[0][0], a3[0][2]), (a3[1][0], a3[1][2])])
# b2 = LineString([(b3[0][0], b3[0][2]), (b3[1][0], b3[1][2])])
# c2 = LineString([(c3[0][0], c3[0][2]), (c3[1][0], c3[1][2])])
# d2 = LineString([(d3[0][0], d3[0][2]), (d3[1][0], d3[1][2])])
#
# def project_3d_to_2d(points_3d):
#     pass
#
#
# def check_for_overlapping_points(*line_strings):
#     # TODO Check function logic
#     for i in range(len(line_strings)):
#         for j in range(i + 1, len(line_strings)):
#             if line_strings[i].intersects(line_strings[j]):
#                 return True
#     return False
#
#
# def check_for_parallel_lines(*line_strings):
#     # TODO Check function logic
#     for i in range(len(line_strings)):
#         for j in range(i + 1, len(line_strings)):
#             if line_strings[i].parallel(line_strings[j]):
#                 return True
#     return False
#
#
# def check_for_intersecting_lines(*line_strings):
#     # TODO Check function logic
#     intersections = []
#     for i in range(len(line_strings)):
#         for j in range(i + 1, len(line_strings)):
#             if line_strings[i].intersects(line_strings[j]):
#                 intersections.append(line_strings[i].intersection(line_strings[j]))
#     return intersections
#
#
#
#
# print(a2.intersects(c2))
#
# i1 = a2.intersection(c2)
#
#
#
# plot_line(a2, ax=ax)
# plot_line(b2, ax=ax)
# plot_line(c2, ax=ax)
# plot_line(d2, ax=ax)
#
# plot_points(i1, ax=ax,
#             marker='o',
#             markersize=40,
#             markerfacecolor='none',
#             markeredgecolor='red',
#             markeredgewidth=4)
#
# plt.show()
