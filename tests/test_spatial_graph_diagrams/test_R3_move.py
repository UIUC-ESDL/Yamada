from cypari import pari
from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing, has_r3, apply_r3

def pre_r3():

    x0 = Crossing('x0')
    x1 = Crossing('x1')
    x2 = Crossing('x2')
    x3 = Crossing('x3')
    x4 = Crossing('x4')

    e0 = Edge('e0')
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    e4 = Edge('e4')
    e5 = Edge('e5')
    e6 = Edge('e6')
    e7 = Edge('e7')
    e8 = Edge('e8')
    e9 = Edge('e9')

    x0[0] = e0[0]
    x0[1] = e3[0]
    x0[2] = e2[0]
    x0[3] = e1[0]

    x1[0] = e4[1]
    x1[1] = e0[1]
    x1[2] = e5[0]
    x1[3] = e8[0]

    x2[0] = e5[1]
    x2[1] = e1[1]
    x2[2] = e6[1]
    x2[3] = e8[1]

    x3[0] = e7[1]
    x3[1] = e9[1]
    x3[2] = e6[0]
    x3[3] = e2[1]

    x4[0] = e4[0]
    x4[1] = e9[0]
    x4[2] = e7[0]
    x4[3] = e3[1]

    sgd = SpatialGraphDiagram([x0, x1, x2, x3, x4, e0, e1, e2, e3, e4, e5, e6, e7, e8, e9])

    return sgd

def post_r3():

    x0 = Crossing('x0')
    x1 = Crossing('x1')
    x2 = Crossing('x2')
    x3 = Crossing('x3')
    x4 = Crossing('x4')

    e0 = Edge('e0')
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    e4 = Edge('e4')
    e5 = Edge('e5')
    e6 = Edge('e6')
    e7 = Edge('e7')
    e8 = Edge('e8')
    e9 = Edge('e9')
    er1 = Edge('er1')
    er2 = Edge('er2')

    x0[0] = er1[0]
    x0[1] = er2[0]
    x0[2] = e2[0]
    x0[3] = e1[0]

    x1[0] = e4[1]
    x1[1] = e0[1]
    x1[2] = e5[0]
    x1[3] = e8[0]

    x2[0] = e5[1]
    x2[1] = e0[0]
    x2[2] = e6[1]
    x2[3] = er1[1]

    x3[0] = e7[1]
    x3[1] = er2[1]
    x3[2] = e6[0]
    x3[3] = e3[0]

    x4[0] = e4[0]
    x4[1] = e9[0]
    x4[2] = e7[0]
    x4[3] = e3[1]

    e1[1] = e8[1]
    e2[1] = e9[1]

    sgd = SpatialGraphDiagram([x0, x1, x2, x3, x4, e0, e1, e2, e3, e4, e5, e6, e7, e8, e9, er1, er2])

    return sgd


def test_r3():
    a = pari('A')

    sgd = pre_r3()

    yp1 = sgd.normalized_yamada_polynomial()

    pre_r3_has_r3, _ = has_r3(sgd)
    assert pre_r3_has_r3

    # Hard-coded demo
    stationary_crossing = 'x0'
    moving_crossing_1 = 'x3'
    moving_crossing_2 = 'x2'
    crossing_edge = 'e6'
    stationary_edge_1 = 'e2'
    stationary_edge_2 = 'e1'
    r3_input = {
        'stationary_crossing': stationary_crossing,
        'moving_crossing_1': moving_crossing_1,
        'moving_crossing_2': moving_crossing_2,
        'crossing_edge': crossing_edge,
        'stationary_edge_1': stationary_edge_1,
        'stationary_edge_2': stationary_edge_2
    }

    sgd_r3 = apply_r3(sgd, r3_input)

    yp2 = sgd_r3.normalized_yamada_polynomial()

    assert yp1 == yp2

    post_r3_has_r3, _ = has_r3(sgd_r3)
    assert post_r3_has_r3


# TODO, add simple example that repeats the R3 move back and forth n times, checks original inputs