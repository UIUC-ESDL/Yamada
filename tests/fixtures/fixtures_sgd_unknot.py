import pytest
from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing


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
    sgd = SpatialGraphDiagram(edges=[e1], simplify=False)
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
    sgd = SpatialGraphDiagram(edges=[e1, e2], simplify=False)
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
    sgd = SpatialGraphDiagram(edges=[e1, e2, e3], simplify=False)
    return sgd


@pytest.fixture
def unknot_0e_1v():
    """
    An unknot formed by a single, self-connected vertex.
    """
    v1 = Vertex(2, label='v1')
    v1[0] = v1[1]
    sgd = SpatialGraphDiagram(vertices=[v1], simplify=False)
    return sgd


@pytest.fixture
def unknot_1e_1v():
    """An unknot formed by an edge and a 2-valent vertex."""
    e1 = Edge('e1')
    v1 = Vertex(2, label='v1')
    v1[0] = e1[1]
    v1[1] = e1[0]
    sgd = SpatialGraphDiagram(edges=[e1], vertices=[v1], simplify=False)
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
    sgd = SpatialGraphDiagram(edges=[e1, e2], vertices=[v1], simplify=False)
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
    sgd = SpatialGraphDiagram(edges=[e1, e2, e3], vertices=[v1], simplify=False)
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
    sgd = SpatialGraphDiagram(vertices=[v1, v2], simplify=False)
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
    sgd = SpatialGraphDiagram(edges=[e1], vertices=[v1, v2], simplify=False)
    return sgd


@pytest.fixture
def unknot_2e_2v_1():
    e1 = Edge('e1')
    e2 = Edge('e2')
    v1 = Vertex(2, 'v1')
    v2 = Vertex(2, 'v2')
    v1[0] = e2[1]
    v1[1] = e1[0]
    e1[1] = v2[0]
    v2[1] = e2[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2], vertices=[v1, v2], simplify=False)
    return sgd


@pytest.fixture
def unknot_2e_2v_2():
    e1 = Edge('e1')
    e2 = Edge('e2')
    v1 = Vertex(2, 'v1')
    v2 = Vertex(2, 'v2')
    v1[0] = v2[1]
    v1[1] = e1[0]
    e1[1] = e2[0]
    e2[1] = v2[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2], vertices=[v1, v2], simplify=False)
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
    sgd = SpatialGraphDiagram(edges=[e1, e2, e3], vertices=[v1, v2], simplify=False)
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
    sgd = SpatialGraphDiagram(edges=[e1, e2, e3], vertices=[v1, v2], simplify=False)
    return sgd


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
    sgd = SpatialGraphDiagram(vertices=[v1, v2, v3], simplify=False)
    return sgd


@pytest.fixture
def unknot_1e_3v():
    e1 = Edge('e1')
    v1 = Vertex(2, 'v1')
    v2 = Vertex(2, 'v2')
    v3 = Vertex(2, 'v3')
    v1[0] = v3[1]
    v1[1] = e1[0]
    e1[1] = v2[0]
    v2[1] = v3[0]
    sgd = SpatialGraphDiagram(edges=[e1], vertices=[v1, v2, v3], simplify=False)
    return sgd


@pytest.fixture
def unknot_2e_3v_1():
    e1 = Edge('e1')
    e2 = Edge('e2')
    v1 = Vertex(2, 'v1')
    v2 = Vertex(2, 'v2')
    v3 = Vertex(2, 'v3')
    v1[0] = v3[1]
    v1[1] = e1[0]
    e1[1] = v2[0]
    v2[1] = e2[0]
    e2[1] = v3[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2], vertices=[v1, v2, v3], simplify=False)
    return sgd


@pytest.fixture
def unknot_2e_3v_2():
    e1 = Edge('e1')
    e2 = Edge('e2')
    v1 = Vertex(2, 'v1')
    v2 = Vertex(2, 'v2')
    v3 = Vertex(2, 'v3')
    v1[0] = v3[1]
    v1[1] = e1[0]
    e1[1] = e2[0]
    e2[1] = v2[0]
    v2[1] = v3[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2], vertices=[v1, v2, v3], simplify=False)
    return sgd



@pytest.fixture
def unknot_3e_3v_1():
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
    sgd = SpatialGraphDiagram(edges=[e1, e2, e3], vertices=[v1, v2, v3], simplify=False)
    return sgd


@pytest.fixture
def unknot_3e_3v_2():
    """An unknot formed by three edges and three 2-valent vertices."""
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    v1 = Vertex(2, 'v1')
    v2 = Vertex(2, 'v2')
    v3 = Vertex(2, 'v3')
    v1[0] = v3[1]
    v1[1] = e1[0]
    e1[1] = e2[0]
    e2[1] = e3[0]
    e3[1] = v2[0]
    v2[1] = v3[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2, e3], vertices=[v1, v2, v3], simplify=False)
    return sgd


@pytest.fixture
def unknot_3e_3v_3():
    """An unknot formed by three edges and three 2-valent vertices."""
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    v1 = Vertex(2, 'v1')
    v2 = Vertex(2, 'v2')
    v3 = Vertex(2, 'v3')
    v1[0] = v3[1]
    v1[1] = e1[0]
    e1[1] = e2[0]
    e2[1] = v2[0]
    v2[1] = e3[0]
    e3[1] = v3[0]
    sgd = SpatialGraphDiagram(edges=[e1, e2, e3], vertices=[v1, v2, v3], simplify=False)
    return sgd
