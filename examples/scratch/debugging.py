from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing
from yamada import SpatialGraph
from yamada import has_r1, apply_r1


e1 = Edge('e1')
e2 = Edge('e2')
e3 = Edge('e3')
v1 = Vertex(2, 'v1')
v2 = Vertex(2, 'v2')
v3 = Vertex(2, 'v3')
v1[0] = e3[1]
v1[1] = e1[0]
e1[1] = v2[0]
v2[1] = e2[0]
e2[1] = v3[0]
v3[1] = e3[0]
sgd = SpatialGraphDiagram(edges=[e1, e2, e3], vertices=[v1, v2, v3])

print(sgd.edges)
print(sgd.vertices)
print(sgd.yamada_polynomial())

edge_1 = sgd.edges[1]
edge_2 = sgd.edges[2]
sgd._merge_edges(edge_1, edge_2)

print(sgd.edges)
print(sgd.vertices)
print(sgd.yamada_polynomial())



