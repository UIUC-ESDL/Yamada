"""Test the calculation of the Yamada polynomial of a spatial graph diagram manually labeled.


"""


import networkx as nx
from cypari import pari
from yamada import has_cut_edge, remove_valence_two_vertices, h_poly, SpatialGraphDiagram, Vertex, Edge, \
    Crossing, reverse_poly, normalize_poly

def test_has_cut_edge_1():
    g = nx.MultiGraph(nx.barbell_graph(3, 0))
    assert has_cut_edge(g)


def test_has_cut_edge_2():
    g = nx.MultiGraph(nx.barbell_graph(3, 0))
    g.add_edge(2, 3)
    assert not has_cut_edge(g)


def test_remove_valence_two_vertices():
    g = nx.MultiGraph([(0, 1), (1, 2), (2, 0)])
    c = remove_valence_two_vertices(g)
    assert list(c.edges()) == [(0, 0)]

# TODO Implement tests for get_coefficients_and_exponents

def test_reverse_poly():
    """

    """

    a = pari('A')

    assert reverse_poly(a ** -1 + 2) == a + 2


def test_normalize_poly_zero():
    assert normalize_poly(pari(0)) == 0


def test_yamada_polynomial_cut_edge_diagram_is_zero():
    e1 = Edge('e1')
    v1 = Vertex(1, 'v1')
    v2 = Vertex(1, 'v2')
    v1[0] = e1[0]
    v2[0] = e1[1]

    sgd = SpatialGraphDiagram(edges=[e1], vertices=[v1, v2])

    assert sgd.yamada_polynomial() == 0
