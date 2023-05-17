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






# def plot_nodes_with_colors(node_positions, ref_points_with_colors):
#     # Convert node positions and reference points to numpy arrays
#     node_xyz = np.array(node_positions)
#     ref_xyz = np.array([p[0] for p in ref_points_with_colors])
#     ref_colors = [p[1] for p in ref_points_with_colors]

#     # Compute the distances between each node and each reference point
#     distances = np.sqrt(((node_xyz[:, np.newaxis, :] - ref_xyz) ** 2).sum(axis=2))

#     # Find the index of the nearest reference point for each node
#     nearest_ref_indices = np.argmin(distances, axis=1)

#     # Plot the nodes with colors based on their nearest reference point
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection="3d")
#     for i, ref_color in enumerate(ref_colors):
#         mask = nearest_ref_indices == i
#         ax.scatter(*node_xyz[mask].T, s=100, ec="w", c=ref_color)
#     for ref_point, ref_color in zip(ref_xyz, ref_colors):
#         ax.scatter(*ref_point.T, s=100, ec="w", c=ref_color)
#     plt.show()


# ref_points_with_colors = [([-1, -1, -1], "r"), ([1, 1, 1], "y"), ([1, -1, 1], "b")]
# plot_nodes_with_colors(node_xyz, ref_points_with_colors)


def k_nearest_neighbors(graph, positions, k=3):
    nodes = sorted(graph.nodes())
    node_xyz = np.array([positions[v] for v in nodes])
    dist_matrix = cdist(node_xyz, node_xyz)
    nearest_neighbors = {}
    for i, node in enumerate(nodes):
        distances = dist_matrix[i]
        neighbors = np.argsort(distances)[1:k+1]
        nearest_neighbors[node] = [nodes[n] for n in neighbors]
    return nearest_neighbors


my_neighbors = k_nearest_neighbors(g, pos)

print(my_neighbors)