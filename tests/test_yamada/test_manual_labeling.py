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


def test_h_poly_1():
    g = nx.barbell_graph(3, 0)
    assert h_poly(g) == 0


def test_h_poly_2():
    a = pari('A')
    assert h_poly(nx.MultiGraph([(0, 0)])) == (a ** 2 + a + 1) / a


def test_h_poly_3():
    a = pari('A')
    assert h_poly(nx.MultiGraph([(0, 1), (1, 2), (2, 0)])) == (a ** 2 + a + 1) / a


def test_h_poly_4():
    a = pari('A')
    g = nx.MultiGraph([(0, 0), (0, 0)])
    assert -h_poly(g) == (a ** 4 + 2 * a ** 3 + 3 * a ** 2 + 2 * a + 1) / a ** 2


def test_h_poly_5():
    a = pari('A')
    theta = nx.MultiGraph(3 * [(0, 1)])
    assert -h_poly(theta) == (a ** 4 + a ** 3 + 2 * a ** 2 + a + 1) / a ** 2

def test_h_poly_6():
    a = pari('A')
    g = nx.MultiGraph([(0, 0), (1, 1)])
    assert h_poly(g) == (a ** 4 + 2 * a ** 3 + 3 * a ** 2 + 2 * a + 1) / a ** 2


def test_h_poly_7():
    a = pari('A')
    g = nx.MultiGraph([(0, 1), (0, 1), (2, 3), (2, 3), (0, 2), (1, 3)])
    assert h_poly(g) == (a ** 6 + a ** 5 + 3 * a ** 4 + 2 * a ** 3 + 3 * a ** 2 + a + 1) / a ** 3

#
# def test_h_poly_g1():
#     g1 = nx.MultiGraph()
#     g1.add_nodes_from(['a', 'b', 'c'])
#     g1.add_edges_from([('a', 'b'), ('a', 'c'), ('a', 'c'), ('b', 'c')])
#
#     a = pari('A')
#     paper_h_poly = -a ** 2 - a - 2 - a ** (-1) - a ** (-2)
#
#     assert h_poly(g1) == paper_h_poly
#
#
# def test_h_poly_g2():
#     """
#     The graph G2 from Drobrynin and Vesnin.
#
#     TODO Verify that the paper's solution is correct.
#
#     Does the paper's solution contain a typo? The final three terms are -4*a**(-1) - 2*a**(-3) - a**(-3) but
#     the last two terms could be simplified. I believe the middle term should be 2*a**(-2).
#     """
#     g2 = nx.MultiGraph()
#     g2.add_nodes_from(['a', 'b', 'c'])
#     g2.add_edges_from([('a', 'b'), ('a', 'c'), ('a', 'c'), ('b', 'c'), ('b', 'b')])
#
#     a = pari('A')
#     # paper_h_poly = -a**3 - 2*a**2 - 4*a - 4 -4*a**(-1) - 2*a**(-3) - a**(-3)
#     expected_h_poly = -a**3 - 2*a**2 - 4*a - 4 -4*a**(-1) - 2*a**(-2) - a**(-3)
#
#     assert h_poly(g2) == expected_h_poly
#
#
# def test_h_poly_g3():
#     """
#     The graph G3 from Drobrynin and Vesnin.
#     TODO Figure out why solution does not match the paper's solution.
#     """
#     g3 = nx.MultiGraph()
#     g3.add_nodes_from(['a', 'b', 'c'])
#     g3.add_edges_from([('a', 'b'), ('a', 'b'), ('a', 'c'), ('b', 'c'), ('b', 'c')])
#
#     a = pari('A')
#     paper_h_poly = a**3 + 3*a**2 + 7*a + 8 + 7*a**(-1) + 3*a**(-2) + a**(-3)
#
#     assert h_poly(g3) == paper_h_poly
#
#
# def test_h_poly_g4():
#     """
#     The graph G4 from Drobrynin and Vesnin.
#
#     TODO Figure out why solution does not match the paper's solution.
#     """
#
#     g4 = nx.MultiGraph()
#     g4.add_nodes_from(['a', 'b', 'c', 'd'])
#     g4.add_edges_from([('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd'), ('c', 'd')])
#
#     a = pari('A')
#     paper_h_poly = -a**4 - 3*a**3 - 7*a**2 - 8*a - 10 - 8*a**(-1) - 7*a**(-2) - 3*a**(-3) - a**(-4)
#
#     assert h_poly(g4) == paper_h_poly
#
# def test_h_poly_g5():
#     """
#     The graph G5 from Drobrynin and Vesnin which contains two quadrivalent vertices
#
#     TODO Figure out why solution does not match the paper's solution.
#     """
#
#     g5 = nx.MultiGraph()
#     g5.add_nodes_from(['a', 'b', 'c', 'd'])
#     g5.add_edges_from([('a', 'c'), ('a', 'd'), ('a', 'b'), ('b', 'c'), ('b', 'd'), ('c', 'd'), ('c', 'd')])
#
#     a = pari('A')
#     paper_h_poly = -1*a**4 - 3*a**3 - 7*a**2 - 8*a - 10 - 8*a**(-1) - 7*a**(-2) - 3*a**(-3) - a**(-4)
#
#     assert h_poly(g5) == paper_h_poly



def test_spatial_graph_diagram_unknotted_theta_graph_1():
    va, vb = Vertex(3, 'a'), Vertex(3, 'b')
    e0, e1, e2 = Edge(0), Edge(1), Edge(2)
    va[0], va[1], va[2] = e0[0], e1[0], e2[0]
    vb[0], vb[1], vb[2] = e0[1], e2[1], e1[1]
    sgd = SpatialGraphDiagram([va, vb, e0, e1, e2])

    assert len(sgd.crossings) == 0
    assert len(sgd.vertices) == 2

    g = sgd.projection_graph()
    t = nx.MultiGraph(3 * [(0, 1)])

    assert nx.is_isomorphic(remove_valence_two_vertices(g), t)


def test_spatial_graph_diagram_unknotted_theta_graph_2():
    va, vb = Vertex(3, 'a'), Vertex(3, 'b')
    e0, e1, e2 = Edge(0), Edge(1), Edge(2)
    va[0], va[1], va[2] = e0[0], e1[0], e2[0]
    vb[0], vb[1], vb[2] = e0[1], e2[1], e1[1]
    sgd = SpatialGraphDiagram([va, vb, e0, e1, e2])

    g = sgd.projection_graph()
    t = nx.MultiGraph(3 * [(0, 1)])

    assert nx.is_isomorphic(remove_valence_two_vertices(g), t)


def test_yamada_polynomial_unknotted_theta_graph_1():
    a = pari('A')

    va, vb = Vertex(3, 'a'), Vertex(3, 'b')
    e0, e1, e2 = Edge(0), Edge(1), Edge(2)
    va[0], va[1], va[2] = e0[0], e1[0], e2[0]
    vb[0], vb[1], vb[2] = e0[1], e2[1], e1[1]
    sgd = SpatialGraphDiagram([va, vb, e0, e1, e2])

    t = nx.MultiGraph(3 * [(0, 1)])

    assert sgd.yamada_polynomial() == h_poly(t)

    assert sgd.normalized_yamada_polynomial() == normalize_yamada_polynomial(-a ** 4 - a ** 3 - 2 * a ** 2 - a - 1)


def test_yamada_polynomial_infinity_symbol_1():
    a = pari('A')
    x1 = Crossing('X')
    x1[0], x1[2] = x1[1], x1[3]
    sgd = SpatialGraphDiagram([x1])
    assert sgd.normalized_yamada_polynomial() == normalize_yamada_polynomial(-a ** 2 - a - 1)


def test_yamada_polynomial_infinity_symbol_2():
    a = pari('A')
    x1 = Crossing('X')
    x1[1], x1[3] = x1[2], x1[0]
    sgd = SpatialGraphDiagram([x1])
    assert sgd.normalized_yamada_polynomial() == normalize_yamada_polynomial(-a ** 2 - a - 1)


def test_yamada_polynomial_theta_2_graph():
    """
    The Theta_2 graph from Drobrynin and Vesnin
    """

    a = pari('A')

    va, vb = Vertex(3, 'a'), Vertex(3, 'b')
    x, y, z = [Crossing(L) for L in 'XYZ']
    va[0], va[1], va[2] = x[0], vb[2], y[1]
    vb[0], vb[1] = x[3], z[0]
    x[1], x[2] = y[0], z[1]
    y[2], y[3] = z[3], z[2]
    sgd = SpatialGraphDiagram([va, vb, x, y, z])
    g = sgd.underlying_graph()
    t = nx.MultiGraph(3 * [(0, 1)])

    assert nx.is_isomorphic(g, t)

    assert sgd.normalized_yamada_polynomial() == normalize_yamada_polynomial(
        a ** 12 - a ** 8 - a ** 6 - a ** 4 - a ** 3 - a ** 2 - a - 1)


def test_yamada_polynomial_omega_2_graph():
    """
    The Omega_2 graph from Drobrynin and Vesnin:
    """

    a = pari('A')

    va, vb, vc, vd = [Vertex(3, L) for L in 'abcd']
    x, y, z = [Crossing(L) for L in 'XYZ']
    va[0], va[1], va[2] = vd[0], vb[2], x[2]
    vb[0], vb[1] = vc[0], x[3]
    vc[1], vc[2] = vd[2], z[0]
    vd[1] = z[1]
    x[0], x[1] = y[3], y[2]
    y[0], y[1] = z[3], z[2]
    sgd = SpatialGraphDiagram([va, vb, vc, vd, x, y, z])
    g = sgd.underlying_graph()

    assert nx.is_isomorphic(g, nx.complete_graph(4))

    expected_normalized_yamada_polynomial = \
        normalize_yamada_polynomial(a**-5 + a**-4 + a**-3 + a**-2 + a**-1 -1 + a - 2*a**2+a**3-a**4+a**5+a**6+a**8)

    assert sgd.normalized_yamada_polynomial() == expected_normalized_yamada_polynomial





# TODO Implement tests for get_coefficients_and_exponents

def test_reverse_poly():
    """

    """

    a = pari('A')

    assert reverse_poly(a ** -1 + 2) == a + 2

# TODO Implement tests for normalize_poly
# def test_normalize_poly():
