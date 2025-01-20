import pytest
from yamada import SpatialGraphDiagram, Edge, Vertex, Crossing


@pytest.fixture
def two_unknots_1():
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    e4 = Edge('e4')
    e5 = Edge('e5')
    e6 = Edge('e6')
    e7 = Edge('e7')
    e8 = Edge('e8')
    e9 = Edge('e9')
    e10 = Edge('e10')
    c1 = Crossing('c1')
    c2 = Crossing('c2')
    c3 = Crossing('c3')
    c4 = Crossing('c4')
    c5 = Crossing('c5')

    c1[0] = e1[0]
    c1[1] = e4[0]
    c1[2] = e3[0]
    c1[3] = e2[0]

    c2[0] = e6[0]
    c2[1] = e9[0]
    c2[2] = e5[1]
    c2[3] = e1[1]

    c3[0] = e6[1]
    c3[1] = e2[1]
    c3[2] = e7[1]
    c3[3] = e9[1]

    c4[0] = e8[1]
    c4[1] = e10[1]
    c4[2] = e7[0]
    c4[3] = e3[1]

    c5[0] = e5[0]
    c5[1] = e10[0]
    c5[2] = e8[0]
    c5[3] = e4[1]

    sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6, e7, e8, e9, e10], crossings=[c1, c2, c3, c4, c5])

    # Number of available Reidemeister moves
    # n_r3 = 8
    # n_r2 = 2
    # n_r1 = 0

    return sgd


@pytest.fixture
def two_unknots_2():

    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    e4 = Edge('e4')
    e5 = Edge('e5')
    e6 = Edge('e6')
    e7 = Edge('e7')
    e8 = Edge('e8')
    e9 = Edge('e9')
    e10 = Edge('e10')

    c1 = Crossing('c1')
    c2 = Crossing('c2')
    c3 = Crossing('c3')
    c4 = Crossing('c4')
    c5 = Crossing('c5')

    c1[0] = e2[0]
    c1[1] = e3[0]
    c1[2] = e10[1]
    c1[3] = e9[1]

    c2[0] = e6[0]
    c2[1] = e9[0]
    c2[2] = e5[1]
    c2[3] = e1[1]

    c3[0] = e6[1]
    c3[1] = e1[0]
    c3[2] = e7[1]
    c3[3] = e2[1]

    c4[0] = e8[1]
    c4[1] = e3[1]
    c4[2] = e7[0]
    c4[3] = e4[0]

    c5[0] = e5[0]
    c5[1] = e10[0]
    c5[2] = e8[0]
    c5[3] = e4[1]

    sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6, e7, e8, e9, e10], crossings=[c1, c2, c3, c4, c5])

    return sgd


@pytest.fixture
def two_unknots_3():
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    e4 = Edge('e4')
    e5 = Edge('e5')
    e6 = Edge('e6')
    e7 = Edge('e7')
    e8 = Edge('e8')
    e9 = Edge('e9')
    e10 = Edge('e10')

    c1 = Crossing('c1')
    c2 = Crossing('c2')
    c3 = Crossing('c3')
    c4 = Crossing('c4')
    c5 = Crossing('c5')

    c1[0] = e6[0]
    c1[1] = e4[0]
    c1[2] = e1[0]
    c1[3] = e2[0]

    c2[0] = e1[1]
    c2[1] = e5[1]
    c2[2] = e8[0]
    c2[3] = e3[0]

    c3[0] = e6[1]
    c3[1] = e2[1]
    c3[2] = e7[1]
    c3[3] = e9[1]

    c4[0] = e8[1]
    c4[1] = e10[1]
    c4[2] = e7[0]
    c4[3] = e3[1]

    c5[0] = e9[0]
    c5[1] = e10[0]
    c5[2] = e5[0]
    c5[3] = e4[1]

    sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6, e7, e8, e9, e10], crossings=[c1, c2, c3, c4, c5])

    # Number of available Reidemeister moves
    # n_r3 = 8
    # n_r2 = 2
    # n_r1 = 0

    return sgd


@pytest.fixture
def two_unknots_4():
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    e4 = Edge('e4')
    e5 = Edge('e5')
    e6 = Edge('e6')
    e7 = Edge('e7')
    e8 = Edge('e8')
    e9 = Edge('e9')
    e10 = Edge('e10')

    c1 = Crossing('c1')
    c2 = Crossing('c2')
    c3 = Crossing('c3')
    c4 = Crossing('c4')
    c5 = Crossing('c5')

    c1[0] = e6[0]
    c1[1] = e4[0]
    c1[2] = e1[0]
    c1[3] = e2[0]

    c2[0] = e1[1]
    c2[1] = e5[1]
    c2[2] = e8[0]
    c2[3] = e3[0]

    c3[0] = e9[1]
    c3[1] = e7[1]
    c3[2] = e8[1]
    c3[3] = e5[0]

    c4[0] = e7[0]
    c4[1] = e10[1]
    c4[2] = e2[1]
    c4[3] = e3[1]

    c5[0] = e6[1]
    c5[1] = e10[0]
    c5[2] = e9[0]
    c5[3] = e4[1]

    # Number of available Reidemeister moves
    # n_r3 = 8
    # n_r2 = 2
    # n_r1 = 0

    sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6, e7, e8, e9, e10], crossings=[c1, c2, c3, c4, c5])

    return sgd


@pytest.fixture
def two_unknots_5():
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    e4 = Edge('e4')
    e5 = Edge('e5')
    e6 = Edge('e6')
    e7 = Edge('e7')
    e8 = Edge('e8')
    e9 = Edge('e9')
    e10 = Edge('e10')

    c1 = Crossing('c1')
    c2 = Crossing('c2')
    c3 = Crossing('c3')
    c4 = Crossing('c4')
    c5 = Crossing('c5')

    c1[0] = e6[0]
    c1[1] = e4[0]
    c1[2] = e1[0]
    c1[3] = e2[0]

    c2[0] = e1[1]
    c2[1] = e3[0]
    c2[2] = e8[0]
    c2[3] = e2[1]

    c3[0] = e9[1]
    c3[1] = e10[1]
    c3[2] = e8[1]
    c3[3] = e7[1]

    c4[0] = e5[0]
    c4[1] = e7[0]
    c4[2] = e3[1]
    c4[3] = e5[1]

    c5[0] = e6[1]
    c5[1] = e10[0]
    c5[2] = e9[0]
    c5[3] = e4[1]

    # Number of available Reidemeister moves
    # n_r3 = 2
    # n_r2 = 3
    # n_r1 = 1

    sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6, e7, e8, e9, e10], crossings=[c1, c2, c3, c4, c5])

    return sgd


@pytest.fixture
def two_unknots_6():
    pass


@pytest.fixture
def figure_8():

    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    e4 = Edge('e4')
    e5 = Edge('e5')
    e6 = Edge('e6')

    c1 = Crossing('c1')
    c2 = Crossing('c2')
    c3 = Crossing('c3')

    c1[0] = e2[1]
    c1[1] = e1[0]
    c1[2] = e4[0]
    c1[3] = e3[1]

    c2[0] = e6[0]
    c2[1] = e2[0]
    c2[2] = e3[0]
    c2[3] = e5[0]

    c3[0] = e5[1]
    c3[1] = e4[1]
    c3[2] = e1[1]
    c3[3] = e6[1]

    sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6], crossings=[c1, c2, c3])

    return sgd


@pytest.fixture
def double_figure_8():

    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    e4 = Edge('e4')
    e5 = Edge('e5')
    e6 = Edge('e6')
    e7 = Edge('e7')
    e8 = Edge('e8')
    e9 = Edge('e9')
    e10 = Edge('e10')
    e11 = Edge('e11')
    e12 = Edge('e12')

    c1 = Crossing("c1")
    c2 = Crossing("c2")
    c3 = Crossing("c3")
    c4 = Crossing("c4")
    c5 = Crossing("c5")
    c6 = Crossing("c6")

    # First Figure 8 Knot

    c1[0] = e2[1]
    c1[1] = e1[0]
    c1[2] = e4[0]
    c1[3] = e3[1]

    c2[0] = e6[0]
    c2[1] = e2[0]
    c2[2] = e3[0]
    c2[3] = e5[0]

    c3[0] = e5[1]
    c3[1] = e4[1]
    c3[2] = e7[1]
    c3[3] = e6[1]

    # Second Figure 8 Knot

    c4[0] = e8[1]
    c4[1] = e7[0]
    c4[2] = e10[0]
    c4[3] = e9[1]

    c5[0] = e12[0]
    c5[1] = e8[0]
    c5[2] = e9[0]
    c5[3] = e11[0]

    c6[0] = e11[1]
    c6[1] = e10[1]
    c6[2] = e1[1]
    c6[3] = e12[1]

    sgd = SpatialGraphDiagram(edges=[e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12], crossings=[c1, c2, c3, c4, c5, c6])

    return sgd