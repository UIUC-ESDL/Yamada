#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from cypari import pari
from yamada import SpatialGraphDiagram, Crossing, Edge




# ## Reidemeister 1
# 

# In[ ]:


def test_r1():
    
    a = pari('A')

    expected = -a**2 - a -1
    
    x1 = Crossing('X')
    x1[1], x1[3] = x1[2], x1[0]
    
    e0, e1 = Edge(0), Edge(1)
    
    e0[0], e0[1] = x1[0], x1[3]
    e1[0], e1[1] = x1[2], x1[1]
    
    sgd = SpatialGraphDiagram([x1, e0, e1])
    
    yp_before = sgd.normalized_yamada_polynomial()
    
    assert sgd.has_r1()
    
    sgd.r1()
    
    yp_after = sgd.normalized_yamada_polynomial()
    
    assert yp_before == yp_after
    
    assert yp_after == expected
    


# ## Reidemeister 2
# 
# 

# In[ ]:


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
    
    # Ensure 
    assert sgd.has_r2()[0]
    
    sgd.r2()
    
    yp_after = sgd.normalized_yamada_polynomial()
    
    assert yp_before == yp_after
    
    assert yp_after == expected

