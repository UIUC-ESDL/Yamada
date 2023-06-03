import json
import os

import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial import Voronoi
from scipy.spatial.distance import cdist

from yamada import SpatialGraph, generate_isomorphism, extract_graph_from_json_file

# %% Define the JSON file location

# Obtain the local path of this example's directory
directory = os.path.dirname(__file__) + '/'

# User Input: Set the path to the json file you want to evaluate

# Example 1
# filepath = directory + "G6/C1/G6C1I0.json"

# Example 2
# filepath = directory + "G10/C4/G10C4I7.json"

# Example 3
filepath = directory + "G14/C3/G14C3I11.json"

# %% Extract the spatial graph from the json file

nodes, node_positions, edges = extract_graph_from_json_file(filepath)




pos = {node: np.array(position) for node, position in zip(nodes, node_positions)}

g = nx.Graph()
g.add_nodes_from(nodes)
g.add_edges_from(edges)



node_xyz = np.array([pos[v] for v in sorted(g)])
edge_xyz = np.array([(pos[u], pos[v]) for u, v in g.edges()])


fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Plot the nodes - alpha is scaled by "depth" automatically
ax.scatter(*node_xyz.T, s=100, ec="w")

for vizedge in edge_xyz:
    ax.plot(*vizedge.T, color="tab:gray")

plt.show()



# g, pos = generate_isomorphism(g, pos, n=2, rotate=False)



# node_xyz = np.array([pos[v] for v in sorted(g)])
# edge_xyz = np.array([(pos[u], pos[v]) for u, v in g.edges()])


# fig = plt.figure()
# ax = fig.add_subplot(111, projection="3d")

# ax.scatter(*node_xyz.T, s=100, ec="w")

# for vizedge in edge_xyz:
#     ax.plot(*vizedge.T, color="tab:gray")

# plt.show()




