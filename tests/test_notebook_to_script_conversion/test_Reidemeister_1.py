#!/usr/bin/env python
# coding: utf-8

# In[1]:


from cypari import pari
from yamada import SpatialGraphDiagram, Crossing, Edge


# ## Reidemeister 1
# 
# ![R1 Move](./images/r1_1.png)

# In[2]:


def test_r1_1():
    
    a = pari('A')

    # expected = -a**2 - a -1
    # 
    # x1 = Crossing('X')
    # x1[1], x1[3] = x1[2], x1[0]
    # 
    # e0, e1 = Edge(0), Edge(1)
    # 
    # e0[0], e0[1] = x1[0], x1[3]
    # e1[0], e1[1] = x1[2], x1[1]
    # 
    # sgd = SpatialGraphDiagram([x1, e0, e1])
    # 
    # yp_before = sgd.normalized_yamada_polynomial()
    # 
    # assert sgd.has_r1()
    # 
    # sgd.r1()
    # 
    # yp_after = sgd.normalized_yamada_polynomial()
    # 
    # assert yp_before == yp_after
    # 
    # assert yp_after == expected


# ![R1 Move](./images/r1_2.png)

# In[3]:


def test_r1_2():
    
    a = pari('A')

    # expected = -a**2 - a -1
    # 
    # x1 = Crossing('X')
    # x1[1], x1[3] = x1[2], x1[0]
    # 
    # sgd = SpatialGraphDiagram([x1])
    # 
    # yp_before = sgd.normalized_yamada_polynomial()
    # 
    # assert sgd.has_r1()
    # 
    # sgd.r1()
    # 
    # yp_after = sgd.normalized_yamada_polynomial()
    # 
    # assert yp_before == yp_after
    # 
    # assert yp_after == expected

