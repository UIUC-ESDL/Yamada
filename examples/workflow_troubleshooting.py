import numpy as np
import networkx as nx
import json
import matplotlib
import time
import matplotlib.pyplot as plt
from yamada import SpatialGraph

# Replaces PyCharm SciView plotting
# matplotlib.use('TkAgg')
print('Starting')

# Read the graphs from the JSON file
input_file = 'output_data.json'

with open(input_file, 'r') as f:
    graph_data = json.load(f)


graphs = list(graph_data.values())

sgs = []
sgds = []
yps = []
num_graphs = 20

print('Time', time.time())

# TODO Add logic for num of crossings

for i, graph in enumerate(graphs):

    print('Loop', i, 'time', time.time())

    edges, nodes, node_positions = graph

    # Reformat edges
    edges = [(a, b) for a, b in edges]

    # Reformat positions as a dict
    pos = {node: np.array(position) for node, position in zip(nodes, node_positions)}

    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)

    # Plot the networkx graph in 3d
    node_xyz = np.array([pos[v] for v in g])
    # edge_xyz = np.array([(pos[u], pos[v]) for u, v in g.edges()])
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection="3d")
    #
    # ax.scatter(*node_xyz.T, s=100, ec="w")
    # ax.scatter(*node_xyz[[1,2]].T, s=200, c="red")
    # ax.scatter(*node_xyz[[91,39]].T, s=200, c="green")
    #
    # for vizedge in edge_xyz:
    #     ax.plot(*vizedge.T, color="tab:gray")
    #
    # plt.show()

    sg = SpatialGraph(nodes=nodes, edges=edges, node_positions=node_xyz)
    sg.plot()

    sgd = sg.create_spatial_graph_diagram()
    yp = sgd.normalized_yamada_polynomial()

    sgs.append(sg)
    sgds.append(sgd)
    yps.append(yp)

    if i >= num_graphs-1:
        break



print('Done')
