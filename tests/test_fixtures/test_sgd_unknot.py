def test_unknot_0e_0v(unknot_0e_0v, poly_empty):
    # Not actually unknot--an empty diagram.
    sgd = unknot_0e_0v
    assert sgd
    assert sgd.yamada_polynomial() == poly_empty

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 0
    assert len(sgd.vertices) == 0
    assert len(sgd.crossings) == 0
    assert sgd.yamada_polynomial() == poly_empty



def test_unknot_1e_0v(unknot_1e_0v, poly_unknot):
    """
    SGD should fix this by adding vertices to self-connected edges.
    """
    sgd = unknot_1e_0v
    assert sgd
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_2e_0v(unknot_2e_0v, poly_unknot):
    """
    SGD should fix this by adding vertices to self-connected edges.
    """
    sgd = unknot_2e_0v
    assert sgd
    assert len(sgd.vertices) == 2
    assert len(sgd.edges) == 2
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_3e_0v(unknot_3e_0v, poly_unknot):
    sgd = unknot_3e_0v
    assert sgd
    assert len(sgd.vertices) == 3
    assert len(sgd.edges) == 3
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.edges[2].label == 'e3'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.vertices[2].label == 'v3'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_0e_1v(unknot_0e_1v, poly_unknot):
    """
    SGD should fix this by adding edges to self-connected vertices.
    """
    sgd = unknot_0e_1v
    assert sgd
    assert len(sgd .vertices) == 1
    assert len(sgd .edges) == 1
    assert len(sgd .crossings) == 0
    assert sgd .edges[0].label == 'e1'
    assert sgd .vertices[0].label == 'v1'
    assert sgd .yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_1e_1v(unknot_1e_1v, poly_unknot):
    sgd = unknot_1e_1v
    assert sgd
    assert len(sgd.vertices) == 1
    assert len(sgd.edges) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_2e_1v(unknot_2e_1v, poly_unknot):
    sgd = unknot_2e_1v
    assert sgd
    assert len(sgd.vertices) == 2
    assert len(sgd.edges) == 2
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_3e_1v(unknot_3e_1v, poly_unknot):
    sgd = unknot_3e_1v
    assert sgd
    assert len(sgd.vertices) == 3
    assert len(sgd.edges) == 3
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.edges[2].label == 'e3'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.vertices[2].label == 'v3'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_0e_2v(unknot_0e_2v, poly_unknot):
    sgd = unknot_0e_2v
    assert sgd
    assert len(sgd.edges) == 2
    assert len(sgd.vertices) == 2
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_1e_2v(unknot_1e_2v, poly_unknot):
    sgd = unknot_1e_2v
    assert sgd
    assert len(sgd.vertices) == 2
    assert len(sgd.edges) == 2
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_2e_2v_1(unknot_2e_2v_1, poly_unknot):
    sgd = unknot_2e_2v_1
    assert sgd
    assert len(sgd.vertices) == 2
    assert len(sgd.edges) == 2
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_2e_2v_2(unknot_2e_2v_2, poly_unknot):
    """
    Completes SGD by inserting a vertex between the two edges.
    And an edge between the two vertices.
    """
    sgd = unknot_2e_2v_2
    assert sgd
    assert len(sgd.vertices) == 3
    assert len(sgd.edges) == 3
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.edges[2].label == 'e3'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.vertices[2].label == 'v3'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_3e_2v_1(unknot_3e_2v_1, poly_unknot):
    """
    Completes SGD by inserting an edge between the two vertices.
    """
    sgd = unknot_3e_2v_1
    assert sgd
    assert len(sgd.vertices) == 4
    assert len(sgd.edges) == 4
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.edges[2].label == 'e3'
    assert sgd.edges[3].label == 'e4'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.vertices[2].label == 'v3'
    assert sgd.vertices[3].label == 'v4'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_3e_2v_2(unknot_3e_2v_2, poly_unknot):
    """
    Completes SGD by inserting two edge between the three vertices.
    And a vertex between the two edges.
    """
    sgd = unknot_3e_2v_2
    assert sgd
    assert len(sgd.vertices) == 3
    assert len(sgd.edges) == 3
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.edges[2].label == 'e3'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.vertices[2].label == 'v3'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_0e_3v(unknot_0e_3v, poly_unknot):
    """
    Completes SGD by inserting an edge between the three vertices.
    """
    sgd = unknot_0e_3v
    assert sgd
    assert len(sgd.vertices) == 3
    assert len(sgd.edges) == 3
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.edges[2].label == 'e3'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.vertices[2].label == 'v3'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_1e_3v(unknot_1e_3v, poly_unknot):
    """
    Completes SGD by inserting an edge between the three vertices.
    """
    sgd = unknot_1e_3v
    assert sgd
    assert len(sgd.vertices) == 3
    assert len(sgd.edges) == 3
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.edges[2].label == 'e3'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.vertices[2].label == 'v3'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_2e_3v_1(unknot_2e_3v_1, poly_unknot):
    """
    Completes SGD by inserting an edge between the two vertices.
    """
    sgd = unknot_2e_3v_1
    assert sgd
    assert len(sgd.vertices) == 3
    assert len(sgd.edges) == 3
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.edges[2].label == 'e3'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.vertices[2].label == 'v3'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_2e_3v_2(unknot_2e_3v_2, poly_unknot):
    """
    Completes SGD by inserting an edge between the two vertices.
    And inserting edges between the three vertices.
    """
    sgd = unknot_2e_3v_2
    assert sgd
    assert len(sgd.vertices) == 4
    assert len(sgd.edges) == 4
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.edges[2].label == 'e3'
    assert sgd.edges[3].label == 'e4'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.vertices[2].label == 'v3'
    assert sgd.vertices[3].label == 'v4'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_3e_3v_1(unknot_3e_3v_1, poly_unknot):
    sgd = unknot_3e_3v_1
    assert sgd
    assert len(sgd.vertices) == 3
    assert len(sgd.edges) == 3
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.edges[2].label == 'e3'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.vertices[2].label == 'v3'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_3e_3v_2(unknot_3e_3v_2, poly_unknot):
    sgd = unknot_3e_3v_2
    assert sgd
    assert len(sgd.vertices) == 5
    assert len(sgd.edges) == 5
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.edges[2].label == 'e3'
    assert sgd.edges[3].label == 'e4'
    assert sgd.edges[4].label == 'e5'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.vertices[2].label == 'v3'
    assert sgd.vertices[3].label == 'v4'
    assert sgd.vertices[4].label == 'v5'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot


def test_unknot_3e_3v_3(unknot_3e_3v_3, poly_unknot):
    sgd = unknot_3e_3v_3
    assert sgd
    assert len(sgd.vertices) == 4
    assert len(sgd.edges) == 4
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.edges[1].label == 'e2'
    assert sgd.edges[2].label == 'e3'
    assert sgd.edges[3].label == 'e4'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.vertices[1].label == 'v2'
    assert sgd.vertices[2].label == 'v3'
    assert sgd.vertices[3].label == 'v4'
    assert sgd.yamada_polynomial() == poly_unknot

    # Simplify the graph
    sgd.simplify()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.edges[0].label == 'e1'
    assert sgd.vertices[0].label == 'v1'
    assert sgd.yamada_polynomial() == poly_unknot





