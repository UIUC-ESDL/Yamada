import networkx as nx
from cypari import pari
from yamada import remove_valence_two_vertices, h_poly, SpatialGraphDiagram, Vertex, Edge, \
    Crossing, normalize_poly

def test_unknotted_theta_graph_1(unknotted_theta_graph_1):
    sgd = unknotted_theta_graph_1
    assert sgd
    assert len(sgd.crossings) == 0
    assert len(sgd.vertices) == 2

    g = sgd.graph()
    t = nx.MultiGraph(3 * [(0, 1)])

    assert nx.is_isomorphic(remove_valence_two_vertices(g), t)

    t = nx.MultiGraph(3 * [(0, 1)])

    assert sgd.yamada_polynomial(normalize=False) == h_poly(t)
    a = pari('A')
    assert sgd.yamada_polynomial() == normalize_poly(-a ** 4 - a ** 3 - 2 * a ** 2 - a - 1)

def test_sgd_unknotted_theta_graph_2(unknotted_theta_graph_2):

    sgd = unknotted_theta_graph_2

    g = sgd.graph()
    t = nx.MultiGraph(3 * [(0, 1)])

    assert nx.is_isomorphic(remove_valence_two_vertices(g), t)
    a = pari('A')

    assert sgd.yamada_polynomial() == normalize_poly(-a ** 4 - a ** 3 - 2 * a ** 2 - a - 1)

    t = nx.MultiGraph(3 * [(0, 1)])

    assert nx.is_isomorphic(g, t)

    assert sgd.yamada_polynomial() == normalize_poly(
        a ** 12 - a ** 8 - a ** 6 - a ** 4 - a ** 3 - a ** 2 - a - 1)


def test_sgd_omega_2_graph(omega_2_graph):
    """
    The Omega_2 graph from Drobrynin and Vesnin:
    """
    sgd = omega_2_graph
    g = sgd.underlying_graph()

    assert nx.is_isomorphic(g, nx.complete_graph(4))
    a = pari('A')
    expected_normalized_yamada_polynomial = \
        normalize_poly(a**-5 + a**-4 + a**-3 + a**-2 + a**-1 -1 + a - 2*a**2+a**3-a**4+a**5+a**6+a**8)

    yp1 = sgd.yamada_polynomial()

    # assert sgd.yamada_polynomial() == expected_normalized_yamada_polynomial