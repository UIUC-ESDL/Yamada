def test_unknot_0e_0v(unknot_0e_0v, poly_empty):
    # Not actually unknot--an empty diagram.
    assert unknot_0e_0v
    assert unknot_0e_0v.yamada_polynomial() == poly_empty



def test_unknot_1e_0v(unknot_1e_0v, poly_unknot):
    """
    SGD should fix this by adding vertices to self-connected edges.
    """
    assert unknot_1e_0v
    assert len(unknot_1e_0v.vertices) == 1
    assert len(unknot_1e_0v.edges) == 1
    assert len(unknot_1e_0v.crossings) == 0
    assert unknot_1e_0v.edges[0].label == 'e1'
    assert unknot_1e_0v.vertices[0].label == 'v1'
    assert unknot_1e_0v.yamada_polynomial() == poly_unknot


def test_unknot_0e_1v(unknot_0e_1v, poly_unknot):
    """
    SGD should fix this by adding vertices to self-connected edges.
    """
    assert unknot_0e_1v
    assert len(unknot_0e_1v.vertices) == 1
    assert len(unknot_0e_1v.edges) == 1
    assert len(unknot_0e_1v.crossings) == 0
    assert unknot_0e_1v.edges[0].label == 'e1'
    assert unknot_0e_1v.vertices[0].label == 'v1'
    assert unknot_0e_1v.yamada_polynomial() == poly_unknot


def test_unknot_1e_1v(unknot_1e_1v):
    assert unknot_1e_1v


def test_unknot_2e_2v(unknot_2e_2v):
    assert unknot_2e_2v








