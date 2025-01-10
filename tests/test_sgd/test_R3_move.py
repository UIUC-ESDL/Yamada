from cypari import pari
from yamada import SpatialGraphDiagram, Edge, Crossing, has_r3, apply_r3


def pre_r3():

    c1 = Crossing('c1')
    c2 = Crossing('c2')
    c3 = Crossing('c3')
    c4 = Crossing('c4')
    c5 = Crossing('c5')

    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    e4 = Edge('e4')
    e5 = Edge('e5')
    e6 = Edge('e6')
    e7 = Edge('e7')
    e8 = Edge('e8')
    e9 = Edge('e9')
    e10 = Edge('e10')

    c1[0] = e1[0]
    c1[1] = e4[0]
    c1[2] = e3[0]
    c1[3] = e2[0]

    c2[0] = e5[1]
    c2[1] = e1[1]
    c2[2] = e6[0]
    c2[3] = e9[0]

    c3[0] = e6[1]
    c3[1] = e2[1]
    c3[2] = e7[1]
    c3[3] = e9[1]

    c4[0] = e8[1]
    c4[1] = e10[1]
    c4[2] = e7[0]
    c4[3] = e3[1]

    c5[0] = e5[0]
    c5[1] = e10[0]
    c5[2] = e8[0]
    c5[3] = e4[1]

    sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6, e7, e8, e9, e10], crossings=[c1, c2, c3, c4, c5])

    return sgd


def post_r3():

    c1 = Crossing('c1')
    c2 = Crossing('c2')
    c3 = Crossing('c3')
    c4 = Crossing('c4')
    c5 = Crossing('c5')

    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    e4 = Edge('e4')
    e5 = Edge('e5')
    e6 = Edge('e6')
    e7 = Edge('e7')
    e8 = Edge('e8')
    e9 = Edge('e9')
    e10 = Edge('e10')
    e11 = Edge('e11')
    e12 = Edge('e12')

    c1[0] = e11[0]
    c1[1] = e12[0]
    c1[2] = e3[0]
    c1[3] = e2[0]

    c2[0] = e5[1]
    c2[1] = e1[1]
    c2[2] = e6[0]
    c2[3] = e9[0]

    c3[0] = e6[1]
    c3[1] = e1[0]
    c3[2] = e7[1]
    c3[3] = e11[1]

    c4[0] = e8[1]
    c4[1] = e12[1]
    c4[2] = e7[0]
    c4[3] = e4[0]

    c5[0] = e5[0]
    c5[1] = e10[0]
    c5[2] = e8[0]
    c5[3] = e4[1]

    e2[1] = e9[1]
    e3[1] = e10[1]

    sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12], crossings=[c1, c2, c3, c4, c5])

    return sgd


def test_r3():
    a = pari('A')

    sgd = pre_r3()

    yp1 = sgd.yamada_polynomial()

    pre_r3_has_r3, _ = has_r3(sgd)
    assert pre_r3_has_r3

    # Hard-coded demo
    stationary_crossing = 'c1'
    moving_crossing_1 = 'c4'
    moving_crossing_2 = 'c3'
    crossing_edge = 'e7'
    stationary_edge_1 = 'e3'
    stationary_edge_2 = 'e2'
    r3_input = {
        'stationary_crossing': stationary_crossing,
        'moving_crossing_1': moving_crossing_1,
        'moving_crossing_2': moving_crossing_2,
        'crossing_edge': crossing_edge,
        'stationary_edge_1': stationary_edge_1,
        'stationary_edge_2': stationary_edge_2
    }

    sgd_r3 = apply_r3(sgd, r3_input)

    yp2 = sgd_r3.yamada_polynomial()

    assert yp1 == yp2

    post_r3_has_r3, _ = has_r3(sgd_r3)
    assert post_r3_has_r3


# TODO, add simple example that repeats the R3 move back and forth n times, checks original inputs