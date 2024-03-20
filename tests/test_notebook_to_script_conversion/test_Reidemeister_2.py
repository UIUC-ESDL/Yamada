#!/usr/bin/env python
# coding: utf-8

# In[5]:


from cypari import pari
from yamada import SpatialGraphDiagram, Vertex, Crossing, Edge, has_r2, apply_r2


# ## Reidemeister 2
# 
# Infinity symbol
# 
# The point of this isn't to rest R2, it's a test to verify remove crossing and fuse edges
# 
# ![R2 Move](./images/r2_infinity.png)

# In[6]:


# def pre_remove_crossing_fuse_edges():
#     e0 = Edge('e0')
#     e1 = Edge('e1')
#     x0 = Crossing('x0')
#     e0[0] = x0[0]
#     e0[1] = x0[3]
#     e1[0] = x0[1]
#     e1[1] = x0[2]
#     sgd = SpatialGraphDiagram([e0, e1, x0])
#     return sgd
# 
# def post_remove_crossing_fuse_edges():
#     e0 = Edge('e0')
#     e1 = Edge('e1')
#     v0 = Vertex(2, 'v0')
#     v1 = Vertex(2, 'v1')
# 
#     e0[0] = v0[0]
#     e0[1] = v1[0]
#     e1[0] = v0[1]
#     e1[1] = v1[1]
# 
#     sgd = SpatialGraphDiagram([e0, e1, v0, v1])
#     return sgd

# def test_remove_crossing_fuse_edges():
#     # TODO Implement for remove crossing fuse edges directly, not the R2 move
#     # TODO Also visualize the Vertices...
#     pass
#     # sgd = pre_remove_crossing_fuse_edges()
#     # sgd = r2(sgd)
#     # expected = post_remove_crossing_fuse_edges()
#     # assert sgd == expected


# ## Reidemeister 2
# 
# ![R2 Move](./images/r2_1.png)
# 

# In[7]:


def test_r2():
    
    a = pari('A')

    expected = -a**2 - a -1

    x1 = Crossing('x1')
    x2 = Crossing('x2')

    x1[0] = x2[2]
    x1[1] = x2[1]
    x1[2] = x1[3]
    x2[0] = x2[3]

    sgd = SpatialGraphDiagram([x1, x2])

    yp_before = sgd.normalized_yamada_polynomial()

    sgd_has_r2, r2_input = has_r2(sgd)
    
    assert sgd_has_r2

    sgd = apply_r2(sgd, r2_input)

    yp_after = sgd.normalized_yamada_polynomial()

    assert yp_before == yp_after

    assert yp_after == expected

