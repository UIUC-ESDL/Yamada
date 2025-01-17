from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing
from yamada import SpatialGraph
from yamada import available_r1_moves, apply_r1_move, available_r2_moves, apply_r2_move


e1 = Edge('e1')
e2 = Edge('e2')
e3 = Edge('e3')
e4 = Edge('e4')
e5 = Edge('e5')
e6 = Edge('e6')
e7 = Edge('e7')
e8 = Edge('e8')
c1 = Crossing('c1')
c2 = Crossing('c2')
c3 = Crossing('c3')
c4 = Crossing('c4')

c1[0] = e8[0]
c1[1] = e2[0]
c1[2] = e1[0]
c1[3] = e1[1]

c2[0] = e7[1]
c2[1] = e2[1]
c2[2] = e8[1]
c2[3] = e3[0]

c3[0] = e6[1]
c3[1] = e4[0]
c3[2] = e7[0]
c3[3] = e3[1]

c4[0] = e5[1]
c4[1] = e4[1]
c4[2] = e6[0]
c4[3] = e5[0]

sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6, e7, e8], crossings=[c1, c2, c3, c4])


r2_moves = available_r2_moves(sgd)

assert len(sgd.edges) == 8
assert len(sgd.vertices) == 0
assert len(sgd.crossings) == 4

sgd = apply_r2_move(sgd, ('c1', 'c2'), simplify=False)

assert len(sgd.edges) == 8
assert len(sgd.vertices) == 4
assert len(sgd.crossings) == 2

sgd.simplify_diagram()


assert len(sgd.edges) == 4
assert len(sgd.vertices) == 0
assert len(sgd.crossings) == 2

