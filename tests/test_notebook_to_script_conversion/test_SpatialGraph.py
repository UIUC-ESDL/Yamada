#!/usr/bin/env python
# coding: utf-8

# 

# In[6]:


import numpy as np
from yamada import SpatialGraph
from yamada import Vertex, Edge, Crossing, SpatialGraphDiagram, h_poly, reverse_poly, normalize_yamada_polynomial

np.random.seed(0)


# ## Verifying the cyclic ordering of nodes for a vertex
# 
# ![Abstract Graph G5](./images/abstract_graph_G5.png)

# In[7]:


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


# ## Verify the cyclic ordering of nodes for a crossing

# In[7]:





# ## Divide edges into sub-edges
# 
# ![Infinity Symbol](./images/infinity_symbol.png)
# 
# 

# In[8]:


sg = SpatialGraph(nodes=['a', 'b', 'c', 'd'],
                  node_positions=np.array([[0, 0.5, 0], [1, 0.5, 1], [1, 0, 0], [0, 0, 1]]),
                  edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a')])
sg.project()

sep = sg.get_sub_edges()

expected_sub_edges = [('b', 'c0'), ('c0', 'a'), ('b', 'c'), ('d', 'c0'), ('c0', 'c'), ('d', 'a')]
# ['b', '0', 'a']

assert sep == expected_sub_edges


# In[8]:




