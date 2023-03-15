import numpy as np
from yamada.projection import SpatialGraph
from yamada.calculation import Vertex, Edge, Crossing, SpatialGraphDiagram, h_poly, reverse_poly, normalize_yamada_polynomial
import networkx as nx
from cypari import pari

# TODO Create GitHub workflow to run notebook conversion script before each commit (?)

np.random.seed(0)




# Double-Crossing Single Edge Example
# TODO Check more than one cross per edge (i.e., 2 and 3) works
#
# nodes = ['a', 'b', 'c', 'd', 'e']
# node_positions = np.array([[0,0,0], [1,0,1], [-1,0,1], [-2,0,2], [0,1,3]])
# edges = [('a', 'b'), ('a', 'c'), ('a', 'e'), ('c', 'd'), ('c', 'b'), ('d', 'b'), ('e','b')]
#
# sg = SpatialGraph(nodes=nodes,
#                   node_positions=node_positions,
#                   edges=edges)
#
# sg.project()
# sg.plot()
#
# sgd = sg.create_spatial_graph_diagram()
#
# print("Yamada Polynomial:", sgd.normalized_yamada_polynomial())


# def test_unknot_single_twist():

# a = pari('A')

# for i in range(6):
#
#     np.random.seed(0)

# sg = SpatialGraph(nodes=['a', 'b', 'c', 'd'],
#                   node_positions=np.array([[0, 0.5, 0], [1, 0.5, 1], [1, 0, 0], [0, 0, 1]]),
#                   edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a')])
# sg.project()
# sg.plot()
# sgd = sg.create_spatial_graph_diagram()

# sep = sg.get_sub_edges()
# print(sep)
#
# print(sg.get_vertices_and_crossings_of_edge(('a', 'b')))


# assert sgd.normalized_yamada_polynomial() == normalize_yamada_polynomial(-a ** 2 - a - 1)



sg = SpatialGraph(nodes=['a', 'b', 'c'],
                  node_positions=np.array([[0, 0.5, 0], [-1, 0.5, 1], [1, 0, 0]]),
                  edges=[('a', 'b'), ('b', 'c'), ('c', 'a')])

sg.project()
sgd = sg.create_spatial_graph_diagram()