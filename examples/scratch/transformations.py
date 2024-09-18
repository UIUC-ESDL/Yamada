from cypari import pari
from yamada import SpatialGraphDiagram, Crossing, Edge, Vertex, has_r1, apply_r1, has_r2, apply_r2


def same_yp_for_multiple_vertices():

    a = pari('A')

    yp_gt = -a ** 2 - a - 1

    # One vertex
    e1 = Edge(1)
    v1 = Vertex(2, 'v1')
    e1[0] = v1[0]
    e1[1] = v1[1]
    sgd1 = SpatialGraphDiagram([v1, e1])
    yp1 = sgd1.normalized_yamada_polynomial()
    assert yp1 == yp_gt

    # Two vertices
    e1, e2 = Edge(1), Edge(2)
    v1, v2 = Vertex(2, 'v1'), Vertex(2, 'v2')
    e1[0] = v1[0]
    v1[1] = e2[0]
    e2[1] = v2[0]
    v2[1] = e1[1]
    sgd2 = SpatialGraphDiagram([v1, v2, e1, e2])
    yp2 = sgd2.normalized_yamada_polynomial()
    assert yp2 == yp_gt

    # Three vertices
    e1, e2, e3 = Edge(1), Edge(2), Edge(3)
    v1, v2, v3 = Vertex(2, 'v1'), Vertex(2, 'v2'), Vertex(2, 'v3')
    e1[0] = v1[0]
    v1[1] = e2[0]
    e2[1] = v2[0]
    v2[1] = e3[0]
    e3[1] = v3[0]
    v3[1] = e1[1]
    sgd3 = SpatialGraphDiagram([v1, v2, v3, e1, e2, e3])
    yp3 = sgd3.normalized_yamada_polynomial()
    assert yp3 == yp_gt

def remove_crossing_from_unknot():

    a = pari('A')

    yp_gt = -a ** 2 - a - 1

    e1 = Edge(1)
    e2 = Edge(2)
    x1 = Crossing('x1')

    e1[0] = x1[0]
    e1[1] = x1[1]
    e2[0] = x1[2]
    e2[1] = x1[3]

    sgd = SpatialGraphDiagram([x1, e1, e2])

    yp = sgd.normalized_yamada_polynomial()
    assert yp == yp_gt


    A, i = sgd.crossings[0].adjacent[0]
    B, j = sgd.crossings[0].adjacent[1]
    C, k = sgd.crossings[0].adjacent[2]
    D, l = sgd.crossings[0].adjacent[3]
    sgd.connect(A, i, C, k)
    sgd.connect(B, j, D, l)
    sgd.remove_crossing(sgd.crossings[0])

    yp_after = sgd.normalized_yamada_polynomial()

    assert yp_after == yp_gt


# a = pari('A')
#
# expected = -a ** 2 - a - 1
#
# x1 = Crossing('x1')
# x2 = Crossing('x2')
# x3 = Crossing('x3')
# x4 = Crossing('x4')
#
# e1, e2, e3, e4, e5, e6, e7, e8 = Edge(1), Edge(2), Edge(3), Edge(4), Edge(5), Edge(6), Edge(7), Edge(8)
#
# # x1
# x1[0] = e8[0]
# x1[1] = e2[0]
# x1[2] = e1[0]
# x1[3] = e1[1]
#
# # x2
# x2[0] = e7[1]
# x2[1] = e2[1]
# x2[2] = e8[1]
# x2[3] = e3[0]
#
# # x3
# x3[0] = e3[1]
# x3[1] = e6[1]
# x3[2] = e4[0]
# x3[3] = e7[0]
#
# # x4
# x4[0] = e5[1]
# x4[1] = e4[1]
# x4[2] = e6[0]
# x4[3] = e5[0]
#
# sgd = SpatialGraphDiagram([x1, x2, x3, x4, e1, e2, e3, e4, e5, e6, e7, e8])
#
# yp_before = sgd.normalized_yamada_polynomial()
#
# # Remove the first loop
#
# sgd_has_r2, r2_input = has_r2(sgd)
#
# assert sgd_has_r2
#
# sgd = apply_r2(sgd, r2_input)
#
# yp_after_1 = sgd.normalized_yamada_polynomial()
#
# assert yp_before == expected


# Remove the second loop

# sgd_has_r2, r2_input = has_r2(sgd)
#
# assert sgd_has_r2
#
# sgd = apply_r2(sgd, r2_input)
#
# yp_after_2 = sgd.normalized_yamada_polynomial()
#
# assert yp_after_1 == yp_after_2
# assert yp_after_2 == expected


a = pari('A')

yp_ground_truth = -a ** 2 - a - 1

x1 = Crossing('x1')
x2 = Crossing('x2')
x3 = Crossing('x3')
x4 = Crossing('x4')

e1, e2, e3, e4, e5, e6, e7, e8 = Edge(1), Edge(2), Edge(3), Edge(4), Edge(5), Edge(6), Edge(7), Edge(8)

# x1
x1[0] = e8[0]
x1[1] = e2[0]
x1[2] = e1[0]
x1[3] = e1[1]

# x2
x2[0] = e7[1]
x2[1] = e2[1]
x2[2] = e8[1]
x2[3] = e3[0]

# x3
x3[0] = e3[1]
x3[1] = e6[1]
x3[2] = e4[0]
x3[3] = e7[0]

# x4
x4[0] = e5[0]
x4[1] = e5[1]
x4[2] = e4[1]
x4[3] = e6[0]

sgd = SpatialGraphDiagram([x1, x2, x3, x4, e1, e2, e3, e4, e5, e6, e7, e8])

yp_before_r2s = sgd.normalized_yamada_polynomial()

assert yp_before_r2s == yp_ground_truth

# Remove the first loop

r2_crossing_labels = has_r2(sgd)

assert len(r2_crossing_labels) == 2
assert ('x1', 'x2') in r2_crossing_labels or ('x2', 'x1') in r2_crossing_labels

sgd = apply_r2(sgd, ('x1', 'x2'))

yp_after_first_r2 = sgd.normalized_yamada_polynomial()

assert yp_after_first_r2 == yp_ground_truth

# Remove the second loop

r2_crossing_labels = has_r2(sgd)

assert len(r2_crossing_labels) == 1
assert ('x3', 'x4') in r2_crossing_labels or ('x4', 'x3') in r2_crossing_labels

sgd = apply_r2(sgd, ('x3', 'x4'))

yp_after_second_r2 = sgd.normalized_yamada_polynomial()

assert yp_after_second_r2 == yp_ground_truth

r2_crossing_labels = has_r2(sgd)

assert len(r2_crossing_labels) == 0
