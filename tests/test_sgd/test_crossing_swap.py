from cypari import pari
from yamada import Edge, Crossing, SpatialGraphDiagram
from yamada.sgd.reidemeister import has_r1, apply_r1, has_r2, apply_r2
from yamada.sgd.utilities import available_crossing_swaps, apply_crossing_swap


def test_crossing_swap_1(unknot_yamada_poly, unknot_infinity_1_2e_1c, unknot_infinity_2_2e_1c):

    sgd_1 = unknot_infinity_1_2e_1c
    sgd_2 = unknot_infinity_2_2e_1c

    # Ensure both unknots have the same Yamada polynomial
    sgd_1_yp = sgd_1.normalized_yamada_polynomial()
    sgd_2_yp = sgd_2.normalized_yamada_polynomial()
    assert sgd_1_yp == unknot_yamada_poly
    assert sgd_2_yp == unknot_yamada_poly

    # There should only be one possible crossing swap
    arm = available_crossing_swaps(sgd_1)
    assert len(arm) == 1
    assert arm[0] == 'c1'

    # Ensure the crossing swap is correct
    sgd_cs = apply_crossing_swap(sgd_1, arm[0])

    sgd_cs_yp = sgd_cs.normalized_yamada_polynomial()
    assert sgd_cs_yp == unknot_yamada_poly


def test_crossing_swap_2(unknot_yamada_poly):
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

    yp_before = sgd.normalized_yamada_polynomial()
    # TODO Calculate what the Yamada polynomial should be for the original diagram, but we at least knot it should not be the unknot Yamada polynomial
    assert yp_before != unknot_yamada_poly

    arm = available_crossing_swaps(sgd)

    # There should be 3 possible crossing swaps
    assert len(arm) == 3
    assert set(arm) == {'x1', 'x2', 'x3'}

    # Ensure the crossing swap is correct
    sgd = apply_crossing_swap(sgd, 'x1')
    yp_after = sgd.normalized_yamada_polynomial()
    assert yp_after == unknot_yamada_poly

    # Ensure the R2 move is correct
    sgd_has_r2 = has_r2(sgd)
    assert len(sgd_has_r2) > 0
    sgd = apply_r2(sgd, ("x2", "x3"))
    yp_after_r2 = sgd.normalized_yamada_polynomial()
    assert yp_after_r2 == unknot_yamada_poly

    # Ensure the R1 move is correct
    sgd_has_r1 = has_r1(sgd)
    assert len(sgd_has_r1) > 0
    # sgd = apply_r1(sgd, "x1")
    # yp_after_r1 = sgd.normalized_yamada_polynomial()
    # assert yp_after_r1 == unknot_yamada_poly
