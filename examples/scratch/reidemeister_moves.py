import networkx as nx
from cypari import pari
from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing

a = pari('A')


# R1: Infinity symbol

# x1 = Crossing('X')
# x1[1], x1[3] = x1[2], x1[0]
#
# e0, e1 = Edge(0), Edge(1)
#
# e0[0], e0[1] = x1[0], x1[3]
# e1[0], e1[1] = x1[2], x1[1]
#
# sgd = SpatialGraphDiagram([x1, e0, e1])
#
# print('Before R1:', sgd.normalized_yamada_polynomial())
#
# print('Has R1?', sgd.has_r1())
#
# sgd.r1()
#
# print('After R1:', sgd.normalized_yamada_polynomial())
#
# print('Has R1?', sgd.has_r1())


# R2

x1 = Crossing('x1')
x2 = Crossing('x2')

x1[0] = x2[2]
x1[1] = x2[1]
x1[2] = x1[3]
x2[0] = x2[3]

sgd = SpatialGraphDiagram([x1, x2])

print('Before R2:', sgd.normalized_yamada_polynomial())
# print('vertices:', sgd.vertices)
# print('edges:', sgd.edges)
# print('crossings:', sgd.crossings)

print('Has R2?', sgd.has_r2())
sgd.r2()
print('After R2:', sgd.normalized_yamada_polynomial())

print('Has R2?', sgd.has_r2())
# print('vertices:', sgd.vertices)
# print('edges:', sgd.edges)
# print('crossings:', sgd.crossings)

