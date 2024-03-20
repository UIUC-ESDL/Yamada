import numpy as np
import networkx as nx
import json
from yamada import SpatialGraph
from yamada.spatial_graph_diagrams.Reidemeister import *

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

    try:

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
        sg.plot_pyvista()

        sgd = sg.create_spatial_graph_diagram()
        # sgd, r1_count, r2_count, r3_count = reidemeister_simplify(sgd, n_tries=10)

        # Only calculate the Yamada polynomial for graphs with up to max # crossings
        if len(sgd.crossings) > max_crossings:
            yp = f'skip: {len(sgd.crossings)} crossings'
            print(yp)
        else:
            yp = sgd.normalized_yamada_polynomial()
            print(yp)

        sgs.append(sg)
        sgds.append(sgd)
        yps.append(yp)

    except:
        # If there is an error create the spatial graph or calculating the Yamada polynomial, skip for now
        # Further work will need to investigate what is raising errors.
        print('Error')
        continue


