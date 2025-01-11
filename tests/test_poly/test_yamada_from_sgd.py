import networkx as nx
from cypari import pari
from yamada import has_cut_edge, remove_valence_two_vertices, h_poly, SpatialGraphDiagram, Vertex, Edge, \
    Crossing, normalize_poly

def test_spatial_graph_diagram_unknotted_theta_graph_1(unknotted_theta_graph_1):
    sgd = unknotted_theta_graph_1

    assert len(sgd.crossings) == 0
    assert len(sgd.vertices) == 2

    g = sgd.projection_graph()
    t = nx.MultiGraph(3 * [(0, 1)])

    assert nx.is_isomorphic(remove_valence_two_vertices(g), t)

def test_spatial_graph_diagram_unknotted_theta_graph_2():

    v1, v2 = Vertex(3, 'v1'), Vertex(3, 'v2')

    e1, e2, e3 = Edge(1), Edge(2), Edge(3)

    v1[0], v1[1], v1[2] = e1[0], e2[0], e3[0]
    v2[0], v2[1], v2[2] = e1[1], e3[1], e2[1]

    sgd = SpatialGraphDiagram(edges=[e1, e2, e3], vertices=[v1, v2])

    g = sgd.projection_graph()
    t = nx.MultiGraph(3 * [(0, 1)])

    assert nx.is_isomorphic(remove_valence_two_vertices(g), t)

def test_yamada_polynomial_unknotted_theta_graph_1():

    a = pari('A')

    v1, v2 = Vertex(3, 'v1'), Vertex(3, 'v2')

    e1, e2, e3 = Edge(1), Edge(2), Edge(3)

    v1[0], v1[1], v1[2] = e1[0], e2[0], e3[0]
    v2[0], v2[1], v2[2] = e1[1], e3[1], e2[1]

    sgd = SpatialGraphDiagram(edges=[e1, e2, e3], vertices=[v1, v2])

    t = nx.MultiGraph(3 * [(0, 1)])

    assert sgd.calculate_yamada_polynomial() == h_poly(t)

    assert sgd.yamada_polynomial() == normalize_poly(-a ** 4 - a ** 3 - 2 * a ** 2 - a - 1)

def test_yamada_polynomial_unknotted_theta_graph_2():

    a = pari('A')

    v1 = Vertex(3, 'v1')
    v2 = Vertex(3, 'v2')
    v3 = Vertex(2, 'v3')
    v4 = Vertex(2, 'v4')

    v1[1] = v3[0]
    v1[0] = v2[1]
    v1[2] = v4[0]

    v2[0] = v3[1]
    v2[2] = v4[1]

    sgd = SpatialGraphDiagram(vertices=[v1, v2, v3, v4])

    assert sgd.yamada_polynomial() == normalize_poly(-a ** 4 - a ** 3 - 2 * a ** 2 - a - 1)

def test_unknot_single_twist_1():

    a = pari('A')

    c1 = Crossing('c1')

    c1[0], c1[2] = c1[1], c1[3]

    sgd = SpatialGraphDiagram(crossings=[c1])

    assert sgd.yamada_polynomial() == (-a ** 2 - a - 1)

def test_unknot_single_twist_2():

    a = pari('A')

    c1 = Crossing('c1')

    c1[1], c1[3] = c1[2], c1[0]

    sgd = SpatialGraphDiagram(crossings=[c1])

    assert sgd.yamada_polynomial() == (-a ** 2 - a - 1)

def test_yamada_polynomial_theta_2_graph():
    """
    The Theta_2 graph from Drobrynin and Vesnin
    """

    a = pari('A')

    v1 = Vertex(3, 'v1')
    v2 = Vertex(3, 'v2')

    c1 = Crossing('c1')
    c2 = Crossing('c2')
    c3 = Crossing('c3')

    v1[0], v1[1], v1[2] = c1[0], v2[2], c2[1]
    v2[0], v2[1] = c1[3], c3[0]

    c1[1], c1[2] = c2[0], c3[1]
    c2[2], c2[3] = c3[3], c3[2]
    sgd = SpatialGraphDiagram(vertices=[v1, v2], crossings=[c1, c2, c3])
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

    v1 = Vertex(3, 'v1')
    v2 = Vertex(3, 'v2')
    v3 = Vertex(3, 'v3')
    v4 = Vertex(3, 'v4')
    c1 = Crossing('c1')
    c2 = Crossing('c2')
    c3 = Crossing('c3')
    v1[0], v1[1], v1[2] = v4[0], v2[2], c1[2]
    v2[0], v2[1] = v3[0], c1[3]
    v3[1], v3[2] = v4[2], c3[0]
    v4[1] = c3[1]
    c1[0], c1[1] = c2[3], c2[2]
    c2[0], c2[1] = c3[3], c3[2]
    sgd = SpatialGraphDiagram(vertices=[v1, v2, v3, v4], crossings=[c1, c2, c3])
    g = sgd.underlying_graph()

    assert nx.is_isomorphic(g, nx.complete_graph(4))

    expected_normalized_yamada_polynomial = \
        normalize_poly(a**-5 + a**-4 + a**-3 + a**-2 + a**-1 -1 + a - 2*a**2+a**3-a**4+a**5+a**6+a**8)

    assert sgd.yamada_polynomial() == expected_normalized_yamada_polynomial