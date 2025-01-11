from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing
from yamada import SpatialGraph
from yamada import has_r1, apply_r1


# e1 = Edge(1)
# e1[0] = e1[1]
# sgd = SpatialGraphDiagram(edges=[e1])

v1 = Vertex(2, label='v1')
v1[0] = v1[1]
sgd = SpatialGraphDiagram(vertices=[v1])


# e1, e2 = Edge(1), Edge(2)
# c1 = Crossing("c1")
# e1[0], e1[1] = c1[3], c1[0]
# e2[0], e2[1] = c1[2], c1[1]
# sgd = SpatialGraphDiagram(edges=[e1, e2], crossings=[c1])
#
# sgd.plot(highlight_nodes=['c1'], highlight_labels={'c1': 'R1'})
#
#
# sgd = apply_r1(sgd, 'c1')
#
# sgd.plot()