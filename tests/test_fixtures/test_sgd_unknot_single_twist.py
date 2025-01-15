# def test_unknot_inf_cw_0e_0v_1c(unknot_inf_cw_0e_0v_1c, poly_unknot):
#     sgd = unknot_inf_cw_0e_0v_1c
#     assert sgd
#     assert len(sgd.edges) == 2
#     assert len(sgd.vertices) == 0
#     assert len(sgd.crossings) == 1
#     assert sgd.edges[0].label == 'e1'
#     assert sgd.edges[1].label == 'e2'
#     assert sgd.crossings[0].label == 'c1'
#     assert sgd.yamada_polynomial() == poly_unknot
#
#     sgd.simplify_diagram()
#     assert len(sgd.edges) == 2
#     assert len(sgd.vertices) == 0
#     assert len(sgd.crossings) == 1
#     assert sgd.edges[0].label == 'e1'
#     assert sgd.edges[1].label == 'e2'
#     assert sgd.crossings[0].label == 'c1'
#     assert sgd.yamada_polynomial() == poly_unknot
#
#
#
# def test_unknot_inf_cw_1e_0v_1c(unknot_inf_cw_1e_0v_1c, poly_unknot):
#     sgd = unknot_inf_cw_1e_0v_1c
#     assert sgd
#     assert len(sgd.edges) == 2
#     assert len(sgd.vertices) == 0
#     assert len(sgd.crossings) == 1
#     assert sgd.edges[0].label == 'e1'
#     assert sgd.edges[1].label == 'e2'
#     assert sgd.crossings[0].label == 'c1'
#     assert sgd.yamada_polynomial() == poly_unknot
#
#     sgd.simplify_diagram()
#     assert len(sgd.edges) == 2
#     assert len(sgd.vertices) == 0
#     assert len(sgd.crossings) == 1
#     assert sgd.edges[0].label == 'e1'
#     assert sgd.edges[1].label == 'e2'
#     assert sgd.crossings[0].label == 'c1'
#     assert sgd.yamada_polynomial() == poly_unknot
#
#
#
# def test_unknot_inf_cw_2e_0v_1c_1(unknot_inf_cw_2e_0v_1c_1, poly_unknot):
#     sgd = unknot_inf_cw_2e_0v_1c_1
#     assert sgd
#     assert len(sgd.edges) == 2
#     assert len(sgd.vertices) == 0
#     assert len(sgd.crossings) == 1
#     assert sgd.edges[0].label == 'e1'
#     assert sgd.edges[1].label == 'e2'
#     assert sgd.crossings[0].label == 'c1'
#     assert sgd.yamada_polynomial() == poly_unknot
#
#     sgd.simplify_diagram()
#     assert len(sgd.edges) == 2
#     assert len(sgd.vertices) == 0
#     assert len(sgd.crossings) == 1
#     assert sgd.edges[0].label == 'e1'
#     assert sgd.edges[1].label == 'e2'
#     assert sgd.crossings[0].label == 'c1'
#     assert sgd.yamada_polynomial() == poly_unknot
#
#
# def test_unknot_inf_cw_2e_0v_1c_2(unknot_inf_cw_2e_0v_1c_2, poly_unknot):
#     sgd = unknot_inf_cw_2e_0v_1c_2
#     assert sgd
#     assert len(sgd.edges) == 3
#     assert len(sgd.vertices) == 1
#     assert len(sgd.crossings) == 1
#     assert sgd.edges[0].label == 'e1'
#     assert sgd.edges[1].label == 'e2'
#     assert sgd.edges[2].label == 'e3'
#     assert sgd.vertices[0].label == 'v1'
#     assert sgd.crossings[0].label == 'c1'
#     assert sgd.yamada_polynomial() == poly_unknot
#
#     sgd.simplify_diagram()
#     assert len(sgd.edges) == 2
#     assert len(sgd.vertices) == 0
#     assert len(sgd.crossings) == 1
#     assert sgd.edges[0].label == 'e1'
#     assert sgd.edges[1].label == 'e3'
#     # TODO Should simplify re-normalize?
#     assert sgd.crossings[0].label == 'c1'
#     assert sgd.yamada_polynomial() == poly_unknot


# def test_unknot_infinity_2_2e_1c(unknot_infinity_ccw_2e_1c):
#     assert unknot_infinity_ccw_2e_1c
#
#
# def test_unknot_infinity_1_4e_2v_1c(unknot_infinity_1_4e_2v_1c):
#     assert unknot_infinity_1_4e_2v_1c