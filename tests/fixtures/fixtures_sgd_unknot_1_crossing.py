import pytest
from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing


# %% Clockwise Orientation


@pytest.fixture
def unknot_inf_cw_0e_0v_1c():
    """
    An unknot with a single twist, forming an infinity symbol.
    Formed by a self-connected crossing.
    Twist is clockwise.
    """
    def create_sgd():
        c1 = Crossing('c1')
        c1[0] = c1[1]
        c1[2] = c1[3]
        return SpatialGraphDiagram(crossings=[c1], simplify_diagram=False)
    return create_sgd


@pytest.fixture
def unknot_inf_cw_1e_0v_1c():
    e1 = Edge('e1')
    c1 = Crossing('c1')
    c1[0] = c1[1]
    c1[2] = e1[0]
    c1[3] = e1[1]
    sgd = SpatialGraphDiagram(edges=[e1], crossings=[c1], simplify_diagram=False)
    return sgd


@pytest.fixture
def unknot_inf_cw_2e_0v_1c_1():
    """
    An infinity symbol formed with a crossing whose four corners are connected by a pair of edges.
    """
    e1 = Edge('e1')
    e2 = Edge('e2')
    c1 = Crossing('c1')
    c1[0] = e2[1]
    c1[1] = e2[0]
    c1[2] = e1[0]
    c1[3] = e1[1]
    sgd = SpatialGraphDiagram(edges=[e1, e2], crossings=[c1], simplify_diagram=False)
    return sgd


@pytest.fixture
def unknot_inf_cw_2e_0v_1c_2():
    """
    An infinity symbol formed with a crossing whose four corners are connected by a pair of edges.
    """
    e1 = Edge('e1')
    e2 = Edge('e2')
    c1 = Crossing('c1')
    c1[0] = c1[1]
    c1[2] = e1[0]
    e1[1] = e2[0]
    e2[1] = c1[3]
    # TODO Assert warning "e1[1] and e2[0] should be connected..."
    sgd = SpatialGraphDiagram(edges=[e1, e2], crossings=[c1], simplify_diagram=False)
    return sgd


@pytest.fixture
def unknot_inf_cw_3e_0v_1c():
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    c1 = Crossing('c1')
    pass


@pytest.fixture
def unknot_inf_cw_4e_0v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_0e_1v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_1e_1v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_2e_1v_1c_1():
    e1 = Edge('e1')
    e2 = Edge('e2')
    v1 = Vertex(2, 'v1')
    c1 = Crossing("c1")
    e1[0] = c1[2]
    e1[1] = v1[0]
    v1[1] = e2[0]
    e2[1] = c1[3]
    c1[1] = c1[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2], vertices=[v1], crossings=[c1])
    return sgd


@pytest.fixture
def unknot_inf_cw_3e_1v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_4e_1v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_0e_2v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_1e_2v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_2e_2v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_3e_2v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_4e_2v_1c_1():
    def create_sgd():
        e1 = Edge('e1')
        e2 = Edge('e2')
        e3 = Edge('e3')
        e4 = Edge('e4')
        v1 = Vertex(2, 'v1')
        v2 = Vertex(2, 'v2')
        c1 = Crossing('c1')

        c1[0] = e4[1]
        c1[1] = e3[0]
        c1[2] = e1[0]
        c1[3] = e2[1]

        v1[0] = e1[1]
        v1[1] = e2[0]

        v2[0] = e3[1]
        v2[1] = e4[0]

        return SpatialGraphDiagram(edges=[e1, e2, e3, e4], vertices=[v1, v2], crossings=[c1])
    return create_sgd


@pytest.fixture
def unknot_inf_cw_0e_3v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_1e_3v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_2e_3v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_3e_3v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_4e_3v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_0e_4v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_1e_4v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_2e_4v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_3e_4v_1c():
    # TODO Implement
    pass


@pytest.fixture
def unknot_inf_cw_4e_4v_1c():
    # TODO Implement
    pass


@pytest.fixture
def TBD_unknot_inf_cw_1e_0v_1c():
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


@pytest.fixture
def TBD_unknot_inf_cw_2e_1c(orientation='cw'):
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
def TBD_unknot_infinity_1_4e_2v_1c():
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


# %% Counterclockwise Orientation


@pytest.fixture
def unknot_inf_ccw_0e_0v_1c_1():
    c1 = Crossing("c1")
    c1[0] = c1[3]
    c1[1] = c1[2]
    sgd = SpatialGraphDiagram(crossings=[c1])
    return sgd



@pytest.fixture
def unknot_inf_ccw_2e_0v_1c_1():
    """
    An infinity symbol formed with a crossing whose four corners are connected by a pair of edges.
    """
    e1 = Edge('e1')
    e2 = Edge('e2')
    c1 = Crossing('c1')
    c1[3] = e2[1]
    c1[0] = e2[0]
    c1[1] = e1[0]
    c1[2] = e1[1]
    sgd = SpatialGraphDiagram(edges=[e1, e2], crossings=[c1])
    return sgd