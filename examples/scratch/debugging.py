from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing
from yamada import SpatialGraph

# e1 = Edge(1)
# c1 = Crossing("c1")
#
# e1[0] = c1[2]
# e1[1] = c1[1]
# c1[0] = c1[3]
#
# sgd = SpatialGraphDiagram(edges=[e1], crossings=[c1])

# c1 = Crossing("c1")
# c1[1] = c1[2]
# c1[3] = c1[0]
# sgd = SpatialGraphDiagram(crossings=[c1])

# e1, e2 = Edge(1), Edge(2)
# v1, v2 = Vertex(2, 'v1'), Vertex(2, 'v2')
# e1[0], e1[1] = v1[0], v2[0]
# e2[0], e2[1] = v1[1], v2[1]
# sgd = SpatialGraphDiagram(edges=[e1, e2], vertices=[v1, v2])
# sgd.underlying_planar_embedding()

# e1, e2 = Edge(1), Edge(2)
# c1 = Crossing("c1")
# c1[0] = e2[1]
# c1[1] = e2[0]
# c1[2] = e1[0]
# c1[3] = e1[1]
# # c1[0] = e1[0]
# # c1[1] = e1[1]
# # c1[2] = e2[0]
# # c1[3] = e2[1]
# sgd = SpatialGraphDiagram(edges=[e1, e2], crossings=[c1])
# # sgd.underlying_planar_embedding()

e1, e2, e3, e4 = Edge(1), Edge(2), Edge(3), Edge(4)
v1, v2 = Vertex(2, 'v1'), Vertex(2, 'v2')
c1 = Crossing('c1')
e1[0] = c1[2]
e1[1] = v1[0]
v1[1] = e3[0]
e3[1] = c1[3]
e2[0] = c1[1]
e2[1] = v2[0]
v2[1] = e4[0]
e4[1] = c1[0]
sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4], vertices=[v1, v2], crossings=[c1])


sgd.plot()

# x1 = Crossing('X')
#
# x1[0], x1[2] = x1[1], x1[3]
#
# sgd = SpatialGraphDiagram(crossings=[x1])


# sg1 = SpatialGraph(nodes=['a', 'b', 'c', 'd', 'e', 'f'],
#                    node_positions={'a': [0, 0.5, 0],
#                                    'b': [1, 0, 1],
#                                    'c': [2, 0.5, 0],
#                                    'd': [3, 0, 1],
#                                    'e': [1, 1, 0],
#                                    'f': [-1, 0, 1]},
#                    edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'f'), ('f', 'a')])
#
# sgd1 = sg1.create_spatial_graph_diagram()
# sgd1.yamada_polynomial()