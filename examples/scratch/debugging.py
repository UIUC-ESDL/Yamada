from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing
from yamada import SpatialGraph
from yamada import available_r1_moves, apply_r1_move, available_r2_moves, apply_r2_move, available_r3_moves, \
    apply_r3_move

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
c1 = Crossing('c1')
c2 = Crossing('c2')
c3 = Crossing('c3')
c4 = Crossing('c4')
c5 = Crossing('c5')

c1[0] = e1[0]
c1[1] = e4[0]
c1[2] = e3[0]
c1[3] = e2[0]

c2[0] = e6[0]
c2[1] = e9[0]
c2[2] = e5[1]
c2[3] = e1[1]

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

# r3_moves_1 = available_r3_moves(sgd)


r3_3 = {'stationary_crossing': 'c1',
        'stationary_edge_1': 'e2',
        'stationary_edge_2': 'e3',
        'moving_crossing_1': 'c3',
        'moving_crossing_2': 'c4',
        'moving_edge': 'e7'}

sgd_post_r3 = apply_r3_move(sgd, r3_3)

r3_rev = {'stationary_crossing': 'c1',
          'stationary_edge_1': 'e3',
          'stationary_edge_2': 'e2',
          'moving_crossing_1': 'c4',
          'moving_crossing_2': 'c3',
          'moving_edge': 'e7'}

sgd_post_rev_r3 = apply_r3_move(sgd_post_r3, r3_rev)

# assert sgd.crossings[]

# There should be 6 R3 moves available...

# r3_moves_2 = available_r3_moves(sgd_2)
#
# sgd_3 = apply_r3_move(sgd_2, r3_moves_2[0])
