#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from cypari import pari
from yamada import SpatialGraphDiagram, Crossing, Edge, has_r2, r2


# ## Reidemeister 2
# 
# ![R2 Move](./images/r2_1.png)
# 

# In[1]:


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
    assert has_r2(sgd)[0]

    sgd = r2(sgd)

    yp_after = sgd.normalized_yamada_polynomial()

    assert yp_before == yp_after

    assert yp_after == expected

