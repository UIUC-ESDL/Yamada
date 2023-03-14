#!/usr/bin/env python
# coding: utf-8

# ## Pytest Examples

# ## Importing the necessary functions

# In[24]:


import networkx as nx
from cypari import pari
from yamada.calculation import has_cut_edge, remove_valence_two_vertices, h_poly, SpatialGraphDiagram, Vertex, Edge, \
    Crossing, reverse_poly, normalize_yamada_polynomial


# ## H Polynomials
# 
# 

# 

# In[ ]:


def test_h_poly_1():
    g = nx.barbell_graph(3, 0)
    assert h_poly(g) == 0


# 

# In[ ]:


def test_h_poly_2():
    a = pari('A')
    assert h_poly(nx.MultiGraph([(0, 0)])) == (a ** 2 + a + 1) / a


# 

# In[ ]:


def test_h_poly_3():
    a = pari('A')
    assert h_poly(nx.MultiGraph([(0, 1), (1, 2), (2, 0)])) == (a ** 2 + a + 1) / a


# 

# In[ ]:


def test_h_poly_4():
    a = pari('A')
    g = nx.MultiGraph([(0, 0), (0, 0)])
    assert -h_poly(g) == (a ** 4 + 2 * a ** 3 + 3 * a ** 2 + 2 * a + 1) / a ** 2


# 

# In[ ]:


def test_h_poly_5():
    a = pari('A')
    theta = nx.MultiGraph(3 * [(0, 1)])
    assert -h_poly(theta) == (a ** 4 + a ** 3 + 2 * a ** 2 + a + 1) / a ** 2


# 

# In[ ]:


def test_h_poly_6():
    a = pari('A')
    g = nx.MultiGraph([(0, 0), (1, 1)])
    assert h_poly(g) == (a ** 4 + 2 * a ** 3 + 3 * a ** 2 + 2 * a + 1) / a ** 2


# 

# In[ ]:


def test_h_poly_7():
    a = pari('A')
    g = nx.MultiGraph([(0, 1), (0, 1), (2, 3), (2, 3), (0, 2), (1, 3)])
    assert h_poly(g) == (a ** 6 + a ** 5 + 3 * a ** 4 + 2 * a ** 3 + 3 * a ** 2 + a + 1) / a ** 3


# ## Abstract Graph G1
# 
# ![Abstract Graph G1](./images/abstract_graph_G1.png)

# In[25]:


def test_h_poly_g1():
    g1 = nx.MultiGraph()
    g1.add_nodes_from(['a', 'b', 'c'])
    g1.add_edges_from([('a', 'b'), ('a', 'c'), ('a', 'c'), ('b', 'c')])

    a = pari('A')
    paper_h_poly = -a ** 2 - a - 2 - a ** (-1) - a ** (-2)

    assert h_poly(g1) == paper_h_poly


# ## Abstract Graph G2
# 
# ![Abstract Graph G2](./images/abstract_graph_G2.png)

# 

# In[26]:


def test_h_poly_g2():
    """
    The graph G2 from Drobrynin and Vesnin.

    TODO Verify that the paper's solution is correct.

    Does the paper's solution contain a typo? The final three terms are -4*a**(-1) - 2*a**(-3) - a**(-3) but
    the last two terms could be simplified. I believe the middle term should be 2*a**(-2).
    """
    g2 = nx.MultiGraph()
    g2.add_nodes_from(['a', 'b', 'c'])
    g2.add_edges_from([('a', 'b'), ('a', 'c'), ('a', 'c'), ('b', 'c'), ('b', 'b')])

    a = pari('A')
    # paper_h_poly = -a**3 - 2*a**2 - 4*a - 4 -4*a**(-1) - 2*a**(-3) - a**(-3)
    expected_h_poly = -a**3 - 2*a**2 - 4*a - 4 -4*a**(-1) - 2*a**(-2) - a**(-3)

    assert h_poly(g2) == expected_h_poly


# ## Abstract Graph G3
# 
# ![Abstract Graph G3](./images/abstract_graph_G3.png)

# In[27]:


def test_h_poly_g3():
    """
    The graph G3 from Drobrynin and Vesnin.
    TODO Figure out why solution does not match the paper's solution.
    """
    g3 = nx.MultiGraph()
    g3.add_nodes_from(['a', 'b', 'c'])
    g3.add_edges_from([('a', 'b'), ('a', 'b'), ('a', 'c'), ('b', 'c'), ('b', 'c')])

    a = pari('A')
    paper_h_poly = a**3 + 3*a**2 + 7*a + 8 + 7*a**(-1) + 3*a**(-2) + a**(-3)

    assert h_poly(g3) == paper_h_poly


# ## Abstract Graph G4
# 
# ![Abstract Graph G4](./images/abstract_graph_G4.png)

# In[28]:


def test_h_poly_g4():
    """
    The graph G4 from Drobrynin and Vesnin.

    TODO Figure out why solution does not match the paper's solution.
    """

    g4 = nx.MultiGraph()
    g4.add_nodes_from(['a', 'b', 'c', 'd'])
    g4.add_edges_from([('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd'), ('c', 'd')])

    a = pari('A')
    paper_h_poly = -a**4 - 3*a**3 - 7*a**2 - 8*a - 10 - 8*a**(-1) - 7*a**(-2) - 3*a**(-3) - a**(-4)

    assert h_poly(g4) == paper_h_poly


# ## Abstract Graph G5
# 
# ![Abstract Graph G5](./images/abstract_graph_G5.png)

# In[29]:


def test_h_poly_g5():
    """
    The graph G5 from Drobrynin and Vesnin which contains two quadrivalent vertices

    TODO Figure out why solution does not match the paper's solution.
    """

    g5 = nx.MultiGraph()
    g5.add_nodes_from(['a', 'b', 'c', 'd'])
    g5.add_edges_from([('a', 'c'), ('a', 'd'), ('a', 'b'), ('b', 'c'), ('b', 'd'), ('c', 'd'), ('c', 'd')])

    a = pari('A')
    paper_h_poly = -1*a**4 - 3*a**3 - 7*a**2 - 8*a - 10 - 8*a**(-1) - 7*a**(-2) - 3*a**(-3) - a**(-4)

    assert h_poly(g5) == paper_h_poly

