import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from yamada import Edge, Crossing, Vertex, SpatialGraphDiagram
from yamada.visualization import position_spatial_graph_in_3d, plot_spatial_graph


matplotlib.use('TkAgg')


def create_unknot():

    e1, e2 = Edge(1), Edge(2)
    v1, v2 = Vertex(2, "v1"), Vertex(2, "v2")

    e1[0] = v1[0]
    e1[1] = v2[0]
    e2[0] = v1[1]
    e2[1] = v2[1]

    sgd = SpatialGraphDiagram([e1, e2, v1, v2])

    return sgd

def create_knot():

    e1, e2, e3, e4, e5, e6 = Edge(1), Edge(2), Edge(3), Edge(4), Edge(5), Edge(6)
    x1, x2, x3 = Crossing("x1"), Crossing("x2"), Crossing("x3")

    x1[0] = e2[1]
    x1[1] = e1[0]
    x1[2] = e4[0]
    x1[3] = e3[1]

    # Before crossing swap
    x2[0] = e6[0]
    x2[1] = e2[0]
    x2[2] = e3[0]
    x2[3] = e5[0]

    x3[0] = e5[1]
    x3[1] = e4[1]
    x3[2] = e1[1]
    x3[3] = e6[1]

    sgd = SpatialGraphDiagram([e1, e2, e3, e4, e5, e6, x1, x2, x3])

    return sgd


sgd_unknot = create_unknot()
sgd_knot = create_knot()


g = sgd_knot.underlying_planar_embedding()

nx.draw(g, with_labels=True)
plt.show()
