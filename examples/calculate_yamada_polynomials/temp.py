import numpy as np
from yamada.projection import SpatialGraph
from yamada.calculation import Vertex, Edge, Crossing, SpatialGraphDiagram, h_poly, reverse_poly, normalize_yamada_polynomial
import networkx as nx
from cypari import pari

np.random.seed(0)

# Quadrivalent Example
# TODO Debug code for quadrivalent example

# nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
# node_positions = np.array([[0, 0, 0], [1, 0, 0], [0.5, 1, 0], [0.5, 0.5, 0], [0.25,0.75,0], [0.75,0.75,0], [0,1,0], [1,1,0]])
# edges = [('a', 'b'), ('a', 'g'), ('a', 'd'), ('b', 'd'), ('b', 'h'), ('d', 'e'), ('d', 'f'), ('e', 'c'), ('f', 'c'), ('g', 'c'), ('h', 'c')]
#
# sg1 = SpatialGraph(nodes=nodes,
#                    node_positions=node_positions,
#                    edges=edges)
# sg1.project()
# sg1.plot()
# sgd1 = sg1.create_spatial_graph_diagram()
# print("Yamada Polynomial:", sgd1.yamada_polynomial())


# Double-Crossing Single Edge Example
# TODO Check more than one cross per edge (i.e., 2 and 3) works
#
# nodes = ['a', 'b', 'c', 'd', 'e']
# node_positions = np.array([[0,0,0], [1,0,1], [-1,0,1], [-2,0,2], [0,1,3]])
# edges = [('a', 'b'), ('a', 'c'), ('a', 'e'), ('c', 'd'), ('c', 'b'), ('d', 'b'), ('e','b')]
#
# sg1 = SpatialGraph(nodes=nodes,
#                    node_positions=node_positions,
#                    edges=edges)
#
# sg1.project()
# sg1.plot()
#
# sgd1 = sg1.create_spatial_graph_diagram()
#
# print("Yamada Polynomial:", sgd1.normalized_yamada_polynomial())


A = pari('A')

a, b, c, d = [Vertex(3, L) for L in 'abcd']
X, Y, Z = [Crossing(L) for L in 'XYZ']
a[0], a[1], a[2] = d[0], b[2], X[2]
b[0], b[1] = c[0], X[3]
c[1], c[2] = d[2], Z[0]
d[1] = Z[1]
X[0], X[1] = Y[3], Y[2]
Y[0], Y[1] = Z[3], Z[2]
D = SpatialGraphDiagram([a, b, c, d, X, Y, Z])
G = D.underlying_graph()

expected = A ** -5 + A ** -4 + A ** -3 + A ** -2 + A ** -1 - 1 + A - 2 * A ** 2 + A ** 3 - A ** 4 + A ** 5 + A ** 6 + A ** 8

yp = D.yamada_polynomial()

nyp = D.normalized_yamada_polynomial()