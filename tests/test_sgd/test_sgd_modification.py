import pytest
from yamada import SpatialGraphDiagram, Vertex, Edge


def test_copy(unknot_inf_cw_4e_2v_1c_1):
    """Ensures that the copy method creates a completely new object."""
    sgd = unknot_inf_cw_4e_2v_1c_1()
    edges = sgd.edges
    vertices = sgd.vertices
    crossings = sgd.crossings

    copy_sgd = sgd.copy()
    copy_edges = copy_sgd.edges
    copy_vertices = copy_sgd.vertices
    copy_crossings = copy_sgd.crossings

    assert sgd is not copy_sgd

    for edge, copy_edge in zip(edges, copy_edges):
        assert edge is not copy_edge

    for vertex, copy_vertex in zip(vertices, copy_vertices):
        assert vertex is not copy_vertex

    for crossing, copy_crossing in zip(crossings, copy_crossings):
        assert crossing is not copy_crossing


def test_standardize_labels_rebuilds_data_after_renumbering():
    e2 = Edge('e2')
    e1 = Edge('e1')
    v_a = Vertex(1, 'a')
    v_b = Vertex(2, 'b')
    v_c = Vertex(1, 'c')

    v_a[0] = e2[0]
    v_b[0] = e2[1]
    v_b[1] = e1[0]
    v_c[0] = e1[1]

    sgd = SpatialGraphDiagram(edges=[e2, e1],
                              vertices=[v_a, v_b, v_c],
                              correct_diagram=False)

    assert set(sgd.data) == {'e1', 'e2', 'v1', 'v2', 'v3'}
    assert sgd.data['e1'] is sgd.edges[0]
    assert sgd.data['e2'] is sgd.edges[1]


def test_labels_must_be_globally_unique():
    e1 = Edge('x')
    v1 = Vertex(1, 'x')
    v2 = Vertex(1, 'v2')
    v1[0] = e1[0]
    v2[0] = e1[1]

    with pytest.raises(ValueError, match="Labels must be unique"):
        SpatialGraphDiagram(edges=[e1], vertices=[v1, v2])


def test_copy_with_standardize_labels_false_has_counters():
    e1 = Edge('custom_edge')
    v1 = Vertex(1, 'left')
    v2 = Vertex(1, 'right')
    v1[0] = e1[0]
    v2[0] = e1[1]

    sgd = SpatialGraphDiagram(edges=[e1],
                              vertices=[v1, v2],
                              standardize_labels=False)
    copy_sgd = sgd.copy()

    assert copy_sgd.edge_counter == sgd.edge_counter
    assert copy_sgd.vertex_counter == sgd.vertex_counter
    assert copy_sgd.crossing_counter == sgd.crossing_counter


def test_merge_edges(unknot_3e_3v_1, poly_unknot):

    sgd_1 = unknot_3e_3v_1(correct_diagram=True, simplify_diagram=False)
    sgd_2 = sgd_1.copy()
    sgd_3 = sgd_1.copy()
    sgd_4 = sgd_1.copy()

    # Try merging adjacent edges
    sgd_2._merge_edges(sgd_2.edges[0], sgd_2.edges[1])
    assert len(sgd_2.edges) == 2
    assert len(sgd_2.vertices) == 2
    assert sgd_2.edges[0].label == 'e1'
    assert sgd_2.edges[1].label == 'e3'
    assert sgd_2.vertices[0].label == 'v1'
    assert sgd_2.vertices[1].label == 'v3'
    assert sgd_2.yamada_polynomial() == poly_unknot

    # Try merging adjacent edges, but in reverse order (should correctly keep lower index)
    sgd_3._merge_edges(sgd_3.edges[1], sgd_3.edges[0])
    assert len(sgd_3.edges) == 2
    assert len(sgd_3.vertices) == 2
    assert sgd_3.edges[0].label == 'e1'
    assert sgd_3.edges[1].label == 'e3'
    assert sgd_3.vertices[0].label == 'v1'
    assert sgd_3.vertices[1].label == 'v3'
    assert sgd_3.yamada_polynomial() == poly_unknot

    # TODO Implement
    # Try merging non-adjacent edges (should raise error)
    # with pytest.raises(ValueError):
    #     sgd_4._merge_edges(sgd_4.edges[0], sgd_4.edges[2]) (This is not a valid test)






