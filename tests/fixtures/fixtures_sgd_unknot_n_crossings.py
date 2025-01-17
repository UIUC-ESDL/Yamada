import pytest
from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing


@pytest.fixture
def unknot_over_loop():
    """An unknot with a loop over it."""
    def create_sgd():
        e1 = Edge('e1')
        e2 = Edge('e2')
        e3 = Edge('e3')
        e4 = Edge('e4')
        c1 = Crossing('c1')
        c2 = Crossing('c2')

        c1[0] = e4[1]
        c1[1] = e2[0]
        c1[2] = e1[0]
        c1[3] = e1[1]

        c2[0] = e3[1]
        c2[1] = e2[1]
        c2[2] = e4[0]
        c2[3] = e3[0]

        return SpatialGraphDiagram(edges=[e1, e2, e3, e4], crossings=[c1, c2])
    return create_sgd


@pytest.fixture
def unknot_under_loop():
    # TODO Implement
    pass


@pytest.fixture
def unknot_two_over_loops():
    """An unknot with two loops that share the same crossing orientations."""
    def create_sgd():
        e1 = Edge('e1')
        e2 = Edge('e2')
        e3 = Edge('e3')
        e4 = Edge('e4')
        e5 = Edge('e5')
        e6 = Edge('e6')
        e7 = Edge('e7')
        e8 = Edge('e8')
        c1 = Crossing('c1')
        c2 = Crossing('c2')
        c3 = Crossing('c3')
        c4 = Crossing('c4')

        c1[0] = e8[0]
        c1[1] = e2[0]
        c1[2] = e1[0]
        c1[3] = e1[1]

        c2[0] = e7[1]
        c2[1] = e2[1]
        c2[2] = e8[1]
        c2[3] = e3[0]

        c3[0] = e6[1]
        c3[1] = e4[0]
        c3[2] = e7[0]
        c3[3] = e3[1]

        c4[0] = e5[1]
        c4[1] = e4[1]
        c4[2] = e6[0]
        c4[3] = e5[0]

        return SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6, e7, e8], crossings=[c1, c2, c3, c4])
    return create_sgd


@pytest.fixture
def unknot_two_under_loops():
    pass


@pytest.fixture
def unknot_one_over_one_under_loop():
    """An unknot with two loops that have opposing crossing orientations."""
    pass


@pytest.fixture
def unknot_two_ccw_twists():
    def create_sgd():
        e1 = Edge('e1')
        e2 = Edge('e2')
        e3 = Edge('e3')
        e4 = Edge('e4')
        c1 = Crossing('c1')
        c2 = Crossing('c2')

        c1[0] = e3[1]
        c1[1] = e4[0]
        c1[2] = e2[1]
        c1[3] = e3[0]

        c2[0] = e1[1]
        c2[1] = e2[0]
        c2[2] = e4[1]
        c2[3] = e1[0]

        return SpatialGraphDiagram(edges=[e1, e2, e3, e4], crossings=[c1, c2])
    return create_sgd


@pytest.fixture
def unknot_one_ccw_one_cw_twist():
    def create_sgd():
        e1 = Edge('e1')
        e2 = Edge('e2')
        e3 = Edge('e3')
        e4 = Edge('e4')
        c1 = Crossing('c1')
        c2 = Crossing('c2')

        c1[0] = e3[1]
        c1[1] = e4[0]
        c1[2] = e2[1]
        c1[3] = e3[0]

        c2[0] = e1[0]
        c2[1] = e1[1]
        c2[2] = e2[0]
        c2[3] = e4[1]

        return SpatialGraphDiagram(edges=[e1, e2, e3, e4], crossings=[c1, c2])

    return create_sgd


@pytest.fixture
def unknot_two_cw_twists():
    def create_sgd():
        e1 = Edge('e1')
        e2 = Edge('e2')
        e3 = Edge('e3')
        e4 = Edge('e4')
        c1 = Crossing('c1')
        c2 = Crossing('c2')

        c1[0] = e3[0]
        c1[1] = e3[1]
        c1[2] = e4[0]
        c1[3] = e2[1]

        c2[0] = e1[0]
        c2[1] = e1[1]
        c2[2] = e2[0]
        c2[3] = e4[1]

        return SpatialGraphDiagram(edges=[e1, e2, e3, e4], crossings=[c1, c2])

    return create_sgd

