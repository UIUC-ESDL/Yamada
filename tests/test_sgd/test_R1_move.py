"""
TODO Ensure Non-R1
TODO Reverse R1
"""

from cypari import pari
from yamada import SpatialGraphDiagram, Edge, Crossing, has_r1, apply_r1


# %% Unknots that do not have a Reidemeister 1 move


def test_r1_unknot_1e_1v(unknot_1e_1v):
    sgd_has_r1 = has_r1(unknot_1e_1v)
    assert len(sgd_has_r1) == 0


def test_r1_unknot_2e_2v(unknot_2e_2v):
    sgd_has_r1 = has_r1(unknot_2e_2v)
    assert len(sgd_has_r1) == 0


# %% Unknots that do have a Reidemeister 1 move


# def test_r1_unknot_infinity_1c(unknot_infinity_1c, unknot_yamada_poly):
#     sgd_has_r1 = has_r1(unknot_infinity_1c)
#     assert len(sgd_has_r1) == 1
#     assert 'c1' in sgd_has_r1
#     sgd_post_r1 = apply_r1(unknot_infinity_1c, 'c1')
#     assert sgd_post_r1.normalized_yamada_polynomial() == unknot_yamada_poly

def test_r1_2():
    a = pari('A')

    yp_ground_truth = -a ** 2 - a - 1

    c1 = Crossing('c1')
    c1[1], c1[3] = c1[2], c1[0]

    sgd = SpatialGraphDiagram(crossings=[c1])

    yp_before_r1 = sgd.yamada_polynomial()

    assert yp_before_r1 == yp_ground_truth

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 1
    assert 'c1' in r1_crossing_labels

    sgd = apply_r1(sgd, 'c1')

    yp_after_r1 = sgd.yamada_polynomial()

    assert yp_after_r1 == yp_ground_truth


def test_r1_3():
    a = pari('A')

    yp_ground_truth = -a ** 2 - a - 1

    c1 = Crossing('c1')
    c2 = Crossing('c2')

    e1, e2, e3, e4 = Edge(1), Edge(2), Edge(3), Edge(4)

    c2[3] = e1[0]
    c2[0] = e1[1]
    c2[1] = e2[0]
    c2[2] = e4[1]

    c1[2] = e2[1]
    c1[1] = e4[0]
    c1[0] = e3[1]
    c1[3] = e3[0]

    sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4], crossings=[c1, c2])

    yp_before_r1s = sgd.yamada_polynomial()

    assert yp_before_r1s == yp_ground_truth

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 2
    assert 'c1' in r1_crossing_labels and 'c2' in r1_crossing_labels

    sgd = apply_r1(sgd, 'c1')

    yp_after_first_r1 = sgd.yamada_polynomial()

    assert yp_after_first_r1 == yp_ground_truth

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 1
    assert 'c2' in r1_crossing_labels

    sgd = apply_r1(sgd, 'c2')

    yp_after_second_r1 = sgd.yamada_polynomial()

    assert yp_after_second_r1 == yp_ground_truth

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 0


def test_r1_4():
    a = pari('A')

    yp_ground_truth = -a ** 2 - a - 1

    c1 = Crossing('c1')
    c2 = Crossing('c2')

    e1, e2, e3, e4 = Edge(1), Edge(2), Edge(3), Edge(4)

    c2[3] = e4[1]
    c2[0] = e1[0]
    c2[1] = e1[1]
    c2[2] = e2[0]

    c1[2] = e2[1]
    c1[1] = e4[0]
    c1[0] = e3[1]
    c1[3] = e3[0]

    sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4], crossings=[c1, c2])

    yp_before_r1s = sgd.yamada_polynomial()

    assert yp_before_r1s == yp_ground_truth

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 2
    assert 'c1' in r1_crossing_labels and 'c2' in r1_crossing_labels

    sgd = apply_r1(sgd, 'c1')

    yp_after_first_r1 = sgd.yamada_polynomial()

    assert yp_after_first_r1 == yp_ground_truth

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 1
    assert 'c2' in r1_crossing_labels

    sgd = apply_r1(sgd, 'c2')

    yp_after_second_r1 = sgd.yamada_polynomial()

    assert yp_after_second_r1 == yp_ground_truth

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 0