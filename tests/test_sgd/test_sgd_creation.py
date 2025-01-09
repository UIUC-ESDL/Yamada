import pytest
from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing


# def test_unknot_1e(unknot_1e):
#     assert unknot_1e


def test_unknot_1e_1v(unknot_1e_1v):
    assert unknot_1e_1v


def test_unknot_2e_2v(unknot_2e_2v):
    assert unknot_2e_2v


def test_unknot_infinity_1c(unknot_infinity_1c):
    assert unknot_infinity_1c


# def test_unknot_infinity_1e_1c(unknot_infinity_1e_1c):
#     assert unknot_infinity_1e_1c


def test_unknot_infinity_1_2e_1c(unknot_infinity_1_2e_1c):
    assert unknot_infinity_1_2e_1c


def test_unknot_infinity_2_2e_1c(unknot_infinity_2_2e_1c):
    assert unknot_infinity_2_2e_1c


def test_unknot_infinity_1_4e_2v_1c(unknot_infinity_1_4e_2v_1c):
    assert unknot_infinity_1_4e_2v_1c

# def test_unknot_double_loop_same_4e_2c(unknot_double_loop_same_4e_2c):
#     assert unknot_double_loop_same_4e_2c
#
# def test_unknot_double_loop_opposite_4e_2c(unknot_double_loop_opposite_4e_2c):
#     """An unknot with two loops that have opposing crossing orientations."""
#     assert unknot_double_loop_opposite_4e_2c


def test_unknotted_theta_graph_1(unknotted_theta_graph_1):
    assert unknotted_theta_graph_1

