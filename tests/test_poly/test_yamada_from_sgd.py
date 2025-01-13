import networkx as nx
from cypari import pari
from yamada import has_cut_edge, remove_valence_two_vertices, h_poly, SpatialGraphDiagram, Vertex, Edge, \
    Crossing, normalize_poly



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

