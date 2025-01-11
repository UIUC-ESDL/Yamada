import networkx as nx
from cypari import pari
from yamada import h_poly


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

def test_h_poly_g1():

    g1 = nx.MultiGraph()
    g1.add_nodes_from(['a', 'b', 'c'])
    g1.add_edges_from([('a', 'b'), ('a', 'c'), ('a', 'c'), ('b', 'c')])

    a = pari('A')
    paper_h_poly = -a ** 2 - a - 2 - a ** (-1) - a ** (-2)

    assert h_poly(g1) == paper_h_poly


def test_h_poly_g2():

    g2 = nx.MultiGraph()
    g2.add_nodes_from(['a', 'b', 'c'])
    g2.add_edges_from([('a', 'b'), ('a', 'c'), ('a', 'c'), ('b', 'c'), ('b', 'b')])

    a = pari('A')

    # paper_h_poly = -a**3 - 2*a**2 - 4*a - 4 -4*a**(-1) - 2*a**(-3) - a**(-3)
    expected_h_poly = (a**6 + 2*a**5 + 4*a**4 + 4*a**3 + 4*a**2 + 2*a + 1 )/a**3

    assert h_poly(g2) == expected_h_poly

def test_h_poly_g3():

    g3 = nx.MultiGraph()
    g3.add_nodes_from(['a', 'b', 'c'])
    g3.add_edges_from([('a', 'b'), ('a', 'b'), ('a', 'c'), ('b', 'c'), ('b', 'c')])

    a = pari('A')

    # paper_h_poly = a**3 + 3*a**2 + 7*a + 8 + 7*a**(-1) + 3*a**(-2) + a**(-3)
    expected_h_poly = (a**6 + a**5 + 3*a**4 + 2*a**3 + 3*a**2 + a + 1)/a**3

    assert h_poly(g3) == expected_h_poly


def test_h_poly_g4():

    g4 = nx.MultiGraph()
    g4.add_nodes_from(['a', 'b', 'c', 'd'])
    g4.add_edges_from([('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd'), ('c', 'd')])

    a = pari('A')

    # paper_h_poly = a**3 - 4*a**2 - 10*a + 12 - 10*a**(-1) + 4*a**(-2) - a**(-3)
    expected_h_poly = (a**6 + 2*a**4 + 2*a**2 + 1)/a**3

    assert h_poly(g4) == expected_h_poly


def test_h_poly_g5():

    g5 = nx.MultiGraph()
    g5.add_nodes_from(['a', 'b', 'c', 'd'])
    g5.add_edges_from([('a', 'c'), ('a', 'd'), ('a', 'b'), ('b', 'c'), ('b', 'd'), ('c', 'd'), ('c', 'd')])

    a = pari('A')
    # paper_h_poly = -a**4 - 3*a**3 - 7*a**2 - 8*a - 10 - 8*a**(-1) - 7*a**(-2) - 3*a**(-3) - a**(-4)
    expected_h_poly = (-a**8 - a**7 - 5*a**6 - 4*a**5 -  8*a**4 - 4*a**3 - 5*a**2 - a- 1)/a**4

    assert h_poly(g5) == expected_h_poly