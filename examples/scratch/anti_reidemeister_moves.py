from cypari import pari
from yamada import Edge, Crossing, SpatialGraphDiagram
from yamada.sgd.Reidemeister import has_r2, apply_r2
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
    # After crossing swap
    # x2[0] = e5[0]
    # x2[1] = e6[0]
    # x2[2] = e2[0]
    # x2[3] = e3[0]

    x3[0] = e5[1]
    x3[1] = e4[1]
    x3[2] = e1[1]
    x3[3] = e6[1]

    sgd = SpatialGraphDiagram([e1, e2, e3, e4, e5, e6, x1, x2, x3])

    return sgd


a = pari('A')

yp_ground_truth = -a ** 2 - a - 1

e1, e2, e3, e4, e5, e6 = Edge(1), Edge(2), Edge(3), Edge(4), Edge(5), Edge(6)

x1, x2, x3 = Crossing("x1"), Crossing("x2"), Crossing("x3")

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
x3[2] = e1[1]
x3[3] = e6[1]

sgd = SpatialGraphDiagram([e1, e2, e3, e4, e5, e6, x1, x2, x3])

yp_before = sgd.yamada_polynomial()
# TODO Calculate what the Yamada polynomial should be for the original diagram, but we at least knot it should not be the unknot Yamada polynomial
assert yp_before != yp_ground_truth

arm = anti_reidemeister_moves(sgd)

# There should be 3 possible crossing swaps
assert len(arm) == 3
assert set(arm) == {'x1', 'x2', 'x3'}

# Ensure the crossing swap is correct
sgd = apply_anti_reidemeister_move(sgd, 'x1')
yp_after = sgd.yamada_polynomial()
assert yp_after == yp_ground_truth

# Ensure the R2 move is correct
sgd_has_r2 = has_r2(sgd)
assert len(sgd_has_r2) > 0
sgd = apply_r2(sgd, ("x2", "x3"))
yp_after_r2 = sgd.yamada_polynomial()
assert yp_after_r2 == yp_ground_truth
# sgd_has_r1 = has_r1(sgd)
# assert len(sgd_has_r1) > 0
# sgd = apply_r1(sgd, "x1")
# yp_after_r1 = sgd.normalized_yamada_polynomial()
# assert yp_after_r1 == yp_ground_truth


