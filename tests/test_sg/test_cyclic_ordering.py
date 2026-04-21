import numpy as np
import pytest
from yamada import SpatialGraph


def test_edge_endpoint_must_be_declared_node():
    with pytest.raises(AssertionError, match="not in nodes"):
        SpatialGraph(nodes=['a'],
                     pos={'a': (0, 0, 0)},
                     edges=[('a', 'b')])


def test_self_loop_requires_explicit_intermediate_vertices():
    with pytest.raises(AssertionError, match="Self-loop edges"):
        SpatialGraph(nodes=['a'],
                     pos={'a': (0, 0, 0)},
                     edges=[('a', 'a')])


def test_reversed_duplicate_edges_are_preserved_as_parallel_edges():
    sg = SpatialGraph(nodes=['a', 'b'],
                      pos={'a': (0, 0, 0), 'b': (1, 0, 0)},
                      edges=[('a', 'b'), ('b', 'a')],
                      rotation=np.array([0.0, 0.0, 0.0]))
    sgd = sg.to_spatial_graph_diagram()

    assert sg.G.number_of_edges('a', 'b') == 2
    assert len(sgd.edges) == 2
    assert sgd.graph().number_of_edges() == 2


def test_exact_duplicate_edges_are_preserved_as_parallel_edges():
    sg = SpatialGraph(nodes=['a', 'b'],
                      pos={'a': (0, 0, 0), 'b': (1, 0, 0)},
                      edges=[('a', 'b'), ('a', 'b')],
                      rotation=np.array([0.0, 0.0, 0.0]))
    sgd = sg.to_spatial_graph_diagram()

    assert sg.G.number_of_edges('a', 'b') == 2
    assert len(sgd.edges) == 2
    assert sgd.graph().number_of_edges() == 2


def test_node_label_containing_crossing_converts_to_diagram():
    nodes = ['crossing_anchor', 'b', 'c']
    pos = {
        'crossing_anchor': (0, 0, 0),
        'b': (1, 0, 0),
        'c': (0, 0, 1),
    }
    edges = [('crossing_anchor', 'b'), ('b', 'c'), ('c', 'crossing_anchor')]

    sg = SpatialGraph(nodes=nodes,
                      pos=pos,
                      edges=edges,
                      rotation=np.array([0.0, 0.0, 0.0]))
    sgd = sg.to_spatial_graph_diagram()

    assert len(sgd.vertices) == 3
    assert len(sgd.crossings) == 0


def test_cyclic_node_ordering_vertex():
    nodes = ['v_a', 'v_b', 'v_c', 'v_d', 'v_e', 'v_f', 'v_g', 'v_h']

    pos = {'v_a': (0, 0, 0), 'v_b': (1, 0, 0), 'v_c': (0.5, 1, 0), 'v_d': (0.5, 0.5, 0), 'v_e': (0.25, 0.75, 0),
                      'v_f': (0.75, 0.75, 0), 'v_g': (0, 1, 0), 'v_h': (1, 1, 0)}

    edges = [('v_a', 'v_b'), ('v_a', 'v_g'), ('v_a', 'v_d'), ('v_b', 'v_d'), ('v_b', 'v_h'), ('v_d', 'v_e'),
             ('v_d', 'v_f'), ('v_e', 'v_c'), ('v_f', 'v_c'), ('v_g', 'v_c'), ('v_h', 'v_c')]

    # Use a predefined rotation (from a random seed) that previously produced an error
    rotation = np.array([3.44829694, 4.49366732, 3.78727399])

    sg = SpatialGraph(nodes=nodes,
                      pos=pos,
                      edges=edges,
                      rotation=rotation)

    order = sg.ccw_orderings['v_c']
    expected_order = {'v_e': 1, 'v_f': 2, 'v_g': 0, 'v_h': 3}

    assert order == expected_order


def test_cyclic_ordering_crossing():
    """
    See ./figures_cyclic_ordering/test_cyclic_ordering_crossing.png
    """
    component_a = 'v_a'
    component_b = 'v_b'
    component_c = 'v_c'
    component_d = 'v_d'
    component_e = 'v_e'
    component_f = 'v_f'
    component_g = 'v_g'
    component_h = 'v_h'

    waypoint_ab = 'w_ab'
    waypoint_ad = 'w_ad'
    waypoint_ae = 'w_ae'
    waypoint_bc = 'w_bc'
    waypoint_bf = 'w_bf'
    waypoint_cd = 'w_cd'
    waypoint_cg = 'w_cg'
    waypoint_dh = 'w_dh'
    waypoint_ef = 'w_ef'
    waypoint_eh = 'w_eh'
    waypoint_fg = 'w_fg'
    waypoint_gh = 'w_gh'

    nodes = [component_a, component_b, component_c, component_d, component_e, component_f,
             component_g, component_h, waypoint_ab, waypoint_ad, waypoint_ae, waypoint_bc,
             waypoint_bf, waypoint_cd, waypoint_cg, waypoint_dh, waypoint_ef, waypoint_eh,
             waypoint_fg, waypoint_gh]

    component_positions = [(0, 0, 0),  # a
                                (1, 0, 0),  # b
                                (1, 1, 0),  # c
                                (0, 1, 0),  # d
                                (0, 0, 1),  # e
                                (1, 0, 1),  # f
                                (1, 1, 1),  # g
                                (0, 1, 1)]  # h

    waypoint_positions = [(0.5, 0, 0),  # ab
                               (0, 0.5, 0),  # ad
                               (0, 0, 0.5),  # ae
                               (1, 0.5, 0),  # bc
                               (1, 0, 0.5),  # bf
                               (0.5, 1, 0),  # cd
                               (1, 1, 0.5),  # cg
                               (0, 1, 0.5),  # dh
                               (0.5, 0, 1),  # ef
                               (0, 0.5, 1),  # eh
                               (1, 0.5, 1),  # fg
                               (0.5, 1, 1)]  # gh

    pos = (component_positions + waypoint_positions)

    pos = {node: pos for node, pos in zip(nodes, pos)}

    edges = [(component_a, waypoint_ab), (waypoint_ab, component_b),
         (component_a, waypoint_ad), (waypoint_ad, component_d),
         (component_a, waypoint_ae), (waypoint_ae, component_e),
         (component_b, waypoint_bc), (waypoint_bc, component_c),
         (component_b, waypoint_bf), (waypoint_bf, component_f),
         (component_c, waypoint_cd), (waypoint_cd, component_d),
         (component_c, waypoint_cg), (waypoint_cg, component_g),
         (component_d, waypoint_dh), (waypoint_dh, component_h),
         (component_e, waypoint_ef), (waypoint_ef, component_f),
         (component_e, waypoint_eh), (waypoint_eh, component_h),
         (component_f, waypoint_fg), (waypoint_fg, component_g),
         (component_g, waypoint_gh), (waypoint_gh, component_h)]

    # Define the random rotation that previously caused issues
    rotation = np.array([3.44829694, 4.49366732, 3.78727399])

    sg = SpatialGraph(nodes=nodes,
                      pos=pos,
                      edges=edges,
                      rotation=rotation)

    ordering_dict = sg.ccw_orderings

    expected_dict = {'crossing_0': {'v_c': 0, 'w_ef': 1, 'w_bc': 2, 'v_f': 3},
                     'crossing_1': {'w_cd': 0, 'w_eh': 1, 'v_d': 2, 'v_e': 3}}

    for k, v in expected_dict.items():
        assert ordering_dict[k] == v, f"Mismatch at {k}: expected {v}, got {ordering_dict[k]}"


def test_cyclic_ordering_crossing_2():
    """
    See ./figures_cyclic_ordering/test_cyclic_ordering_crossing_2.png
    """
    component_a = 'v_a'
    component_b = 'v_b'
    component_c = 'v_c'
    component_d = 'v_d'
    component_e = 'v_e'
    component_f = 'v_f'
    component_g = 'v_g'
    component_h = 'v_h'

    waypoint_ab = 'w_ab'
    waypoint_ad = 'w_ad'
    waypoint_ae = 'w_ae'
    waypoint_bc = 'w_bc'
    waypoint_bf = 'w_bf'
    waypoint_cd = 'w_cd'
    waypoint_cg = 'w_cg'
    waypoint_dh = 'w_dh'
    waypoint_ef = 'w_ef'
    waypoint_eh = 'w_eh'
    waypoint_fg = 'w_fg'
    waypoint_gh = 'w_gh'

    nodes = [component_a, component_b, component_c, component_d, component_e, component_f,
             component_g, component_h, waypoint_ab, waypoint_ad, waypoint_ae, waypoint_bc,
             waypoint_bf, waypoint_cd, waypoint_cg, waypoint_dh, waypoint_ef, waypoint_eh,
             waypoint_fg, waypoint_gh]

    component_positions = [(0, 0, 0),  # a
                                    (1, 0, 0),  # b
                                    (1, 1, 0),  # c
                                    (0, 1, 0),  # d
                                    (0, 0, 1),  # e
                                    (1, 0, 1),  # f
                                    (1, 1, 1),  # g
                                    (0, 1, 1)]  # h

    waypoint_positions = [(0.5, 0.1, 0),  # ab
                                   (0.1, 0.7, 0.2),  # ad
                                   (0.1, 0, 0.5),  # ae
                                   (1, 0.5, 0),  # bc
                                   (1, 0.1, 0.5),  # bf
                                   (0.5, 1, 0),  # cd
                                   (0.7, 0.6, 0.5),  # cg
                                   (0.1, 1, 0.5),  # dh
                                   (0.5, 0.1, 1),  # ef
                                   (0.1, 0.6, 1),  # eh
                                   (1, 0.5, 1),  # fg
                                   (0.5, 0.95, 1)]  # gh


    pos = (component_positions + waypoint_positions)

    pos = {node: pos for node, pos in zip(nodes, pos)}

    edges = [(component_a, waypoint_ab), (waypoint_ab, component_b),
             (component_a, waypoint_ad), (waypoint_ad, component_d),
             (component_a, waypoint_ae), (waypoint_ae, component_e),
             (component_b, waypoint_bc), (waypoint_bc, component_c),
             (component_b, waypoint_bf), (waypoint_bf, component_f),
             (component_c, waypoint_cd), (waypoint_cd, component_d),
             (component_c, waypoint_cg), (waypoint_cg, component_g),
             (component_d, waypoint_dh), (waypoint_dh, component_h),
             (component_e, waypoint_ef), (waypoint_ef, component_f),
             (component_e, waypoint_eh), (waypoint_eh, component_h),
             (component_f, waypoint_fg), (waypoint_fg, component_g),
             (component_g, waypoint_gh), (waypoint_gh, component_h)]

    # Set rotation
    rotation = np.array([2.73943676, 0.16289932, 3.4536312])

    sg = SpatialGraph(nodes=nodes,
                      pos=pos,
                      edges=edges,
                      rotation=rotation)

    ordering_dict = sg.ccw_orderings

    expected_dict = {'crossing_0': {'v_a': 3, 'v_d': 0, 'w_ab': 1, 'w_dh': 2},
                     'crossing_1': {'v_b': 3, 'v_c': 0, 'crossing_2': 1, 'w_cg': 2},
                     'crossing_2': {'w_cg': 2, 'crossing_1': 3, 'v_g': 0, 'w_bf': 1},
                     'crossing_3': {'w_gh': 0, 'w_bf': 1, 'v_g': 2, 'v_f': 3}}

    for k, v in expected_dict.items():
        assert ordering_dict[k] == v, f"Mismatch at {k}: expected {v}, got {ordering_dict[k]}"
