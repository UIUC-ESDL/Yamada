import pytest
from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing


@pytest.fixture
def empty_0e_0v_0c():
    """
    An unknot with no edges or vertices.
    Should raise an error.
    """
    sgd = SpatialGraphDiagram(correct_diagram=False, simplify_diagram=False)

    return sgd