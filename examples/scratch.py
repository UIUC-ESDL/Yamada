"""SCRATCH FILE

This file is used to test code snippets and ideas. It is not intended to be run as a script by other users.

"""

import numpy as np
from yamada.spatial_graphs import SpatialGraph
from yamada.spatial_graph_diagrams import Vertex, Edge, Crossing, SpatialGraphDiagram, h_poly, reverse_poly, normalize_yamada_polynomial
import networkx as nx
from cypari import pari



np.random.seed(0)


sg = SpatialGraph(nodes=['a', 'b', 'c', 'd', 'e'],
                  node_positions=np.array([[0, 0, 1], [1, 0, 1], [1, 0, 2], [0.5, 0.5, 0], [0, 0, 2]]),
                  edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'a')])

sg.project(predefined_rotation=[0, 0, 0])
sg.plot()

sgd = sg.create_spatial_graph_diagram()

yp1 = sgd.normalized_yamada_polynomial()
print('yp1', yp1)

has_r2, edge, crossing_a, crossing_b = sgd.has_r2()
print('has_r2', has_r2, edge, crossing_a, crossing_b)


sgd.remove_crossing_fuse_edges(sgd.crossings[0])
sgd.remove_crossing_fuse_edges(sgd.crossings[0])
# sgd._merge_vertices()
#
# yp2 = sgd.normalized_yamada_polynomial()
# print('yp2', yp2)

# e0 = Edge('0')
# e1 = Edge('1')
# v0 = Vertex(2, 'v0')
# v1 = Vertex(2, 'v1')
# e0[0] = v0[0]
# e1[0] = v0[1]
# e0[1] = v1[0]
# e1[1] = v1[1]
# sgd3 = SpatialGraphDiagram([v0, v1, e0, e1])
#
# print(sgd3.normalized_yamada_polynomial())

# e0 = Edge('0')
# e1 = Edge('1')
# v0 = Vertex(2, 'v0')
# v1 = Vertex(2, 'v1')
# e0[0] = v0[0]
# e1[0] = v0[1]
# e0[1] = v1[0]
# e1[1] = v1[1]
# sgd3 = SpatialGraphDiagram([v0, v1, e0, e1])

# e0[0] = e1[1]
# e0[1] = e1[0]
# sgd3 = SpatialGraphDiagram([e0, e1])

# print(sgd3.normalized_yamada_polynomial())


# v0, v1 = [Vertex(2, f'v{i}') for i in range(2)]
#
# v0[0] = v1[0]
#
# v0[1] = v1[1]
#
# sgd = SpatialGraphDiagram([v0, v1])
#
#
# print(sgd.normalized_yamada_polynomial())
