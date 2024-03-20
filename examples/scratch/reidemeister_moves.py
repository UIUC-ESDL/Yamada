from cypari import pari
from yamada.spatial_graph_diagrams.spatial_graph_diagrams import SpatialGraphDiagram
from yamada.spatial_graph_diagrams.diagram_elements import Vertex, Edge, Crossing
from yamada.spatial_graph_diagrams.Reidemeister import *

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

import numpy as np
np.random.seed(0)
import random
random.seed(0)

sgd = pre_r3()

print('Before R Simplify:', sgd.normalized_yamada_polynomial())


# sgd_has_r3, stationary_crossings, moving_crossings_1, moving_crossings_2, crossing_edges, stationary_edges_1, stationary_edges_2 = has_r3(sgd)
# ir3 = crossing_edges.index('e6')
# sgd = apply_r3(sgd, stationary_crossings[ir3], moving_crossings_1[ir3], moving_crossings_2[ir3], stationary_edges_1[ir3], stationary_edges_2[ir3])

sgd, r1_count, r2_count, r3_count = reidemeister_simplify(sgd)

# sgd_has_r2, crossing_pairs, edge_pairs = has_r2(sgd)
# print('has r2?', sgd_has_r2)
#
# sgd = r2(sgd, crossing_pairs[0])
#
print('After R Simplify: ', sgd.normalized_yamada_polynomial())
# TODO Problem: Added vertices, things don't appear adjacent.  Need to fix this.
# print('R1 count:', r1_count)
# print('R2 count:', r2_count)
# print('R3 count:', r3_count)
#
# sgd_has_r2, crossing_pairs, edge_pairs = has_r2(sgd)
# print('has r2?', sgd_has_r2)
#
# sgd = r2(sgd, crossing_pairs[0])
#
# print('After R2: ', sgd.normalized_yamada_polynomial())








# # Ensure
# print('Has R2:', has_r2(sgd)[0])

# sgd = r2(sgd)
#
# yp_after = sgd.normalized_yamada_polynomial()
#
# assert yp_before == yp_after
#
# assert yp_after == expected



# pre_r3_has_r3, candidates = has_r3(sgd)
# print('Has R3?', pre_r3_has_r3)



# print('has r2?', has_r2(sgd)[0])

# Hard-coded demo
# reidemeister_crossing = 'x0'
# other_crossing_1 = 'x3'
# other_crossing_2 = 'x2'
# reidemeister_edge = 'e6'
# other_edge_1 = 'e2'
# other_edge_2 = 'e1'

# candidate = candidates[0]
# reidemeister_crossing = candidate['reidemeister crossing']
# other_crossing_1 = candidate['other crossing 1']
# other_crossing_2 = candidate['other crossing 2']
# reidemeister_edge = candidate['reidemeister edge']
# other_edge_1 = candidate['other edge 1']
# other_edge_2 = candidate['other edge 2']
#
#
# sgd = r3(sgd, reidemeister_crossing, other_crossing_1, other_crossing_2, reidemeister_edge, other_edge_1, other_edge_2)




# Reassign the Reidemeister crossing edges



# yp = sgd.normalized_yamada_polynomial()
# print('After R3:', yp)
# print('Has R3?', has_r3(sgd)[0])

