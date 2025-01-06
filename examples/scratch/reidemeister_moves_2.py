import numpy as np
import networkx as nx
import json
from yamada import SpatialGraph
from yamada.sgd.Reidemeister import *

# set the random seed for reproducibility
np.random.seed(0)


# Read the graphs from the JSON file
input_file = 'output_data.json'

with open(input_file, 'r') as f:
    graph_data = json.load(f)

graphs = list(graph_data.values())

# Truncate list if wanting to evaluate a small subset of the graphs
# [0:1] has an R2
graphs = graphs[0:1]

# Initialize lists to store outputs
sgs = []
sgds = []
yps = []

max_crossings = 3

for i, graph in enumerate(graphs):

    # try:

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

    sg = SpatialGraph(nodes=nodes, edges=edges, node_positions=node_xyz)
    sg.plot()

    sgd = sg.create_spatial_graph_diagram()

    print(f"{len(sgd.crossings)} crossings")
    # t_1 = time.time_ns()
    sgd, r1_count, r2_count, r3_count = reidemeister_simplify(sgd, n_tries=10)
    # t_2 = time.time_ns()
    # print(f"Time: {(t_2 - t_1) / 1e9:.9f} seconds")


    print(f"R1: {r1_count}, R2: {r2_count}, R3: {r3_count}, Remaining Crossings: {len(sgd.crossings)}")
    yp = sgd.normalized_yamada_polynomial()
    print(yp)

    # Only calculate the Yamada polynomial for graphs with up to max # crossings
    # if len(sgd.crossings) > max_crossings:
    #     yp = f'skip: {len(sgd.crossings)} crossings'
    #     print(yp)
    # else:
    #     yp = sgd.normalized_yamada_polynomial()
    #     print(yp)

    sgs.append(sg)
    sgds.append(sgd)
    yps.append(yp)

    # except:
    #     # If there is an error create the spatial graph or calculating the Yamada polynomial, skip for now
    #     # Further work will need to investigate what is raising errors.
    #     print('Error. There was an issue with the graph. Skipping.')
    #     continue


