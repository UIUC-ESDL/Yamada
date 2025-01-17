"""
TODO Ensure Non-R1
TODO Reverse R1
"""

from cypari import pari
from yamada import SpatialGraphDiagram, Edge, Crossing, has_r1, apply_r1


# %% Unknots that do not have a Reidemeister 1 move


def test_r1_unknot_1e_1v(unknot_1e_1v):
    sgd = unknot_1e_1v(correct_diagram=True, simplify_diagram=True)
    sgd_has_r1 = has_r1(sgd)
    assert len(sgd_has_r1) == 0


def test_r1_unknot_2e_2v(unknot_2e_2v_1):
    sgd = unknot_2e_2v_1(correct_diagram=True, simplify_diagram=True)
    sgd_has_r1 = has_r1(sgd)
    assert len(sgd_has_r1) == 0


# %% Unknots that do have a Reidemeister 1 move


def test_r1_unknot_inf_cw_2e_0v_1c_1(unknot_inf_cw_2e_0v_1c_1, poly_unknot):
    sgd = unknot_inf_cw_2e_0v_1c_1
    sgd_has_r1 = has_r1(sgd)
    assert len(sgd_has_r1) == 1
    assert 'c1' in sgd_has_r1
    sgd_post_r1 = apply_r1(sgd, 'c1')
    assert sgd_post_r1.yamada_polynomial() == poly_unknot

def test_r1_unknot_inf_cw_4e_2v_1c_1(unknot_inf_cw_4e_2v_1c_1, poly_unknot):

    sgd = unknot_inf_cw_4e_2v_1c_1()

    assert sgd.yamada_polynomial() == poly_unknot

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 1
    assert 'c1' in r1_crossing_labels

    sgd = apply_r1(sgd, 'c1')

    assert sgd.yamada_polynomial() == poly_unknot


def test_r1_unknot_two_ccw_twists(unknot_two_ccw_twists, poly_unknot):

    sgd = unknot_two_ccw_twists()

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 2
    assert 'c1' in r1_crossing_labels and 'c2' in r1_crossing_labels

    sgd = apply_r1(sgd, 'c1')


    assert sgd.yamada_polynomial() == poly_unknot

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 1
    assert 'c2' in r1_crossing_labels

    sgd = apply_r1(sgd, 'c2')

    assert sgd.yamada_polynomial() == poly_unknot

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 0


def test_r1_unknot_one_ccw_one_cw_twist(unknot_one_ccw_one_cw_twist, poly_unknot):

    sgd = unknot_one_ccw_one_cw_twist()

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 2
    assert 'c1' in r1_crossing_labels and 'c2' in r1_crossing_labels

    sgd = apply_r1(sgd, 'c1')


    assert sgd.yamada_polynomial() == poly_unknot

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 1
    assert 'c2' in r1_crossing_labels

    sgd = apply_r1(sgd, 'c2')

    assert sgd.yamada_polynomial() == poly_unknot

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 0


def test_r1_unknot_unknot_two_ccw_twists(unknot_two_ccw_twists, poly_unknot):

    sgd = unknot_two_ccw_twists()

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 2
    assert 'c1' in r1_crossing_labels and 'c2' in r1_crossing_labels

    sgd = apply_r1(sgd, 'c1')

    assert sgd.yamada_polynomial() == poly_unknot

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 1
    assert 'c2' in r1_crossing_labels

    sgd = apply_r1(sgd, 'c2')

    assert sgd.yamada_polynomial() == poly_unknot

    r1_crossing_labels = has_r1(sgd)

    assert len(r1_crossing_labels) == 0



