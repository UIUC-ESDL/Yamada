import numpy as np
import networkx as nx
from yamada import SpatialGraph
from yamada.enumeration import enumerate_yamada_classes

# Simple system architecture
sa = [(0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 0), (2, 5), (3, 5), (4, 5)]

# Create a networkx graph from the system architecture
sa_graph = nx.MultiGraph()
sa_graph.add_edges_from(sa)

# Enumerate the Yamada classes
number_of_crossings = 2

unique_spatial_topologies, number_topologies = enumerate_yamada_classes(sa_graph, number_of_crossings)
#