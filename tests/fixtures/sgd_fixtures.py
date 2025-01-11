import pytest
from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing


# %% Simple Unknots

@pytest.fixture
def unknot_0e_0v():
    """
    An unknot with no edges or vertices.
    Should raise an error.
    """
    sgd = SpatialGraphDiagram()
    return sgd


@pytest.fixture
def unknot_1e_0v():
    """
    An unknot formed by a single, self-connected edge.
    """
    e1 = Edge('e1')
    e1[0] = e1[1]
    sgd = SpatialGraphDiagram(edges=[e1])
    return sgd


@pytest.fixture
def unknot_2e_0v():
    """
    An unknot formed by two edges.
    """
    e1 = Edge('e1')
    e2 = Edge('e2')
    e1[0] = e2[1]
    e1[1] = e2[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2])
    return sgd


@pytest.fixture
def unknot_3e_0v():
    """
    An unknot formed by three edges.
    """
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    e1[0] = e3[1]
    e1[1] = e2[0]
    e2[1] = e3[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2, e3])
    return sgd


@pytest.fixture
def unknot_0e_1v():
    """
    An unknot formed by a single, self-connected vertex.
    """
    v1 = Vertex(2, label='v1')
    v1[0] = v1[1]
    sgd = SpatialGraphDiagram(vertices=[v1])
    return sgd


@pytest.fixture
def unknot_1e_1v():
    """An unknot formed by an edge and a 2-valent vertex."""
    e1 = Edge('e1')
    v1 = Vertex(2, label='v1')
    v1[0] = e1[1]
    v1[1] = e1[0]
    sgd = SpatialGraphDiagram(edges=[e1], vertices=[v1])
    return sgd


@pytest.fixture
def unknot_2e_1v():
    """An unknot formed by two edges and a 2-valent vertex."""
    e1 = Edge('e1')
    e2 = Edge('e2')
    v1 = Vertex(2, 'v1')
    v1[0] = e2[1]
    v1[1] = e1[0]
    e1[1] = e2[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2], vertices=[v1])
    return sgd

@pytest.fixture
def unknot_3e_1v():
    """An unknot formed by three edges and a 2-valent vertex."""
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    v1 = Vertex(2, 'v1')
    v1[0] = e3[1]
    v1[1] = e1[0]
    e1[1] = e2[0]
    e2[1] = e3[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2, e3], vertices=[v1])
    return sgd


@pytest.fixture
def unknot_0e_2v():
    """
    An unknot formed by two vertices.
    """
    v1 = Vertex(2, label='v1')
    v2 = Vertex(2, label='v2')
    v1[0] = v2[1]
    v1[1] = v2[0]
    sgd = SpatialGraphDiagram(vertices=[v1, v2])
    return sgd

@pytest.fixture
def unknot_1e_2v():
    """An unknot formed by an edge and two 2-valent vertices."""
    e1 = Edge('e1')
    v1 = Vertex(2, 'v1')
    v2 = Vertex(2, 'v2')
    v1[0] = v2[1]
    v1[1] = e1[0]
    e1[1] = v2[0]
    sgd = SpatialGraphDiagram(edges=[e1], vertices=[v1, v2])
    return sgd


@pytest.fixture
def unknot_2e_2v():
    pass


@pytest.fixture
def unknot_0e_3v():
    """
    An unknot formed by three vertices.
    """
    v1 = Vertex(2, label='v1')
    v2 = Vertex(2, label='v2')
    v3 = Vertex(2, label='v3')
    v1[0] = v3[1]
    v1[1] = v2[0]
    v2[1] = v3[0]
    sgd = SpatialGraphDiagram(vertices=[v1, v2, v3])
    return sgd


@pytest.fixture
def TBDunknot_0e_1v():
    """An unknot formed by an edge and a 2-valent vertex."""
    e1 = Edge('e1')
    v1 = Vertex(2, label='v1')
    v1[0] = e1[1]
    v1[1] = e1[0]
    sgd = SpatialGraphDiagram(edges=[e1], vertices=[v1])
    return sgd


@pytest.fixture
def unknot_2e_2v():
    """An unknot formed by two edges and two 2-valent vertices."""
    e1 = Edge('e1')
    e2 = Edge('e2')
    v1 = Vertex(2, 'v1')
    v2 = Vertex(2, 'v2')
    v1[0] = e2[1]
    v1[1] = e1[0]
    v2[0] = e1[1]
    v2[1] = e2[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2], vertices=[v1, v2])
    return sgd


@pytest.fixture
def unknot_3e_2v_1():
    """An unknot formed by three edges and two 2-valent vertices."""
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    v1 = Vertex(2, 'v1')
    v2 = Vertex(2, 'v2')
    v1[0] = v2[1]
    v1[1] = e1[0]
    e1[1] = e2[0]
    e2[1] = e3[0]
    e3[1] = v2[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2, e3], vertices=[v1, v2])
    return sgd


@pytest.fixture
def unknot_3e_2v_2():
    """An unknot formed by three edges and two 2-valent vertices."""
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    v1 = Vertex(2, 'v1')
    v2 = Vertex(2, 'v2')
    v1[0] = e3[1]
    v1[1] = e1[0]
    e1[1] = e2[0]
    e2[1] = v2[0]
    v2[1] = e3[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2, e3], vertices=[v1, v2])
    return sgd


@pytest.fixture
def unknot_3e_3v():
    """An unknot formed by three edges and three 2-valent vertices."""
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    v1 = Vertex(2, 'v1')
    v2 = Vertex(2, 'v2')
    v3 = Vertex(2, 'v3')
    v1[0] = e3[1]
    v1[1] = e1[0]
    v2[0] = e1[1]
    v2[1] = e2[0]
    v3[0] = e2[1]
    v3[1] = e3[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2, e3], vertices=[v1, v2, v3])
    return sgd


# %% Unknots with a single twist


@pytest.fixture
def unknot_inf_cw_1c():
    """
    An unknot with a single twist, forming an infinity symbol.
    Formed by a self-connected crossing.
    Twist is clockwise.
    """
    c1 = Crossing("c1")
    c1[0] = c1[3]
    c1[1] = c1[2]
    sgd = SpatialGraphDiagram(crossings=[c1])
    return sgd


@pytest.fixture
def unknot_inf_cw_1e_1c():
    """
    An unknot with a single twist, forming an infinity symbol.
    Formed by a crossing with two corners self-connected and two corners connected via an edge.
    Twist is clockwise.
    """
    e1 = Edge('e1')
    c1 = Crossing("c1")
    c1[0] = c1[3]
    c1[1] = e1[0]
    c1[2] = e1[1]
    sgd = SpatialGraphDiagram(edges=[e1], crossings=[c1])
    return sgd


# ...other orientations...

@pytest.fixture
def unknot_inf_cw_2e_1c(orientation='cw'):
    """
    An unknot with a single twist, forming an infinity symbol.
    Formed by a crossing with two corners self-connected and two corners connected via an edge.
    Order of corners is reversed.
    TODO Ensure CW
    """
    e1 = Edge('e1')
    e2 = Edge('e2')
    c1 = Crossing('c1')

    if orientation == 'cw':
        c1[0] = e2[0]
        c1[1] = e2[1]
        c1[2] = e1[0]
        c1[3] = e1[1]
    elif orientation == 'ccw':
        c1[0] = e1[0]
        c1[1] = e2[0]
        c1[2] = e2[1]
        c1[3] = e1[1]

    sgd = SpatialGraphDiagram(edges=[e1, e2], crossings=[c1])
    return sgd


@pytest.fixture
def unknot_infinity_ccw_2e_1c():
    """
    An infinity symbol formed with a crossing whose four corners are connected by a pair of edges.
    """
    e1 = Edge('e1')
    e2 = Edge('e2')
    c1 = Crossing('c1')
    c1[0] = e1[0]
    c1[1] = e2[0]
    c1[2] = e2[1]
    c1[3] = e1[1]
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


# %% Unknots with two loops


@pytest.fixture
def unknot_double_loop_same_4e_2c():
    """An unknot with two loops that share the same crossing orientations."""
    pass


@pytest.fixture
def unknot_double_loop_opposite_4e_2c():
    """An unknot with two loops that have opposing crossing orientations."""
    pass


# %% Knots from Drobrynin and Vesnin


@pytest.fixture
def unknotted_theta_graph_1():
    v1 = Vertex(3, 'v1')
    v2 = Vertex(3, 'v2')
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    v1[0] = e1[0]
    v1[1] = e2[0]
    v1[2] = e3[0]
    v2[0] = e1[1]
    v2[1] = e3[1]
    v2[2] = e2[1]
    sgd = SpatialGraphDiagram(edges=[e1, e2, e3], vertices=[v1, v2])
    return sgd


@pytest.fixture
def unknotted_theta_graph_2():
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    v1 = Vertex(3, 'v1')
    v2 = Vertex(3, 'v2')
    v1[0] = e1[0]
    v1[1] = e2[0]
    v1[2] = e3[0]
    v2[0] = e1[1]
    v2[1] = e3[1]
    v2[2] = e2[1]
    sgd = SpatialGraphDiagram(edges=[e1, e2, e3], vertices=[v1, v2])
    return sgd


@pytest.fixture
def omega_2_graph():
    """
    The Omega_2 graph from Drobrynin and Vesnin
    """
    v1 = Vertex(3, 'v1')
    v2 = Vertex(3, 'v2')
    v3 = Vertex(3, 'v3')
    v4 = Vertex(3, 'v4')
    c1 = Crossing('c1')
    c2 = Crossing('c2')
    c3 = Crossing('c3')
    v1[0] = v4[0]
    v1[1] = v2[2]
    v1[2] = c1[2]
    v2[0] = v3[0]
    v2[1] = c1[3]
    v3[1] = v4[2]
    v3[2] = c3[0]
    v4[1] = c3[1]
    c1[0] = c2[3]
    c1[1] = c2[2]
    c2[0] = c3[3]
    c2[1] = c3[2]
    sgd = SpatialGraphDiagram(vertices=[v1, v2, v3, v4], crossings=[c1, c2, c3])
    return sgd


# %% Other knots

