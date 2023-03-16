#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
from yamada.projection import SpatialGraph
from yamada.calculation import normalize_yamada_polynomial
from cypari import pari

np.random.seed(0)


# ## Calculate the Yamada polynomial of the unknot
# 
# 
# ![Infinity Symbol](./images/unknot/unknot.png)

# In[3]:


def test_unknot():

    a = pari('A')

    for i in range(6):
        np.random.seed(i)

        sg = SpatialGraph(nodes=['a', 'b', 'c'],
                          node_positions=np.array([[0, 0.5, 0], [-1, 0.5, 1], [1, 0, 0]]),
                          edges=[('a', 'b'), ('b', 'c'), ('c', 'a')])
        sg.project()
        sgd = sg.create_spatial_graph_diagram()

        assert sgd.normalized_yamada_polynomial() == normalize_yamada_polynomial(-a ** 2 - a - 1)


# ## The Unknot with a single twist (infinity symbol)
# 
# ![Infinity Symbol](./images/unknot/infinity_symbol_version_2.png)

# In[4]:


def test_unknot_single_twist():

    a = pari('A')

    for i in range(6):

        np.random.seed(0)

        sg = SpatialGraph(nodes=['a', 'b', 'c', 'd'],
                          node_positions=np.array([[0, 0.5, 0], [1, 0.5, 1], [1, 0, 0], [0, 0, 1]]),
                          edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a')])
        sg.project()
        sgd = sg.create_spatial_graph_diagram()

        assert sgd.normalized_yamada_polynomial() == normalize_yamada_polynomial(-a ** 2 - a - 1)


# ## The Unknot with a double twist
# 
# ![Unknot](./images/unknot/Unknot_double_twist.png)

# In[5]:


def test_unknot_double_twist():

    a = pari('A')

    for i in range(6):
        np.random.seed(i)
        sg1 = SpatialGraph(nodes=['a', 'b', 'c', 'd', 'e', 'f'],
                           node_positions=np.array([[0, 0.5, 0], [1, 0, 1], [2, 0.5, 0], [3, 0, 1], [1, 1, 0], [-1, 0, 1]]),
                           edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'f'), ('f', 'a')])
        sg1.project()
        sgd1 = sg1.create_spatial_graph_diagram()

        assert sgd1.normalized_yamada_polynomial() == normalize_yamada_polynomial(-a ** 2 - a - 1)


# ## The Unknot with four crossings along one edge
# 
# The example tests to ensure that the calculator correctly handles the cyclic ordering of vertices and crossings so that it preserves the topology of the unknot.
# 
# ![Unknot with four crossings](./images/unknot/unknot_four_crossings.png)

# In[6]:


def test_unknot_four_crossings():

    nodes = ['a', 'b', 'c', 'd', 'e','f','g']
    node_positions = np.array([[0,0,0], [1,1,2], [2,0,0], [3,1,2], [4,0,0],[4,0,1],[0,0,1]])
    edges = [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'f'), ('f', 'g'), ('g','a')]

    sg = SpatialGraph(nodes=nodes,
                      node_positions=node_positions,
                      edges=edges)

    sg.project()

    sgd = sg.create_spatial_graph_diagram()

    a = pari('A')

    assert sgd.normalized_yamada_polynomial() == normalize_yamada_polynomial(-a ** 2 - a - 1)


# 

# In[7]:


def test_double_crossing_single_edge():
    # TODO Implement this test.
    pass


# 

# In[8]:


def test_triple_crossing_single_edge():
    # TODO Implement this test.
    pass


# 

# In[9]:


def test_quadrivalent_node():
    pass


# 

# 
