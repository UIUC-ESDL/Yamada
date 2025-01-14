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


def test_unknot_2e_0v(unknot_2e_0v, poly_unknot):
    """
    SGD should fix this by adding vertices to self-connected edges.
    """
    assert unknot_2e_0v
    assert len(unknot_2e_0v.vertices) == 2
    assert len(unknot_2e_0v.edges) == 2
    assert len(unknot_2e_0v.crossings) == 0
    assert unknot_2e_0v.edges[0].label == 'e1'
    assert unknot_2e_0v.edges[1].label == 'e2'
    assert unknot_2e_0v.vertices[0].label == 'v1'
    assert unknot_2e_0v.vertices[1].label == 'v2'
    assert unknot_2e_0v.yamada_polynomial() == poly_unknot

    # Simplify the graph
    unknot_2e_0v._simplify_graph()
    assert len(unknot_2e_0v.edges) == 1
    assert len(unknot_2e_0v.vertices) == 1
    assert unknot_2e_0v.edges[0].label == 'e1'
    assert unknot_2e_0v.vertices[0].label == 'v1'


def test_unknot_3e_0v(unknot_3e_0v, poly_unknot):
    assert unknot_3e_0v
    assert len(unknot_3e_0v.vertices) == 3
    assert len(unknot_3e_0v.edges) == 3
    assert len(unknot_3e_0v.crossings) == 0
    assert unknot_3e_0v.edges[0].label == 'e1'
    assert unknot_3e_0v.edges[1].label == 'e2'
    assert unknot_3e_0v.edges[2].label == 'e3'
    assert unknot_3e_0v.vertices[0].label == 'v1'
    assert unknot_3e_0v.vertices[1].label == 'v2'
    assert unknot_3e_0v.vertices[2].label == 'v3'
    assert unknot_3e_0v.yamada_polynomial() == poly_unknot


def test_unknot_0e_1v(unknot_0e_1v, poly_unknot):
    """
    SGD should fix this by adding edges to self-connected vertices.
    """
    assert unknot_0e_1v
    assert len(unknot_0e_1v.vertices) == 1
    assert len(unknot_0e_1v.edges) == 1
    assert len(unknot_0e_1v.crossings) == 0
    assert unknot_0e_1v.edges[0].label == 'e1'
    assert unknot_0e_1v.vertices[0].label == 'v1'
    assert unknot_0e_1v.yamada_polynomial() == poly_unknot


def test_unknot_1e_1v(unknot_1e_1v, poly_unknot):
    assert unknot_1e_1v
    assert len(unknot_1e_1v.vertices) == 1
    assert len(unknot_1e_1v.edges) == 1
    assert len(unknot_1e_1v.crossings) == 0
    assert unknot_1e_1v.edges[0].label == 'e1'
    assert unknot_1e_1v.vertices[0].label == 'v1'
    assert unknot_1e_1v.yamada_polynomial() == poly_unknot


def test_unknot_2e_1v(unknot_2e_1v, poly_unknot):
    assert unknot_2e_1v
    assert len(unknot_2e_1v.vertices) == 2
    assert len(unknot_2e_1v.edges) == 2
    assert len(unknot_2e_1v.crossings) == 0
    assert unknot_2e_1v.edges[0].label == 'e1'
    assert unknot_2e_1v.edges[1].label == 'e2'
    assert unknot_2e_1v.vertices[0].label == 'v1'
    assert unknot_2e_1v.vertices[1].label == 'v2'
    assert unknot_2e_1v.yamada_polynomial() == poly_unknot


def test_unknot_3e_1v(unknot_3e_1v, poly_unknot):
    assert unknot_3e_1v
    assert len(unknot_3e_1v.vertices) == 3
    assert len(unknot_3e_1v.edges) == 3
    assert len(unknot_3e_1v.crossings) == 0
    assert unknot_3e_1v.edges[0].label == 'e1'
    assert unknot_3e_1v.edges[1].label == 'e2'
    assert unknot_3e_1v.edges[2].label == 'e3'
    assert unknot_3e_1v.vertices[0].label == 'v1'
    assert unknot_3e_1v.vertices[1].label == 'v2'
    assert unknot_3e_1v.vertices[2].label == 'v3'
    assert unknot_3e_1v.yamada_polynomial() == poly_unknot


def test_unknot_0e_2v(unknot_0e_2v, poly_unknot):
    assert unknot_0e_2v
    assert len(unknot_0e_2v.edges) == 2
    assert len(unknot_0e_2v.vertices) == 2
    assert len(unknot_0e_2v.crossings) == 0
    assert unknot_0e_2v.edges[0].label == 'e1'
    assert unknot_0e_2v.edges[1].label == 'e2'
    assert unknot_0e_2v.vertices[0].label == 'v1'
    assert unknot_0e_2v.vertices[1].label == 'v2'
    assert unknot_0e_2v.yamada_polynomial() == poly_unknot


def test_unknot_1e_2v(unknot_1e_2v, poly_unknot):
    assert unknot_1e_2v
    assert len(unknot_1e_2v.vertices) == 2
    assert len(unknot_1e_2v.edges) == 2
    assert len(unknot_1e_2v.crossings) == 0
    assert unknot_1e_2v.edges[0].label == 'e1'
    assert unknot_1e_2v.edges[1].label == 'e2'
    assert unknot_1e_2v.vertices[0].label == 'v1'
    assert unknot_1e_2v.vertices[1].label == 'v2'
    assert unknot_1e_2v.yamada_polynomial() == poly_unknot


def test_unknot_2e_2v_1(unknot_2e_2v_1, poly_unknot):
    assert unknot_2e_2v_1
    assert len(unknot_2e_2v_1.vertices) == 2
    assert len(unknot_2e_2v_1.edges) == 2
    assert len(unknot_2e_2v_1.crossings) == 0
    assert unknot_2e_2v_1.edges[0].label == 'e1'
    assert unknot_2e_2v_1.edges[1].label == 'e2'
    assert unknot_2e_2v_1.vertices[0].label == 'v1'
    assert unknot_2e_2v_1.vertices[1].label == 'v2'
    assert unknot_2e_2v_1.yamada_polynomial() == poly_unknot


def test_unknot_2e_2v_2(unknot_2e_2v_2, poly_unknot):
    """
    Completes SGD by inserting a vertex between the two edges.
    And an edge between the two vertices.
    """
    assert unknot_2e_2v_2
    assert len(unknot_2e_2v_2.vertices) == 3
    assert len(unknot_2e_2v_2.edges) == 3
    assert len(unknot_2e_2v_2.crossings) == 0
    assert unknot_2e_2v_2.edges[0].label == 'e1'
    assert unknot_2e_2v_2.edges[1].label == 'e2'
    assert unknot_2e_2v_2.edges[2].label == 'e3'
    assert unknot_2e_2v_2.vertices[0].label == 'v1'
    assert unknot_2e_2v_2.vertices[1].label == 'v2'
    assert unknot_2e_2v_2.vertices[2].label == 'v3'
    assert unknot_2e_2v_2.yamada_polynomial() == poly_unknot


def test_unknot_3e_2v_1(unknot_3e_2v_1, poly_unknot):
    """
    Completes SGD by inserting an edge between the two vertices.
    """
    assert unknot_3e_2v_1
    assert len(unknot_3e_2v_1.vertices) == 4
    assert len(unknot_3e_2v_1.edges) == 4
    assert len(unknot_3e_2v_1.crossings) == 0
    assert unknot_3e_2v_1.edges[0].label == 'e1'
    assert unknot_3e_2v_1.edges[1].label == 'e2'
    assert unknot_3e_2v_1.edges[2].label == 'e3'
    assert unknot_3e_2v_1.edges[3].label == 'e4'
    assert unknot_3e_2v_1.vertices[0].label == 'v1'
    assert unknot_3e_2v_1.vertices[1].label == 'v2'
    assert unknot_3e_2v_1.vertices[2].label == 'v3'
    assert unknot_3e_2v_1.vertices[3].label == 'v4'
    assert unknot_3e_2v_1.yamada_polynomial() == poly_unknot


def test_unknot_3e_2v_2(unknot_3e_2v_2, poly_unknot):
    """
    Completes SGD by inserting two edge between the three vertices.
    And a vertex between the two edges.
    """
    assert unknot_3e_2v_2
    assert len(unknot_3e_2v_2.vertices) == 3
    assert len(unknot_3e_2v_2.edges) == 3
    assert len(unknot_3e_2v_2.crossings) == 0
    assert unknot_3e_2v_2.edges[0].label == 'e1'
    assert unknot_3e_2v_2.edges[1].label == 'e2'
    assert unknot_3e_2v_2.edges[2].label == 'e3'
    assert unknot_3e_2v_2.vertices[0].label == 'v1'
    assert unknot_3e_2v_2.vertices[1].label == 'v2'
    assert unknot_3e_2v_2.vertices[2].label == 'v3'
    assert unknot_3e_2v_2.yamada_polynomial() == poly_unknot


def test_unknot_0e_3v(unknot_0e_3v, poly_unknot):
    """
    Completes SGD by inserting an edge between the three vertices.
    """
    assert unknot_0e_3v
    assert len(unknot_0e_3v.vertices) == 3
    assert len(unknot_0e_3v.edges) == 3
    assert len(unknot_0e_3v.crossings) == 0
    assert unknot_0e_3v.edges[0].label == 'e1'
    assert unknot_0e_3v.edges[1].label == 'e2'
    assert unknot_0e_3v.edges[2].label == 'e3'
    assert unknot_0e_3v.vertices[0].label == 'v1'
    assert unknot_0e_3v.vertices[1].label == 'v2'
    assert unknot_0e_3v.vertices[2].label == 'v3'
    assert unknot_0e_3v.yamada_polynomial() == poly_unknot


def test_1e_3v(unknot_1e_3v, poly_unknot):
    """
    Completes SGD by inserting an edge between the three vertices.
    """
    assert unknot_1e_3v
    assert len(unknot_1e_3v.vertices) == 3
    assert len(unknot_1e_3v.edges) == 3
    assert len(unknot_1e_3v.crossings) == 0
    assert unknot_1e_3v.edges[0].label == 'e1'
    assert unknot_1e_3v.edges[1].label == 'e2'
    assert unknot_1e_3v.edges[2].label == 'e3'
    assert unknot_1e_3v.vertices[0].label == 'v1'
    assert unknot_1e_3v.vertices[1].label == 'v2'
    assert unknot_1e_3v.vertices[2].label == 'v3'
    assert unknot_1e_3v.yamada_polynomial() == poly_unknot


def test_unknot_2e_3v_1(unknot_2e_3v_1, poly_unknot):
    """
    Completes SGD by inserting an edge between the two vertices.
    """
    assert unknot_2e_3v_1
    assert len(unknot_2e_3v_1.vertices) == 3
    assert len(unknot_2e_3v_1.edges) == 3
    assert len(unknot_2e_3v_1.crossings) == 0
    assert unknot_2e_3v_1.edges[0].label == 'e1'
    assert unknot_2e_3v_1.edges[1].label == 'e2'
    assert unknot_2e_3v_1.edges[2].label == 'e3'
    assert unknot_2e_3v_1.vertices[0].label == 'v1'
    assert unknot_2e_3v_1.vertices[1].label == 'v2'
    assert unknot_2e_3v_1.vertices[2].label == 'v3'
    assert unknot_2e_3v_1.yamada_polynomial() == poly_unknot


def test_unknot_2e_3v_2(unknot_2e_3v_2, poly_unknot):
    """
    Completes SGD by inserting an edge between the two vertices.
    And inserting edges between the three vertices.
    """
    assert unknot_2e_3v_2
    assert len(unknot_2e_3v_2.vertices) == 4
    assert len(unknot_2e_3v_2.edges) == 4
    assert len(unknot_2e_3v_2.crossings) == 0
    assert unknot_2e_3v_2.edges[0].label == 'e1'
    assert unknot_2e_3v_2.edges[1].label == 'e2'
    assert unknot_2e_3v_2.edges[2].label == 'e3'
    assert unknot_2e_3v_2.edges[3].label == 'e4'
    assert unknot_2e_3v_2.vertices[0].label == 'v1'
    assert unknot_2e_3v_2.vertices[1].label == 'v2'
    assert unknot_2e_3v_2.vertices[2].label == 'v3'
    assert unknot_2e_3v_2.vertices[3].label == 'v4'
    assert unknot_2e_3v_2.yamada_polynomial() == poly_unknot


def test_3e_3v_1(unknot_3e_3v_1, poly_unknot):
    assert unknot_3e_3v_1
    assert len(unknot_3e_3v_1.vertices) == 3
    assert len(unknot_3e_3v_1.edges) == 3
    assert len(unknot_3e_3v_1.crossings) == 0
    assert unknot_3e_3v_1.edges[0].label == 'e1'
    assert unknot_3e_3v_1.edges[1].label == 'e2'
    assert unknot_3e_3v_1.edges[2].label == 'e3'
    assert unknot_3e_3v_1.vertices[0].label == 'v1'
    assert unknot_3e_3v_1.vertices[1].label == 'v2'
    assert unknot_3e_3v_1.vertices[2].label == 'v3'
    assert unknot_3e_3v_1.yamada_polynomial() == poly_unknot


def test_3e_3v_2(unknot_3e_3v_2, poly_unknot):
    assert unknot_3e_3v_2
    assert len(unknot_3e_3v_2.vertices) == 5
    assert len(unknot_3e_3v_2.edges) == 5
    assert len(unknot_3e_3v_2.crossings) == 0
    assert unknot_3e_3v_2.edges[0].label == 'e1'
    assert unknot_3e_3v_2.edges[1].label == 'e2'
    assert unknot_3e_3v_2.edges[2].label == 'e3'
    assert unknot_3e_3v_2.edges[3].label == 'e4'
    assert unknot_3e_3v_2.edges[4].label == 'e5'
    assert unknot_3e_3v_2.vertices[0].label == 'v1'
    assert unknot_3e_3v_2.vertices[1].label == 'v2'
    assert unknot_3e_3v_2.vertices[2].label == 'v3'
    assert unknot_3e_3v_2.vertices[3].label == 'v4'
    assert unknot_3e_3v_2.vertices[4].label == 'v5'
    assert unknot_3e_3v_2.yamada_polynomial() == poly_unknot


def test_3e_3v_3(unknot_3e_3v_3, poly_unknot):
    assert unknot_3e_3v_3
    assert len(unknot_3e_3v_3.vertices) == 4
    assert len(unknot_3e_3v_3.edges) == 4
    assert len(unknot_3e_3v_3.crossings) == 0
    assert unknot_3e_3v_3.edges[0].label == 'e1'
    assert unknot_3e_3v_3.edges[1].label == 'e2'
    assert unknot_3e_3v_3.edges[2].label == 'e3'
    assert unknot_3e_3v_3.edges[3].label == 'e4'
    assert unknot_3e_3v_3.vertices[0].label == 'v1'
    assert unknot_3e_3v_3.vertices[1].label == 'v2'
    assert unknot_3e_3v_3.vertices[2].label == 'v3'
    assert unknot_3e_3v_3.vertices[3].label == 'v4'
    assert unknot_3e_3v_3.yamada_polynomial() == poly_unknot





