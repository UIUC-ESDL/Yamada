import networkx as nx
from cypari import pari
from yamada import has_cut_edge, remove_valence_two_vertices, h_poly, SpatialGraphDiagram, Vertex, Edge, Crossing, reverse_poly



def test_has_cut_edge_1():
    G = nx.MultiGraph(nx.barbell_graph(3, 0))
    assert has_cut_edge(G)


def test_has_cut_edge_1():
    G = nx.MultiGraph(nx.barbell_graph(3, 0))
    G.add_edge(2, 3)
    assert not has_cut_edge(G)


def test_remove_valence_two_vertices():
    G = nx.MultiGraph([(0, 1), (1, 2), (2, 0)])
    C = remove_valence_two_vertices(G)
    assert list(C.edges()) == [(0, 0)]


def test_h_poly_1():
    G = nx.barbell_graph(3, 0)
    assert h_poly(G) == 0


def test_h_poly_2():
    A = pari('A')
    assert h_poly(nx.MultiGraph([(0, 0)])) == (A ** 2 + A + 1) / A


def test_h_poly_3():
    A = pari('A')
    assert h_poly(nx.MultiGraph([(0, 1), (1, 2), (2, 0)])) == (A ** 2 + A + 1) / A


def test_h_poly_4():
    A = pari('A')
    G = nx.MultiGraph([(0, 0), (0, 0)])
    assert -h_poly(G) == (A**4 + 2*A**3 + 3*A**2 + 2*A + 1)/A**2


def test_h_poly_5():
    A = pari('A')
    theta = nx.MultiGraph(3*[(0, 1)])
    assert -h_poly(theta) == (A**4 + A**3 + 2*A**2 + A + 1)/A**2


def test_h_poly_6():
    A = pari('A')
    G = nx.MultiGraph([(0, 0), (1, 1)])
    assert h_poly(G) == (A**4 + 2*A**3 + 3*A**2 + 2*A + 1)/A**2


def test_h_poly_7():
    A = pari('A')
    G = nx.MultiGraph([(0, 1), (0, 1), (2, 3), (2, 3), (0, 2), (1, 3)])
    assert h_poly(G) == (A**6 + A**5 + 3*A**4 + 2*A**3 + 3*A**2 + A + 1)/A**3


def test_spatial_graph_diagram_unknotted_theta_graph_1():
    a, b = Vertex(3, 'a'), Vertex(3, 'b')
    e0, e1, e2 = Edge(0), Edge(1), Edge(2)
    a[0], a[1], a[2] = e0[0], e1[0], e2[0]
    b[0], b[1], b[2] = e0[1], e2[1], e1[1]
    D = SpatialGraphDiagram([a, b, e0, e1, e2])

    assert len(D.crossings) == 0
    assert len(D.vertices) == 2

    G = D.projection_graph()
    T = nx.MultiGraph(3 * [(0, 1)])

    assert nx.is_isomorphic(remove_valence_two_vertices(G), T)


def test_spatial_graph_diagram_unknotted_theta_graph_2():

    a, b = Vertex(3, 'a'), Vertex(3, 'b')
    e0, e1, e2 = Edge(0), Edge(1), Edge(2)
    a[0], a[1], a[2] = e0[0], e1[0], e2[0]
    b[0], b[1], b[2] = e0[1], e2[1], e1[1]
    D = SpatialGraphDiagram([a, b, e0, e1, e2])

    G = D.projection_graph()
    T = nx.MultiGraph(3 * [(0, 1)])

    assert nx.is_isomorphic(remove_valence_two_vertices(G), T)


def test_yamada_polynomial_unknotted_theta_graph_1():
    a, b = Vertex(3, 'a'), Vertex(3, 'b')
    e0, e1, e2 = Edge(0), Edge(1), Edge(2)
    a[0], a[1], a[2] = e0[0], e1[0], e2[0]
    b[0], b[1], b[2] = e0[1], e2[1], e1[1]
    D = SpatialGraphDiagram([a, b, e0, e1, e2])

    T = nx.MultiGraph(3 * [(0, 1)])

    assert D.yamada_polynomial() == h_poly(T)


def test_yamada_polynomial_infinity_symbol_1():
    A = pari('A')
    C = Crossing('X')
    C[0], C[2] = C[1], C[3]
    D = SpatialGraphDiagram([C])
    assert D.yamada_polynomial() == A**3 + A**2 + A


def test_yamada_polynomial_infinity_symbol_2():
    A = pari('A')
    C = Crossing('X')
    C[1], C[3] = C[2], C[0]
    D = SpatialGraphDiagram([C])
    assert D.yamada_polynomial() == (A**2 + A + 1)/A**3


def test_yamada_polynomial_theta_2_graph():
    """
    The Theta_2 graph from Drobrynin and Vesnin
    """

    A = pari('A')

    a, b = Vertex(3, 'a'), Vertex(3, 'b')
    X, Y, Z = [Crossing(L) for L in 'XYZ']
    a[0], a[1], a[2] = X[0], b[2], Y[1]
    b[0], b[1] = X[3], Z[0]
    X[1], X[2] = Y[0], Z[1]
    Y[2], Y[3] = Z[3], Z[2]
    D = SpatialGraphDiagram([a, b, X, Y, Z])
    G = D.underlying_graph()
    T = nx.MultiGraph(3 * [(0, 1)])

    assert nx.is_isomorphic(G, T)

    assert D.yamada_polynomial() == (A**12 - A**8 - A**6 - A**4 - A**3 - A**2 - A - 1)/A**6


def test_yamada_polynomial_omega_2_graph():
    """
    The Omega_2 graph from Drobrynin and Vesnin:
    """

    A = pari('A')

    a, b, c, d = [Vertex(3, L) for L in 'abcd']
    X, Y, Z = [Crossing(L) for L in 'XYZ']
    a[0], a[1], a[2] = d[0], b[2], X[2]
    b[0], b[1] = c[0], X[3]
    c[1], c[2] = d[2], Z[0]
    d[1] = Z[1]
    X[0], X[1] = Y[3], Y[2]
    Y[0], Y[1] = Z[3], Z[2]
    D = SpatialGraphDiagram([a, b, c, d, X, Y, Z])
    G = D.underlying_graph()
    assert nx.is_isomorphic(G, nx.complete_graph(4))

    assert D.yamada_polynomial() == (A**13 + A**11 + A**10 - A**9 + A**8 - 2*A**7 + A**6 - A**5 + A**4 + A**3 + A**2 + A + 1)/A**5

# TODO Implement tests for get_coefficients_and_exponents

def test_reverse_poly():
    """

    """

    A = pari('A')

    assert reverse_poly(A**-1 + 2) == A + 2

# TODO Implement tests for normalize_poly
# def test_normalize_poly():


