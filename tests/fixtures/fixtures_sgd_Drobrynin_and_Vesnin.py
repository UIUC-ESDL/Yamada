import pytest
from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing


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
