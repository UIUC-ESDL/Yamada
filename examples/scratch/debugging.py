from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing
from yamada import SpatialGraph

# e1 = Edge(1)
# c1 = Crossing("c1")
#
# e1[0] = c1[2]
# e1[1] = c1[1]
# c1[0] = c1[3]
#
# sgd = SpatialGraphDiagram([e1, c1])





sg1 = SpatialGraph(nodes=['a', 'b', 'c', 'd', 'e', 'f'],
                   node_positions={'a': [0, 0.5, 0],
                                   'b': [1, 0, 1],
                                   'c': [2, 0.5, 0],
                                   'd': [3, 0, 1],
                                   'e': [1, 1, 0],
                                   'f': [-1, 0, 1]},
                   edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'f'), ('f', 'a')])

sgd1 = sg1.create_spatial_graph_diagram()
sgd1.yamada_polynomial()