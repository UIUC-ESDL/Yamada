import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from yamada import SpatialGraph
from yamada.enumeration import enumerate_yamada_classes
from yamada.visualization import position_spatial_graph_in_3D, position_spatial_graphs_in_3D


# Define a System Architecture
G = nx.MultiGraph([(1, 2), (1,5),(1,6),(2,3),(2,3), (3,4), (4,5),(4,6),(5,6)])

plantri_directory="./plantri53/"
number_of_crossings = 2
ust_dict, number_of_graphs_examined = enumerate_yamada_classes(plantri_directory, G, number_of_crossings)

# Grab the first diagram
g1 = list(ust_dict.values())[0]

# Plot the diagram
# node_labels, node_positions, edges = position_spatial_graph_in_3D(g1)
#
# sg1 = SpatialGraph(node_labels, node_positions, edges)
#
# sg1.plot()
#
# sgd1 = sg1.create_spatial_graph_diagram()
# yp1 = sgd1.normalized_yamada_polynomial()
#
# print(list(ust_dict.keys())[0])
# print(yp1)

sg_inputs = position_spatial_graphs_in_3D(ust_dict)

for sg_input in sg_inputs:
    sg = SpatialGraph(*sg_input)
    sg.plot()
    sgd = sg.create_spatial_graph_diagram()
    yp = sgd.normalized_yamada_polynomial()
    print(yp)