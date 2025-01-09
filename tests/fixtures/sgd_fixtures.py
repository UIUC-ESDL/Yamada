import pytest
from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing


@pytest.fixture
def unknot_1e():
    """
    A circle formed by one edge that is connected to itself.
    TODO SGD Should fix this by adding a vertex to the edge.
    """
    e1 = Edge(1)
    e1[0] = e1[1]
    sgd = SpatialGraphDiagram(edges=[e1])
    return sgd


@pytest.fixture
def unknot_1e_1v():
    """A circle formed by one edge that is connected to itself by a vertex."""
    e1 = Edge(1)
    v1 = Vertex(2, label='v1')
    e1[0] = v1[0]
    e1[1] = v1[1]
    sgd = SpatialGraphDiagram(edges=[e1], vertices=[v1])
    return sgd


@pytest.fixture
def unknot_2e_2v():
    """A circle formed by two edges that are connected to each other by two vertices."""
    e1, e2 = Edge(1), Edge(2)
    v1, v2 = Vertex(2, 'v1'), Vertex(2, 'v2')
    e1[0], e1[1] = v1[0], v2[0]
    e2[0], e2[1] = v1[1], v2[1]
    sgd = SpatialGraphDiagram(edges=[e1, e2], vertices=[v1, v2])
    return sgd


@pytest.fixture
def unknot_infinity_1c():
    """
    An infinity symbol formed by one self-connected crossing.
    TODO SGD should fix this by adding edges to self-connected crossings.
    """
    c1 = Crossing("c1")
    c1[1] = c1[2]
    c1[3] = c1[0]
    sgd = SpatialGraphDiagram(crossings=[c1])
    return sgd


@pytest.fixture
def unknot_infinity_1e_1c():
    """An infinity symbol formed with a crossing that had two corners self-connected and the other two connected by an edge."""
    e1 = Edge(1)
    c1 = Crossing("c1")

    e1[0] = c1[2]
    e1[1] = c1[1]
    c1[0] = c1[3]
    sgd = SpatialGraphDiagram(edges=[e1], crossings=[c1])
    return sgd


@pytest.fixture
def unknot_infinity_1_2e_1c():
    e1, e2 = Edge(1), Edge(2)
    c1 = Crossing("c1")
    e1[0], e1[1] = c1[2], c1[3]
    e2[0], e2[1] = c1[1], c1[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2], crossings=[c1])
    return sgd


@pytest.fixture
def unknot_infinity_2_2e_1c():
    """
    An infinity symbol formed with a crossing whose four corners are connected by a pair of edges.
    """
    e1, e2 = Edge(1), Edge(2)
    c1 = Crossing("c1")
    e1[0], e1[1] = c1[3], c1[0]
    e2[0], e2[1] = c1[2], c1[1]
    sgd = SpatialGraphDiagram(edges=[e1, e2], crossings=[c1])
    return sgd


@pytest.fixture
def unknot_infinity_1_4e_2v_1c():
    """
    An infinity symbol formed with a crossing whose four corners are connected by a pair of edges.
    The order of these corners is reversed.
    """
    e1, e2, e3, e4 = Edge(1), Edge(2), Edge(3), Edge(4)
    v1, v2 = Vertex(2, 'v1'), Vertex(2, 'v2')
    c1 = Crossing('c1')
    e1[0] = c1[2]
    e1[1] = v1[0]
    v1[1] = e3[0]
    e3[1] = c1[3]
    e2[0] = c1[1]
    e2[1] = v2[0]
    v2[1] = e4[0]
    e4[1] = c1[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4], vertices=[v1, v2], crossings=[c1])
    return sgd


@pytest.fixture
def unknot_double_loop_same_4e_2c():
    """An unknot with two loops that share the same crossing orientations."""
    pass


@pytest.fixture
def unknot_double_loop_opposite_4e_2c():
    """An unknot with two loops that have opposing crossing orientations."""
    pass


@pytest.fixture
def unknotted_theta_graph_1():
    va, vb = Vertex(3, 'a'), Vertex(3, 'b')
    e0, e1, e2 = Edge(0), Edge(1), Edge(2)
    va[0], va[1], va[2] = e0[0], e1[0], e2[0]
    vb[0], vb[1], vb[2] = e0[1], e2[1], e1[1]
    sgd = SpatialGraphDiagram(edges=[e1, e2], vertices=[va, vb, e0])
    return sgd
