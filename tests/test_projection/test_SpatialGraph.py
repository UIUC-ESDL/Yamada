#!/usr/bin/env python
# coding: utf-8

# 

# In[3]:


import numpy as np
from yamada.projection import SpatialGraph
from yamada.calculation import Vertex, Edge, Crossing, SpatialGraphDiagram, h_poly, reverse_poly, normalize_yamada_polynomial

np.random.seed(0)


# ## Verifying cylic ordering of vertices
# 
# ![Abstract Graph G5](./images/abstract_graph_G5.png)

# In[4]:


def test_cyclic_node_ordering_vertex():

    nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    node_positions = np.array([[0, 0, 0], [1, 0, 0], [0.5, 1, 0], [0.5, 0.5, 0], [0.25,0.75, 0], [0.75, 0.75, 0], [0, 1, 0], [1, 1, 0]])

    edges = [('a', 'b'), ('a', 'g'), ('a', 'd'), ('b', 'd'), ('b', 'h'), ('d', 'e'), ('d', 'f'), ('e', 'c'), ('f', 'c'), ('g', 'c'), ('h', 'c')]

    sg = SpatialGraph(nodes=nodes,
                      node_positions=node_positions,
                      edges=edges)

    sg.project()

    order = sg.cyclic_node_ordering_vertex('c')
    expected_order = {'c': {'e': 3, 'f': 0, 'g': 2, 'h': 1}}

    assert order == expected_order

