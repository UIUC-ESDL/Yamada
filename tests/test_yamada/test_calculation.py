"""Test the calculation of the Yamada polynomial of a spatial graph diagram manually labeled.


"""


import networkx as nx
from cypari import pari
from yamada.calculation import has_cut_edge, remove_valence_two_vertices, h_poly, SpatialGraphDiagram, Vertex, Edge, \
    Crossing, reverse_poly, normalize_yamada_polynomial

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

# TODO Implement tests for normalize_poly
# def test_normalize_poly():
