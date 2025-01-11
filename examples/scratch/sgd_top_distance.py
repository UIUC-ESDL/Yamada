from cypari import pari
from yamada import Edge, Crossing, Vertex, SpatialGraphDiagram
from yamada.Anti_Reidemeister import apply_anti_reidemeister_move
from yamada.sgd.topological_distance import compute_min_distance

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

def create_knot_post_crossing_swap():

    e1, e2, e3, e4, e5, e6 = Edge(1), Edge(2), Edge(3), Edge(4), Edge(5), Edge(6)
    x1, x2, x3 = Crossing("x1"), Crossing("x2"), Crossing("x3")

    x1[0] = e2[1]
    x1[1] = e1[0]
    x1[2] = e4[0]
    x1[3] = e3[1]

    # After crossing swap
    x2[0] = e5[0]
    x2[1] = e6[0]
    x2[2] = e2[0]
    x2[3] = e3[0]

    x3[0] = e5[1]
    x3[1] = e4[1]
    x3[2] = e1[1]
    x3[3] = e6[1]

    sgd = SpatialGraphDiagram([e1, e2, e3, e4, e5, e6, x1, x2, x3])

    return sgd

def create_double_knot():

    e1, e2, e3, e4, e5, e6 = Edge(1), Edge(2), Edge(3), Edge(4), Edge(5), Edge(6)
    e7, e8, e9, e10, e11, e12 = Edge(7), Edge(8), Edge(9), Edge(10), Edge(11), Edge(12)
    x1, x2, x3 = Crossing("x1"), Crossing("x2"), Crossing("x3")
    x4, x5, x6 = Crossing("x4"), Crossing("x5"), Crossing("x6")

    x1[0] = e2[1]
    x1[1] = e1[0]
    x1[2] = e4[0]
    x1[3] = e3[1]

    x2[0] = e6[0]
    x2[1] = e2[0]
    x2[2] = e3[0]
    x2[3] = e5[0]

    x3[0] = e5[1]
    x3[1] = e4[1]
    x3[2] = e7[1]  # x3[2] = e1[1]
    x3[3] = e6[1]

    # Knot 2

    x4[0] = e8[1]
    x4[1] = e7[0]
    x4[2] = e10[0]
    x4[3] = e9[1]

    x5[0] = e12[0]
    x5[1] = e8[0]
    x5[2] = e9[0]
    x5[3] = e11[0]

    x6[0] = e11[1]
    x6[1] = e10[1]
    x6[2] = e1[1]
    x6[3] = e12[1]

    sgd = SpatialGraphDiagram([e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, x1, x2, x3, x4, x5, x6])

    return sgd

a = pari('A')
yp_unknot = -a ** 2 - a - 1

sgd_unknot = create_unknot()
sgd_knot = create_knot()
sgd_knot_pcs = create_knot_post_crossing_swap()
sgd_double_knot = create_double_knot()

sgd_double_knot_mod = apply_anti_reidemeister_move(sgd_double_knot, "x2")
sgd_double_knot_mod = apply_anti_reidemeister_move(sgd_double_knot_mod, "x5")
assert sgd_double_knot_mod.yamada_polynomial() == yp_unknot

# Pass
assert compute_min_distance(sgd_knot, sgd_knot_pcs, 2, 10) == 1
assert compute_min_distance(sgd_knot, sgd_unknot, 2, 10) == 1
assert compute_min_distance(sgd_knot_pcs, sgd_unknot, 2, 10) == 0
assert compute_min_distance(sgd_unknot, sgd_unknot, 2, 10) == 0
assert compute_min_distance(sgd_knot, sgd_knot, 2, 10) == 0

# Fail
print(compute_min_distance(sgd_double_knot, sgd_unknot, 5, 20))


g = sgd_knot_pcs.planar_embedding()
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')  # or 'Qt5Agg' if TkAgg doesn’t work
nx.draw(g, with_labels=True)
plt.show()
