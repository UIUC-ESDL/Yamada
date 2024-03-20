from cypari import pari
from yamada.spatial_graph_diagrams.spatial_graph_diagrams import SpatialGraphDiagram
from yamada.spatial_graph_diagrams.diagram_elements import Vertex, Edge, Crossing
from yamada.spatial_graph_diagrams.Reidemeister import *
import numpy as np
import random


np.random.seed(0)
random.seed(0)

a = pari('A')


# R3: Infinity symbol and circle

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

def post_r3_corrected():

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



# sgd = pre_r3()
#
# print('Before R Simplify:', sgd.normalized_yamada_polynomial())
#
# sgd, r1_count, r2_count, r3_count = reidemeister_simplify(sgd, n_tries=10)
#
# print('After R Simplify: ', sgd.normalized_yamada_polynomial())

a = pari('A')

expected = -a ** 2 - a - 1

x1 = Crossing('x1')
x2 = Crossing('x2')

x1[0] = x2[2]
x1[1] = x2[1]
x1[2] = x1[3]
x2[0] = x2[3]

sgd = SpatialGraphDiagram([x1, x2])

yp_before = sgd.normalized_yamada_polynomial()

sgd_has_r2, r2_input = has_r2(sgd)

# assert sgd_has_r2

sgd = apply_r2(sgd, r2_input)

yp_after = sgd.normalized_yamada_polynomial()
#
# assert yp_before == yp_after
#
# assert yp_after == expected

