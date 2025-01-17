def test_unknot_two_ccw_twists(unknot_two_ccw_twists, poly_unknot):
    sgd = unknot_two_ccw_twists()
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_one_ccw_one_cw_twist(unknot_one_ccw_one_cw_twist, poly_unknot):
    sgd = unknot_one_ccw_one_cw_twist()
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_two_cw_twists(unknot_two_cw_twists, poly_unknot):
    sgd = unknot_two_cw_twists()
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_two_over_loops(unknot_two_over_loops, poly_unknot):
    """An unknot with two loops that have the same crossing orientation."""
    sgd = unknot_two_over_loops()
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_one_over_one_under_loop(unknot_one_over_one_under_loop, poly_unknot):
    """An unknot with two loops that have opposing crossing orientations."""
    sgd = unknot_one_over_one_under_loop()
    assert sgd.yamada_polynomial() == poly_unknot