from cypari import pari
from yamada import Edge, Crossing, Vertex, SpatialGraphDiagram
from yamada.sgd.sgd_analysis import available_crossing_swaps
from yamada.sgd.sgd_modification import apply_crossing_swap
from yamada.sgd.topological_distance import compute_min_distance

e1 = Edge(1)
e2 = Edge(2)
e3 = Edge(3)
e4 = Edge(4)
e5 = Edge(5)
e6 = Edge(6)

v1 = Vertex(3, 'v1')
v2 = Vertex(3, 'v2')
v3 = Vertex(3, 'v3')

v1[0] = e1[0]
v1[1] = e2[0]
v1[2] = e3[0]

v2[0] = e1[1]
v2[1] = e3[1]
v2[2] = e2[1]

v3[0] = e2[2]
v3[1] = e1[2]
v3[2] = e4[0]

sgd1 = SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6], vertices=[v1, v2, v3])
sgd2 = sgd1.copy()

compute_min_distance(sgd1, sgd2)