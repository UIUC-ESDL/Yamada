#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from yamada.projection import SpatialGraph
from yamada.calculation import normalize_yamada_polynomial
from cypari import pari

np.random.seed(0)


# ## Calculate the Yamada polynomial of the unknot
# 
# 
# ![Infinity Symbol](./images/unknot.png)

# In[2]:


def test_unknot_1():
    a = pari('A')
    sg1 = SpatialGraph(nodes=['a', 'b', 'c'],
                       node_positions=np.array([[0, 0.5, 0], [-1, 0.5, 1], [1, 0, 0]]),
                       edges=[('a', 'b'), ('b', 'c'), ('c', 'a')])
    sg1.project()
    sgd1 = sg1.create_spatial_graph_diagram()
    assert sgd1.normalized_yamada_polynomial() == normalize_yamada_polynomial(-a ** 2 - a - 1)

