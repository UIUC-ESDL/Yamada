import numpy as np
from yamada import SpatialGraph
from yamada.sgd.sgd_analysis import edges_form_a_strand


# %% Strands


def test_forms_a_strand_unknot_1e_1v(unknot_1e_1v):
    sgd = unknot_1e_1v(correct_diagram=False, simplify_diagram=False)
    e1 = sgd.edges[0]
    v1 = sgd.vertices[0]
    forms_a_strand = edges_form_a_strand(e1, e1)
    assert forms_a_strand is True


def test_forms_a_strand_unknot_1e_2v(unknot_2e_2v_1):
    sgd = unknot_2e_2v_1(correct_diagram=False, simplify_diagram=False)
    e1, e2 = sgd.edges
    forms_a_strand = edges_form_a_strand(e1, e2)
    assert forms_a_strand is True


# def test_forms_a_strand_unknot_inf_1_2e_1c(unknot_inf_cw_2e_0v_1c_1):
#     # TODO Fix logic for all cases...
#     sgd = unknot_inf_cw_2e_0v_1c_1(correct_diagram=False, simplify_diagram=False)
#     e1, e2 = sgd.edges
#     c1 = sgd.crossings[0]
#
#     check_1 = edges_form_a_strand(e1, e1)
#     assert check_1 is True
#
#     check_2 = edges_form_a_strand(e2, e2)
#     assert check_2 is True
#
#     check_3 = edges_form_a_strand(e1, e2)
#     assert check_3 is False
#
#     check_4 = edges_form_a_strand(e2, e1)
#     assert check_4 is False
#
#     # TODO Implement this (both arguments must be edges)
#     # check_5 = edges_form_a_strand(e1, c1)
#     # assert check_5 is False
#     # check_6 = edges_form_a_strand(e2, c1)
#     # assert check_6 is False


# def test_forms_a_strand_unknot_infinity_1_4e_2v_1c(unknot_infinity_1_4e_2v_1c):
#     e1, e2, e3, e4 = unknot_infinity_1_4e_2v_1c.edges
#     v1, v2 = unknot_infinity_1_4e_2v_1c.vertices
#     c1 = unknot_infinity_1_4e_2v_1c.crossings[0]
#
#     check_1 = edges_form_a_strand(e1, e1)
#     assert check_1 is True
#
#     check_2 = edges_form_a_strand(e1, e3)
#     assert check_2 is True
#
#     check_3 = edges_form_a_strand(e1, e4)
#     assert check_3 is False







def test_get_sub_edges():

    # Set rotation
    rotation = np.array([3.44829694, 4.49366732, 3.78727399])

    sg = SpatialGraph(nodes=['a', 'b', 'c', 'd'],
                      node_positions={'a':[0, 0.5, 0],
                                      'b': [1, 0.5, 1],
                                      'c': [1, 0, 0],
                                      'd': [0, 0, 1]},
                      edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a')],
                      rotation=rotation)

    sep = sg.get_sub_edges()

    expected_sub_edges = [('b', 'crossing_0'), ('crossing_0', 'a'), ('b', 'c'), ('d', 'crossing_0'), ('crossing_0', 'c'), ('d', 'a')]

    assert sep == expected_sub_edges

# def test_edge_order():
#
        # TODO Implement this

#         np.random.seed(0)
#
#         sg = SpatialGraph(nodes=['a', 'b', 'c', 'd'],
#                         node_positions=np.array([[0, 0.5, 0], [1, 0.5, 1], [1, 0, 0], [0, 0, 1]]),
#                         edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a')])
#
#         edge_0 = sg.edges[0]
#
#         vertices_and_crossings = sg.get_vertices_and_crossings_of_edge(edge_0)
#
#         edge_order = [vertices_and_crossings[i][0] < vertices_and_crossings[i+1][0] for i in range(len(vertices_and_crossings)-1)]
#
#         assert all(edge_order)