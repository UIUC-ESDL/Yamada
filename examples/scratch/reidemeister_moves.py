import networkx as nx
from cypari import pari
from yamada import has_cut_edge, remove_valence_two_vertices, h_poly, SpatialGraphDiagram, Vertex, Edge, \
    Crossing, reverse_poly, normalize_yamada_polynomial



# R1: Infinity symbol

a = pari('A')


x1 = Crossing('X')
x1[1], x1[3] = x1[2], x1[0]

e0, e1 = Edge(0), Edge(1)

e0[0], e0[1] = x1[0], x1[3]
e1[0], e1[1] = x1[2], x1[1]

sgd = SpatialGraphDiagram([x1, e0, e1])

print(sgd.normalized_yamada_polynomial())

