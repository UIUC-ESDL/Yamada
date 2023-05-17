"""EXAMPLE

Extract spatial graphs from jsons and calculate their Yamada polynomials.

"""
# %% Import Statements

import os
import numpy as np
from yamada import extract_graph_from_json_file, SpatialGraph, generate_isomorphism
import networkx as nx
import matplotlib.pyplot as plt

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


# %% Create a SpatialGraph object and calculate the Yamada polynomial

# Instantiate the SpatialGraph object
sg = SpatialGraph(nodes=nodes,
                  node_positions=node_positions,
                  edges=edges)

# Plot the Spatial Graph in 3D and the projected 2D plane to see what's going on. Crossings will be circled in red.
# Note: Crossings occur when two edges that do not intersect, but appear to when they are projected onto a 2D plane.
# sg.plot()

# Create the spatial graph diagram (necessary for calculating the Yamada polynomial)
sgd = sg.create_spatial_graph_diagram()

# Calculate the Yamada polynomial
yamada_polynomial = sgd.normalized_yamada_polynomial()
print("Yamada Polynomial: ", yamada_polynomial)


pos = {node: np.array(position) for node, position in zip(nodes, node_positions)}

g = nx.Graph()
g.add_nodes_from(nodes)
g.add_edges_from(edges)

# k = 20 * (1 / np.sqrt(len(nodes)))
#
# pos = nx.spring_layout(g, dim=3, pos=pos, k=k)
#
# node_positions_new = np.array([pos[v] for v in nodes])
#
#
# # Instantiate the SpatialGraph object
# sg = SpatialGraph(nodes=nodes,
#                   node_positions=node_positions_new,
#                   edges=edges)
#
# # Plot the Spatial Graph in 3D and the projected 2D plane to see what's going on. Crossings will be circled in red.
# # Note: Crossings occur when two edges that do not intersect, but appear to when they are projected onto a 2D plane.
# sg.plot()
#
# # Create the spatial graph diagram (necessary for calculating the Yamada polynomial)
# sgd = sg.create_spatial_graph_diagram()
#
# # Calculate the Yamada polynomial
# yamada_polynomial = sgd.normalized_yamada_polynomial()
# print("Yamada Polynomial: ", yamada_polynomial)


node_xyz = np.array([pos[v] for v in sorted(g)])
edge_xyz = np.array([(pos[u], pos[v]) for u, v in g.edges()])


fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Plot the nodes - alpha is scaled by "depth" automatically
ax.scatter(*node_xyz.T, s=100, ec="w")

for vizedge in edge_xyz:
    ax.plot(*vizedge.T, color="tab:gray")

plt.show()



g, pos = generate_isomorphism(g, pos, n=9, rotate=False)



node_xyz = np.array([pos[v] for v in sorted(g)])
edge_xyz = np.array([(pos[u], pos[v]) for u, v in g.edges()])


fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

ax.scatter(*node_xyz.T, s=100, ec="w")

for vizedge in edge_xyz:
    ax.plot(*vizedge.T, color="tab:gray")

plt.show()


sg = SpatialGraph(nodes=sorted(list(g.nodes)), edges=list(g.edges), node_positions=node_xyz)
sgd = sg.create_spatial_graph_diagram()
yp = sgd.normalized_yamada_polynomial()
print("Yamada polynomial:  {}".format(yp))




