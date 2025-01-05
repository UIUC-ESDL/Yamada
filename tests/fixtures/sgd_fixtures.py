import pytest
from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing


@pytest.fixture
def unknot_1e():
    e1 = Edge(1)
    e1[0] = e1[1]
    sgd = SpatialGraphDiagram([e1])
    return sgd


@pytest.fixture
def unknot_1e_1v():
    e1 = Edge(1)
    v1 = Vertex(2, label='v1')
    e1[0] = v1[0]
    e1[1] = v1[1]
    sgd = SpatialGraphDiagram([e1, v1])
    return sgd


@pytest.fixture
def unknot_2e_2v():
    e1, e2 = Edge(1), Edge(2)
    v1, v2 = Vertex(2, 'v1'), Vertex(2, 'v2')
    e1[0], e1[1] = v1[0], v2[0]
    e2[0], e2[1] = v1[1], v2[1]
    sgd = SpatialGraphDiagram([e1, e2, v1, v2])
    return sgd


@pytest.fixture
def unknotted_theta_graph_1():
    va, vb = Vertex(3, 'a'), Vertex(3, 'b')
    e0, e1, e2 = Edge(0), Edge(1), Edge(2)
    va[0], va[1], va[2] = e0[0], e1[0], e2[0]
    vb[0], vb[1], vb[2] = e0[1], e2[1], e1[1]
    sgd = SpatialGraphDiagram([va, vb, e0, e1, e2])
    return sgd
