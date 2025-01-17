import pytest


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






