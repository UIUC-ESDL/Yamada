import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from shapely.plotting import plot_line, plot_points


# Plot 3D points

a3 = np.array([[0, 0.1, 0], [1, 0.1, 1]])
b3 = np.array([[1, 0.1, 1], [1, 0, 0]])
c3 = np.array([[1, 0, 0], [0, 0, 1]])
d3 = np.array([[0, 0, 1], [0, 0.1, 0]])


fig = plt.figure()
ax = plt.axes(projection='3d')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)

ax.title.set_text('3D points')
ax.xaxis.label.set_text('x')
ax.yaxis.label.set_text('y')
ax.zaxis.label.set_text('z')

ax.plot3D(a3[:, 0], a3[:, 1], a3[:, 2], 'blue')
ax.plot3D(b3[:, 0], b3[:, 1], b3[:, 2], 'blue')
ax.plot3D(c3[:, 0], c3[:, 1], c3[:, 2], 'blue')
ax.plot3D(d3[:, 0], d3[:, 1], d3[:, 2], 'blue')

plt.show()

# Project 3D points to 2D on the XZ plane


fig = plt.figure()
ax = fig.add_subplot()

a2 = LineString([(a3[0][0], a3[0][2]), (a3[1][0], a3[1][2])])
b2 = LineString([(b3[0][0], b3[0][2]), (b3[1][0], b3[1][2])])
c2 = LineString([(c3[0][0], c3[0][2]), (c3[1][0], c3[1][2])])
d2 = LineString([(d3[0][0], d3[0][2]), (d3[1][0], d3[1][2])])




print(a2.intersects(c2))

i1 = a2.intersection(c2)



plot_line(a2, ax=ax)
plot_line(b2, ax=ax)
plot_line(c2, ax=ax)
plot_line(d2, ax=ax)

plot_points(i1, ax=ax, color='red')

plt.show()
