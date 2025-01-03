from cypari import pari
from yamada import Edge, Crossing, Vertex, SpatialGraphDiagram
from yamada.Reidemeister import has_r1, has_r2, apply_r1, apply_r2
from yamada.Anti_Reidemeister import anti_reidemeister_moves, apply_anti_reidemeister_move

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

def create_knot_post_r2():

    e1, e2, e3, e4, e5, e6 = Edge(1), Edge(2), Edge(3), Edge(4), Edge(5), Edge(6)
    v1 = Vertex(degree=2, label="v1")
    v2 = Vertex(degree=2, label="v2")
    v3 = Vertex(degree=2, label="v3")
    v4 = Vertex(degree=2, label="v4")

    x1 = Crossing("x1")

    x1[0] = e2[1]
    x1[1] = e1[0]
    x1[2] = e4[0]
    x1[3] = e3[1]

    e1[1] = v3[1]
    v3[0] = e5[1]
    e5[0] = v2[1]
    v2[0] = e2[0]

    e4[1] = v4[0]
    v4[1] = e6[1]
    e6[0] = v1[0]
    v1[1] = e3[0]

    sgd = SpatialGraphDiagram([e1, e2, e3, e4, e5, e6, v1, v2, v3, v4, x1])

    return sgd


sgd_knot = create_knot()
sgd_post_crossing_swap = create_knot_post_crossing_swap()
sgd_knot_post_r2 = create_knot_post_r2()

# Define the ground truth
a = pari('A')
yp_unknot = -a ** 2 - a - 1

# Verify the original knot is not the unknot
assert sgd_knot.normalized_yamada_polynomial() != yp_unknot

# Perform the crossing swap
sgd_knot = apply_anti_reidemeister_move(sgd_knot, "x2")
assert sgd_knot.normalized_yamada_polynomial() == yp_unknot

# Perform the R2 move
sgd_has_r2 = has_r2(sgd_knot)
assert len(sgd_has_r2) == 2
sgd_knot = apply_r2(sgd_knot, ("x2", "x3"))
assert sgd_knot.normalized_yamada_polynomial() == yp_unknot

print(sgd_knot.crossings[0].adjacent)

sgd_has_r1 = has_r1(sgd_knot)
# assert len(sgd_has_r1) > 0
