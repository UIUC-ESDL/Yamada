def test_unknot_two_ccw_twists(unknot_two_ccw_twists, poly_unknot):
    sgd = unknot_two_ccw_twists()
    assert sgd.yamada_polynomial() == poly_unknot

def test_unknot_one_ccw_one_cw_twist(unknot_one_ccw_one_cw_twist, poly_unknot):
    sgd = unknot_one_ccw_one_cw_twist()
    assert sgd.yamada_polynomial() == poly_unknot

def test_unknot_two_cw_twists(unknot_two_cw_twists, poly_unknot):
    sgd = unknot_two_cw_twists()
    assert sgd.yamada_polynomial() == poly_unknot









# def test_unknot_double_loop_same_4e_2c(unknot_double_loop_same_4e_2c):
#     assert unknot_double_loop_same_4e_2c
#
# def test_unknot_double_loop_opposite_4e_2c(unknot_double_loop_opposite_4e_2c):
#     """An unknot with two loops that have opposing crossing orientations."""
#     assert unknot_double_loop_opposite_4e_2c