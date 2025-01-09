from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing

e1 = Edge(1)
c1 = Crossing("c1")

e1[0] = c1[2]
e1[1] = c1[1]
c1[0] = c1[3]

sgd = SpatialGraphDiagram([e1, c1])