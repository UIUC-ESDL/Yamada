from cypari import pari
from yamada import SpatialGraphDiagram, Crossing, Edge, has_r2, apply_r2


def test_r2():
    a = pari('A')

    yp_ground_truth = -a ** 2 - a - 1

    c1 = Crossing('c1')
    c2 = Crossing('c2')

    c1[0] = c2[2]
    c1[1] = c2[1]
    c1[2] = c1[3]
    c2[0] = c2[3]

    sgd = SpatialGraphDiagram(crossings=[c1, c2])

    yp_before = sgd.yamada_polynomial()

    assert yp_before == yp_ground_truth

    r2_crossing_labels = has_r2(sgd)

    assert len(r2_crossing_labels) == 1
    assert ('c1', 'c2') in r2_crossing_labels or ('c2', 'c1') in r2_crossing_labels

    sgd = apply_r2(sgd, ('c1', 'c2'))

    yp_after = sgd.yamada_polynomial()

    assert yp_after == yp_ground_truth


def test_r2_2():
    a = pari('A')

    yp_ground_truth = -a ** 2 - a - 1

    c1 = Crossing('c1')
    c2 = Crossing('c2')
    c3 = Crossing('c3')
    c4 = Crossing('c4')

    e1, e2, e3, e4, e5, e6, e7, e8 = Edge(1), Edge(2), Edge(3), Edge(4), Edge(5), Edge(6), Edge(7), Edge(8)

    # x1
    c1[0] = e8[0]
    c1[1] = e2[0]
    c1[2] = e1[0]
    c1[3] = e1[1]

    # x2
    c2[0] = e7[1]
    c2[1] = e2[1]
    c2[2] = e8[1]
    c2[3] = e3[0]

    # x3
    c3[0] = e6[1]
    c3[1] = e4[0]
    c3[2] = e7[0]
    c3[3] = e3[1]

    # x4
    c4[0] = e5[1]
    c4[1] = e4[1]
    c4[2] = e6[0]
    c4[3] = e5[0]

    sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6, e7, e8], crossings=[c1, c2, c3, c4])

    yp_before_r2s = sgd.yamada_polynomial()

    assert yp_before_r2s == yp_ground_truth

    # Remove the first loop

    r2_crossing_labels = has_r2(sgd)

    assert len(
        r2_crossing_labels) == 3  # I intended it to be 2, but since both loops are on the same side, the edge 3 can also be treated as a loop.
    assert ('c1', 'c2') in r2_crossing_labels or ('c2', 'c1') in r2_crossing_labels

    sgd = apply_r2(sgd, ('c1', 'c2'))

    yp_after_first_r2 = sgd.yamada_polynomial()

    assert yp_after_first_r2 == yp_ground_truth

    # Remove the second loop

    r2_crossing_labels = has_r2(sgd)

    assert len(r2_crossing_labels) == 1
    assert ('c3', 'c4') in r2_crossing_labels or ('c4', 'c3') in r2_crossing_labels

    sgd = apply_r2(sgd, ('c3', 'c4'))

    yp_after_second_r2 = sgd.yamada_polynomial()

    assert yp_after_second_r2 == yp_ground_truth

    r2_crossing_labels = has_r2(sgd)

    assert len(r2_crossing_labels) == 0


def test_r2_3():
    a = pari('A')

    yp_ground_truth = -a ** 2 - a - 1

    c1 = Crossing('c1')
    c2 = Crossing('c2')
    c3 = Crossing('c3')
    c4 = Crossing('c4')

    e1, e2, e3, e4, e5, e6, e7, e8 = Edge(1), Edge(2), Edge(3), Edge(4), Edge(5), Edge(6), Edge(7), Edge(8)

    # x1
    c1[0] = e8[0]
    c1[1] = e2[0]
    c1[2] = e1[0]
    c1[3] = e1[1]

    # x2
    c2[0] = e7[1]
    c2[1] = e2[1]
    c2[2] = e8[1]
    c2[3] = e3[0]

    # x3
    c3[0] = e3[1]
    c3[1] = e6[1]
    c3[2] = e4[0]
    c3[3] = e7[0]

    # x4
    c4[0] = e5[0]
    c4[1] = e5[1]
    c4[2] = e4[1]
    c4[3] = e6[0]

    sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6, e7, e8], crossings=[c1, c2, c3, c4])

    yp_before_r2s = sgd.yamada_polynomial()

    assert yp_before_r2s == yp_ground_truth

    # Remove the first loop

    r2_crossing_labels = has_r2(sgd)

    assert len(r2_crossing_labels) == 2
    assert ('c1', 'c2') in r2_crossing_labels or ('c2', 'c1') in r2_crossing_labels

    sgd = apply_r2(sgd, ('c1', 'c2'))

    yp_after_first_r2 = sgd.yamada_polynomial()

    assert yp_after_first_r2 == yp_ground_truth

    # Remove the second loop

    r2_crossing_labels = has_r2(sgd)

    assert len(r2_crossing_labels) == 1
    assert ('c3', 'c4') in r2_crossing_labels or ('c4', 'c3') in r2_crossing_labels

    sgd = apply_r2(sgd, ('c3', 'c4'))

    yp_after_second_r2 = sgd.yamada_polynomial()

    assert yp_after_second_r2 == yp_ground_truth

    r2_crossing_labels = has_r2(sgd)

    assert len(r2_crossing_labels) == 0
