from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing
from yamada import SpatialGraph
from yamada import has_r1, apply_r1


e1 = Edge('e1')
e2 = Edge('e2')
e3 = Edge('e3')
v1 = Vertex(2, 'v1')
v2 = Vertex(2, 'v2')
v1[0] = v2[1]
v1[1] = e1[0]
e1[1] = e2[0]
e2[1] = e3[0]
e3[1] = v2[0]
unknot_3e_2v_1 = SpatialGraphDiagram(edges=[e1, e2, e3], vertices=[v1, v2])


assert unknot_3e_2v_1
assert len(unknot_3e_2v_1.vertices) == 3
assert len(unknot_3e_2v_1.edges) == 3
assert len(unknot_3e_2v_1.crossings) == 0
assert unknot_3e_2v_1.edges[0].label == 'e1'
assert unknot_3e_2v_1.edges[1].label == 'e2'
assert unknot_3e_2v_1.edges[2].label == 'e3'
assert unknot_3e_2v_1.vertices[0].label == 'v1'
assert unknot_3e_2v_1.vertices[1].label == 'v2'
assert unknot_3e_2v_1.vertices[2].label == 'v3'
