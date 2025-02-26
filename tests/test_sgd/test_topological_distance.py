"""
poly_unknot
unknot_2e_2v_1
unknot_inf_cw_0e_0v_1c
figure_8, double_figure_8
"""

import pytest
from yamada.sgd.topological_distance import compute_min_distance


def test_top_dist_unknot(unknot_2e_2v_1, unknot_inf_cw_0e_0v_1c, poly_unknot):
    top_dist_1, _ = compute_min_distance(unknot_2e_2v_1(), unknot_inf_cw_0e_0v_1c(), 2, 10)
    top_dist_2, _ = compute_min_distance(unknot_inf_cw_0e_0v_1c(), unknot_2e_2v_1(), 2, 10)
    assert top_dist_1 == 0
    assert top_dist_2 == 0


def test_top_dist_unknot_figure_8(unknot_2e_2v_1, figure_8):
    top_dist_1, _ = compute_min_distance(unknot_2e_2v_1(), figure_8, 2, 10)
    top_dist_2, _ = compute_min_distance(figure_8, unknot_2e_2v_1(), 2, 10)
    assert top_dist_1 == 1
    assert top_dist_2 == 1


def test_top_dist_figure_8(figure_8):
    top_dist, _ = compute_min_distance(figure_8, figure_8, 2, 10)
    assert top_dist == 0


def test_top_dist_double_figure_8(double_figure_8):
    top_dist, _ = compute_min_distance(double_figure_8, double_figure_8, 2, 10)
    assert top_dist == 0


def test_top_dist_mixed(unknot_2e_2v_1, figure_8, double_figure_8):
    top_dist_1, _ = compute_min_distance(figure_8, double_figure_8, 2, 10)
    top_dist_2, _ = compute_min_distance(double_figure_8, figure_8, 2, 10)
    top_dist_3, _ = compute_min_distance(unknot_2e_2v_1(), double_figure_8, 2, 10)
    top_dist_4, _ = compute_min_distance(double_figure_8, unknot_2e_2v_1(), 2, 10)
    assert top_dist_1 == 1
    assert top_dist_2 == 1
    assert top_dist_3 == 2
    assert top_dist_4 == 2
