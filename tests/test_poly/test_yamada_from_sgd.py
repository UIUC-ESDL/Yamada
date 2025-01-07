import networkx as nx
from cypari import pari
from yamada import has_cut_edge, remove_valence_two_vertices, h_poly, SpatialGraphDiagram, Vertex, Edge, \
    Crossing, normalize_poly

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

    assert sgd.calculate_yamada_polynomial() == h_poly(t)

    assert sgd.yamada_polynomial() == normalize_poly(-a ** 4 - a ** 3 - 2 * a ** 2 - a - 1)

def test_yamada_polynomial_unknotted_theta_graph_2():

    a = pari('A')

    va, vb = Vertex(3, 'A'), Vertex(3, 'B')
    vc, vd = Vertex(2, 'C'), Vertex(2, 'D')

    va[1] = vc[0]
    va[0] = vb[1]
    va[2] = vd[0]

    vb[0] = vc[1]
    vb[2] = vd[1]

    sgd = SpatialGraphDiagram([va, vb, vc, vd])

    assert sgd.yamada_polynomial() == normalize_poly(-a ** 4 - a ** 3 - 2 * a ** 2 - a - 1)

def test_unknot_single_twist_1():

    a = pari('A')

    x1 = Crossing('X')

    x1[0], x1[2] = x1[1], x1[3]

    sgd = SpatialGraphDiagram([x1])

    assert sgd.yamada_polynomial() == (-a ** 2 - a - 1)

def test_unknot_single_twist_2():

    a = pari('A')

    x1 = Crossing('X')

    x1[1], x1[3] = x1[2], x1[0]

    sgd = SpatialGraphDiagram([x1])

    assert sgd.yamada_polynomial() == (-a ** 2 - a - 1)

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

    assert sgd.yamada_polynomial() == normalize_poly(
        a ** 12 - a ** 8 - a ** 6 - a ** 4 - a ** 3 - a ** 2 - a - 1)

# TODO FIX NUMBER ORDER 3 NODE
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
        normalize_poly(a**-5 + a**-4 + a**-3 + a**-2 + a**-1 -1 + a - 2*a**2+a**3-a**4+a**5+a**6+a**8)

    assert sgd.yamada_polynomial() == expected_normalized_yamada_polynomial