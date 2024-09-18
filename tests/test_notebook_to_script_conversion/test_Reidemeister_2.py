#!/usr/bin/env python
# coding: utf-8

# In[5]:


from cypari import pari
from yamada import SpatialGraphDiagram, Vertex, Crossing, Edge, has_r2, apply_r2


# ## Reidemeister 2
# 
# ![R2 Move](./images/r2_1.png)
# 

# In[7]:


def test_r2():
    
    a = pari('A')

    yp_ground_truth = -a**2 - a -1

    x1 = Crossing('x1')
    x2 = Crossing('x2')

    x1[0] = x2[2]
    x1[1] = x2[1]
    x1[2] = x1[3]
    x2[0] = x2[3]

    sgd = SpatialGraphDiagram([x1, x2])

    yp_before = sgd.normalized_yamada_polynomial()
    
    assert yp_before == yp_ground_truth

    r2_crossing_labels = has_r2(sgd)
    
    assert len(r2_crossing_labels) == 1
    assert ('x1', 'x2') in r2_crossing_labels or ('x2', 'x1') in r2_crossing_labels

    sgd = apply_r2(sgd, ('x1', 'x2'))

    yp_after = sgd.normalized_yamada_polynomial()

    assert yp_after == yp_ground_truth


# ![R2 Move](./images/r2_double_loop_same.jpg)
# 

# In[ ]:


def test_r2_2():
    
    a = pari('A')

    yp_ground_truth = -a**2 - a -1

    x1 = Crossing('x1')
    x2 = Crossing('x2')
    x3 = Crossing('x3')
    x4 = Crossing('x4')

    e1, e2, e3, e4, e5, e6, e7, e8  = Edge(1), Edge(2), Edge(3), Edge(4), Edge(5), Edge(6), Edge(7), Edge(8)

    # x1
    x1[0] = e8[0]
    x1[1] = e2[0]
    x1[2] = e1[0]
    x1[3] = e1[1]
    
    # x2
    x2[0] = e7[1]
    x2[1] = e2[1]
    x2[2] = e8[1]
    x2[3] = e3[0]
    
    # x3
    x3[0] = e6[1]
    x3[1] = e4[0]
    x3[2] = e7[0]
    x3[3] = e3[1]
    
    # x4
    x4[0] = e5[1]
    x4[1] = e4[1]
    x4[2] = e6[0]
    x4[3] = e5[0]

    sgd = SpatialGraphDiagram([x1, x2, x3, x4, e1, e2, e3, e4, e5, e6, e7, e8])

    yp_before_r2s = sgd.normalized_yamada_polynomial()

    assert yp_before_r2s == yp_ground_truth
    
    # Remove the first loop
    
    r2_crossing_labels = has_r2(sgd)
    
    assert len(r2_crossing_labels) == 3  # I intended it to be 2, but since both loops are on the same side, the edge 3 can also be treated as a loop.
    assert ('x1', 'x2') in r2_crossing_labels or ('x2', 'x1') in r2_crossing_labels
    
    sgd = apply_r2(sgd, ('x1', 'x2'))
    
    yp_after_first_r2 = sgd.normalized_yamada_polynomial()
    
    assert yp_after_first_r2 == yp_ground_truth
    
    # Remove the second loop
    
    r2_crossing_labels = has_r2(sgd)
    
    assert len(r2_crossing_labels) == 1
    assert ('x3', 'x4') in r2_crossing_labels or ('x4', 'x3') in r2_crossing_labels
    
    sgd = apply_r2(sgd, ('x3', 'x4'))
    
    yp_after_second_r2 = sgd.normalized_yamada_polynomial()
    
    assert yp_after_second_r2 == yp_ground_truth
    
    r2_crossing_labels = has_r2(sgd)
    
    assert len(r2_crossing_labels) == 0


# ![R2 Move](./images/r2_double_loop_opposite.jpg)
# 

# In[ ]:


def test_r2_3():
    
    a = pari('A')

    yp_ground_truth = -a**2 - a -1

    x1 = Crossing('x1')
    x2 = Crossing('x2')
    x3 = Crossing('x3')
    x4 = Crossing('x4')

    e1, e2, e3, e4, e5, e6, e7, e8  = Edge(1), Edge(2), Edge(3), Edge(4), Edge(5), Edge(6), Edge(7), Edge(8)

    # x1
    x1[0] = e8[0]
    x1[1] = e2[0]
    x1[2] = e1[0]
    x1[3] = e1[1]
    
    # x2
    x2[0] = e7[1]
    x2[1] = e2[1]
    x2[2] = e8[1]
    x2[3] = e3[0]
    
    # x3
    x3[0] = e3[1]
    x3[1] = e6[1]
    x3[2] = e4[0]
    x3[3] = e7[0]
    
    # x4
    x4[0] = e5[0]
    x4[1] = e5[1]
    x4[2] = e4[1]
    x4[3] = e6[0]

    sgd = SpatialGraphDiagram([x1, x2, x3, x4, e1, e2, e3, e4, e5, e6, e7, e8])

    yp_before_r2s = sgd.normalized_yamada_polynomial()

    assert yp_before_r2s == yp_ground_truth
    
    # Remove the first loop
    
    r2_crossing_labels = has_r2(sgd)
    
    assert len(r2_crossing_labels) == 2
    assert ('x1', 'x2') in r2_crossing_labels or ('x2', 'x1') in r2_crossing_labels
    
    sgd = apply_r2(sgd, ('x1', 'x2'))
    
    yp_after_first_r2 = sgd.normalized_yamada_polynomial()
    
    assert yp_after_first_r2 == yp_ground_truth
    
    # Remove the second loop
    
    r2_crossing_labels = has_r2(sgd)
    
    assert len(r2_crossing_labels) == 1
    assert ('x3', 'x4') in r2_crossing_labels or ('x4', 'x3') in r2_crossing_labels
    
    sgd = apply_r2(sgd, ('x3', 'x4'))
    
    yp_after_second_r2 = sgd.normalized_yamada_polynomial()
    
    assert yp_after_second_r2 == yp_ground_truth
    
    r2_crossing_labels = has_r2(sgd)
    
    assert len(r2_crossing_labels) == 0

