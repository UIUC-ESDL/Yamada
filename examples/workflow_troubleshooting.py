import numpy as np
import networkx as nx
import json
import matplotlib
import matplotlib.pyplot as plt
from yamada import SpatialGraph

# Replaces PyCharm SciView plotting
# matplotlib.use('TkAgg')
print('Starting')

# Read the graphs from the JSON file
input_file = 'output_data.json'

with open(input_file, 'r') as f:
    graphs = json.load(f)

graph1 = list(graphs.values())[0]


edges, nodes, node_positions = graph1

indices = []
sgs = []
sgds = []
yps = []

# for i, (edges, nodes, node_positions) in data.items():

# Reformat edges
edges = [(a, b) for a, b in edges]

# Reformat positions as a dict
pos = {node: np.array(position) for node, position in zip(nodes, node_positions)}

g = nx.Graph()
g.add_nodes_from(nodes)
g.add_edges_from(edges)

# Plot the networkx graph in 3d
node_xyz = np.array([pos[v] for v in g])
# node_xyz = np.array([pos[v] for v in sorted(g)])
edge_xyz = np.array([(pos[u], pos[v]) for u, v in g.edges()])

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

ax.scatter(*node_xyz.T, s=100, ec="w")
ax.scatter(*node_xyz[[1,2]].T, s=200, c="red")
ax.scatter(*node_xyz[[91,39]].T, s=200, c="green")

for vizedge in edge_xyz:
    ax.plot(*vizedge.T, color="tab:gray")

plt.show()

sg = SpatialGraph(nodes=nodes, edges=edges, node_positions=node_xyz)
sg.plot()

sgd = sg.create_spatial_graph_diagram()
yp = sgd.normalized_yamada_polynomial()




print('Done')
