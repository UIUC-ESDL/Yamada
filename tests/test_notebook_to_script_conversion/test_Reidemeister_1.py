#!/usr/bin/env python
# coding: utf-8

# In[1]:


from cypari import pari
from yamada import SpatialGraphDiagram, Crossing, Edge, has_r1, apply_r1


# ## Reidemeister 1
# 
# ![R1 Move](./images/r1_1.png)

# In[2]:


def test_r1_1():
    
    a = pari('A')

    expected = -a**2 - a -1

    x1 = Crossing('X')
    x1[1], x1[3] = x1[2], x1[0]

    e0, e1 = Edge(0), Edge(1)

    e0[0], e0[1] = x1[0], x1[3]
    e1[0], e1[1] = x1[2], x1[1]

    sgd = SpatialGraphDiagram([x1, e0, e1])

    yp_before = sgd.normalized_yamada_polynomial()

    sgd_has_r1, r1_input = has_r1(sgd)

    assert sgd_has_r1

    sgd = apply_r1(sgd, r1_input)

    yp_after = sgd.normalized_yamada_polynomial()

    assert yp_before == yp_after

    assert yp_after == expected


# ![R1 Move](./images/r1_2.png)

# In[3]:


def test_r1_2():
    
    a = pari('A')

    expected = -a**2 - a -1

    x1 = Crossing('X')
    x1[1], x1[3] = x1[2], x1[0]

    sgd = SpatialGraphDiagram([x1])

    yp_before = sgd.normalized_yamada_polynomial()

    sgd_has_r1, r1_input = has_r1(sgd)

    assert sgd_has_r1

    sgd = apply_r1(sgd, r1_input)

    yp_after = sgd.normalized_yamada_polynomial()

    assert yp_before == yp_after

    assert yp_after == expected


# ![R1 Move](./images/r1_double_loop_same_orientation.jpg)

# In[ ]:


def test_r1_3():
    
    a = pari('A')

    expected = -a**2 - a -1

    x1 = Crossing('x1')
    x2 = Crossing('x2')

    e1, e2, e3, e4  = Edge(1), Edge(2), Edge(3), Edge(4)

    x2[3] = e1[0]
    x2[0] = e1[1]
    x2[1] = e2[0]
    x2[2] = e4[1]
    
    x1[2] = e2[1]
    x1[1] = e4[0]
    x1[0] = e3[1]
    x1[3] = e3[0]

    sgd = SpatialGraphDiagram([x1, x2, e1, e2, e3, e4])

    yp_before = sgd.normalized_yamada_polynomial()

    # Remove the first loop

    sgd_has_r1, r1_input = has_r1(sgd)

    assert sgd_has_r1

    sgd = apply_r1(sgd, r1_input)

    yp_after_1 = sgd.normalized_yamada_polynomial()

    assert yp_before == yp_after_1
    assert yp_after_1 == expected
    
    # Remove the second loop
    
    sgd_has_r1, r1_input = has_r1(sgd)
    
    assert sgd_has_r1
    
    sgd = apply_r1(sgd, r1_input)
    
    yp_after_2 = sgd.normalized_yamada_polynomial()
    
    assert yp_after_1 == yp_after_2
    assert yp_after_2 == expected


# ![R1 Move](./images/r1_double_loop_opposite_orientation.jpg)

# In[ ]:


def test_r1_4():
    
    a = pari('A')

    expected = -a**2 - a -1

    x1 = Crossing('x1')
    x2 = Crossing('x2')

    e1, e2, e3, e4  = Edge(1), Edge(2), Edge(3), Edge(4)

    x2[3] = e4[1]
    x2[0] = e1[0]
    x2[1] = e1[1]
    x2[2] = e2[0]
    
    x1[2] = e2[1]
    x1[1] = e4[0]
    x1[0] = e3[1]
    x1[3] = e3[0]

    sgd = SpatialGraphDiagram([x1, x2, e1, e2, e3, e4])

    yp_before = sgd.normalized_yamada_polynomial()

    # Remove the first loop

    sgd_has_r1, r1_input = has_r1(sgd)

    assert sgd_has_r1

    sgd = apply_r1(sgd, r1_input)

    yp_after_1 = sgd.normalized_yamada_polynomial()

    assert yp_before == yp_after_1
    assert yp_after_1 == expected
    
    # Remove the second loop
    
    sgd_has_r1, r1_input = has_r1(sgd)
    
    assert sgd_has_r1
    
    sgd = apply_r1(sgd, r1_input)
    
    yp_after_2 = sgd.normalized_yamada_polynomial()
    
    assert yp_after_1 == yp_after_2
    assert yp_after_2 == expected

