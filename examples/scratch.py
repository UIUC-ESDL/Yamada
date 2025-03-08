from time import time_ns
import matplotlib
matplotlib.use('TkAgg')
from yamada.sgd.diagram_elements import Edge, Vertex, Crossing
from yamada.sgd.spatial_graph_diagrams import SpatialGraphDiagram
from yamada.sgd.topological_distance import compute_min_distance, compute_network

import networkx as nx
import matplotlib.pyplot as plt

from yamada import enumerate_yamada_classes
from yamada.sgd.topological_distance import compute_min_distance

# %% Define the System Architecture and Component Geometries

# The system architecture is a NetworkX graph where the nodes represent components and the edges
# represent connections between components. The nodes are labeled with integers starting from 0.

# Currently, components must be either 2- or 3-valent. Please refer to the documentation for
# more information.

# User Input: System architecture
sa = [(0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 0), (2, 5), (3, 5), (4, 5)]
# sa = [
#     (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom face edges
#     (4, 5), (5, 6), (6, 7), (7, 4),  # Top face edges
#     (0, 4), (1, 5), (2, 6), (3, 7)   # Vertical edges connecting top and bottom
# ]


# Create a networkx graph from the system architecture
sa_graph = nx.MultiGraph()
sa_graph.add_edges_from(sa)

# Plot the system architecture
# nx.draw(sa_graph, with_labels=True)
# plt.show()


# %% Enumerate all Unique Spatial Topologies

# User Input
number_of_crossings = 5

unique_spatial_topologies, number_topologies = enumerate_yamada_classes(sa_graph, number_of_crossings)

sgds = list(unique_spatial_topologies.values())


# def create_unknot():
#     e1 = Edge('e1')
#     v1 = Vertex(2, 'v1')
#     e1[0] = v1[0]
#     e1[1] = v1[1]
#     return SpatialGraphDiagram(edges=[e1], vertices=[v1])
#
#
# def create_figure_eight():
#     e1 = Edge('e1')
#     e2 = Edge('e2')
#     e3 = Edge('e3')
#     e4 = Edge('e4')
#     e5 = Edge('e5')
#     e6 = Edge('e6')
#
#     c1 = Crossing('c1')
#     c2 = Crossing('c2')
#     c3 = Crossing('c3')
#
#     c1[0] = e2[1]
#     c1[1] = e1[0]
#     c1[2] = e4[0]
#     c1[3] = e3[1]
#
#     c2[0] = e6[0]
#     c2[1] = e2[0]
#     c2[2] = e3[0]
#     c2[3] = e5[0]
#
#     c3[0] = e5[1]
#     c3[1] = e4[1]
#     c3[2] = e1[1]
#     c3[3] = e6[1]
#
#     return SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6], crossings=[c1, c2, c3])
#
#
# def double_figure_8():
#
#     e1 = Edge('e1')
#     e2 = Edge('e2')
#     e3 = Edge('e3')
#     e4 = Edge('e4')
#     e5 = Edge('e5')
#     e6 = Edge('e6')
#     e7 = Edge('e7')
#     e8 = Edge('e8')
#     e9 = Edge('e9')
#     e10 = Edge('e10')
#     e11 = Edge('e11')
#     e12 = Edge('e12')
#
#     c1 = Crossing("c1")
#     c2 = Crossing("c2")
#     c3 = Crossing("c3")
#     c4 = Crossing("c4")
#     c5 = Crossing("c5")
#     c6 = Crossing("c6")
#
#     # First Figure 8 Knot
#
#     c1[0] = e2[1]
#     c1[1] = e1[0]
#     c1[2] = e4[0]
#     c1[3] = e3[1]
#
#     c2[0] = e6[0]
#     c2[1] = e2[0]
#     c2[2] = e3[0]
#     c2[3] = e5[0]
#
#     c3[0] = e5[1]
#     c3[1] = e4[1]
#     c3[2] = e7[1]
#     c3[3] = e6[1]
#
#     # Second Figure 8 Knot
#
#     c4[0] = e8[1]
#     c4[1] = e7[0]
#     c4[2] = e10[0]
#     c4[3] = e9[1]
#
#     c5[0] = e12[0]
#     c5[1] = e8[0]
#     c5[2] = e9[0]
#     c5[3] = e11[0]
#
#     c6[0] = e11[1]
#     c6[1] = e10[1]
#     c6[2] = e1[1]
#     c6[3] = e12[1]
#
#     sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12], crossings=[c1, c2, c3, c4, c5, c6])
#
#     return sgd
#
# unknot = create_unknot()
# figure_8 = create_figure_eight()
# double_figure_8 = double_figure_8()

# distance, network = compute_min_distance(unknot, figure_8)

# t1 = time_ns()
# distance, network = compute_min_distance(unknot, double_figure_8, max_depth=3)
# t2 = time_ns()
#
# print(f"Time: {(t2 - t1) / 1e6} ms")

# results = compute_network([unknot, figure_8, double_figure_8],max_depth=5)
results = compute_network(sgds,max_depth=2)

import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

# Add nodes with an attribute for min_depth
for poly, data in results.items():
    G.add_node(poly, min_depth=data['min_depth'])

# Add directed edges with weights
for src, data in results.items():
    for tgt, weight in data['neighbors'].items():
        # If the same edge exists from multiple BFS searches, only the minimum weight is kept.
        G.add_edge(src, tgt, weight=weight)

# Use a layout algorithm (e.g., spring_layout) to determine positions for the nodes.
pos = nx.spring_layout(G, k=0.5, iterations=50)

plt.figure(figsize=(12, 8))

# Draw nodes and labels
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
nx.draw_networkx_labels(G, pos, font_size=8)

# Draw edges with arrows and edge labels
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)

plt.title("Network of Unique Spatial Topologies")
plt.axis("off")
plt.show(block=True)