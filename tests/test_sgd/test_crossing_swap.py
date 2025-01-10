from yamada import Edge, Crossing, SpatialGraphDiagram
from yamada.sgd.reidemeister import has_r1, has_r2, apply_r2
from yamada.sgd.utilities import available_crossing_swaps, apply_crossing_swap


def test_crossing_swap_1(unknot_yamada_poly, unknot_infinity_1_2e_1c, unknot_infinity_2_2e_1c):

    sgd_1 = unknot_infinity_1_2e_1c
    sgd_2 = unknot_infinity_2_2e_1c

    # Ensure both unknots have the same Yamada polynomial
    sgd_1_yp = sgd_1.yamada_polynomial()
    sgd_2_yp = sgd_2.yamada_polynomial()
    assert sgd_1_yp == unknot_yamada_poly
    assert sgd_2_yp == unknot_yamada_poly

    # There should only be one possible crossing swap
    arm = available_crossing_swaps(sgd_1)
    assert len(arm) == 1
    assert arm[0] == 'c1'

    # Ensure the crossing swap is correct
    sgd_cs = apply_crossing_swap(sgd_1, arm[0])

    sgd_cs_yp = sgd_cs.yamada_polynomial()
    assert sgd_cs_yp == unknot_yamada_poly


def test_crossing_swap_2(unknot_yamada_poly):
    e1 = Edge(1)
    e2 = Edge(2)
    e3 = Edge(3)
    e4 = Edge(4)
    e5 = Edge(5)
    e6 = Edge(6)

    c1 = Crossing("c1")
    c2 = Crossing("c2")
    c3 = Crossing("c3")

    c1[0] = e2[1]
    c1[1] = e1[0]
    c1[2] = e4[0]
    c1[3] = e3[1]

    c2[0] = e6[0]
    c2[1] = e2[0]
    c2[2] = e3[0]
    c2[3] = e5[0]

    c3[0] = e5[1]
    c3[1] = e4[1]
    c3[2] = e1[1]
    c3[3] = e6[1]

    sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6], crossings=[c1, c2, c3])

    yp_before = sgd.yamada_polynomial()
    # TODO Calculate what the Yamada polynomial should be for the original diagram, but we at least knot it should not be the unknot Yamada polynomial
    assert yp_before != unknot_yamada_poly

    arm = available_crossing_swaps(sgd)

    # There should be 3 possible crossing swaps
    assert len(arm) == 3
    assert set(arm) == {'c1', 'c2', 'c3'}

    # Ensure the crossing swap is correct
    sgd = apply_crossing_swap(sgd, 'c1')
    yp_after = sgd.yamada_polynomial()
    assert yp_after == unknot_yamada_poly

    # Ensure the R2 move is correct
    sgd_has_r2 = has_r2(sgd)
    assert len(sgd_has_r2) > 0
    sgd = apply_r2(sgd, ("c2", "c3"))
    yp_after_r2 = sgd.yamada_polynomial()
    assert yp_after_r2 == unknot_yamada_poly

    # Ensure the R1 move is correct
    sgd_has_r1 = has_r1(sgd)
    assert len(sgd_has_r1) > 0
    # sgd = apply_r1(sgd, "c1")
    # yp_after_r1 = sgd.normalized_yamada_polynomial()
    # assert yp_after_r1 == unknot_yamada_poly
