#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from cypari import pari
from yamada import Edge, Crossing, Vertex, SpatialGraphDiagram
from yamada.Reidemeister import has_r1, apply_r1, has_r2, apply_r2 
from yamada.Anti_Reidemeister import anti_reidemeister_moves, apply_anti_reidemeister_move


# # Anti-Reidemeister Moves
# 
# ## Check one: Unknot-to-unknot
# 
# If we take an unknot and twist it to form an infinity symbol then it will have one crossing. If we untwist it, and then twist it in the opposite direction we will also get an infinity symbol with one crossing. Swapping the crossing order should switch between the two. All three should have the unknot Yamada polynomial
# 
# ![R1 Move](./images/unknot_to_unknot_crossing_swap.jpg)

# In[ ]:


def create_unknot_1():
    """Infinity symbol"""

    a = pari('A')

    e1, e2 = Edge(1), Edge(2)
    x1 = Crossing("x1")

    e1[0] = x1[2]
    e1[1] = x1[3]
    e2[0] = x1[1]
    e2[1] = x1[0]

    sgd = SpatialGraphDiagram([e1, e2, x1])

    return sgd

def create_unknot_2():
    """Infinity symbol w/ opposite twist"""

    a = pari('A')

    e1, e2 = Edge(1), Edge(2)
    x1 = Crossing("x1")

    e1[0] = x1[3]
    e1[1] = x1[0]
    e2[0] = x1[2]
    e2[1] = x1[1]

    sgd = SpatialGraphDiagram([e1, e2, x1])

    return sgd

def test_anti_reidemeister_1():
    a = pari('A')

    yp_ground_truth = -a**2 - a - 1
    
    sgd_1 = create_unknot_1()
    sgd_2 = create_unknot_2()
    
    # Ensure both unknots have the same Yamada polynomial
    sgd_1_yp = sgd_1.normalized_yamada_polynomial()
    sgd_2_yp = sgd_2.normalized_yamada_polynomial()
    assert sgd_1_yp == yp_ground_truth
    assert sgd_2_yp == yp_ground_truth
    
    # There should only be one possible crossing swap
    arm = anti_reidemeister_moves(sgd_1)
    assert len(arm) == 1
    assert arm[0] == 'x1'

    # Ensure the crossing swap is correct
    sgd_cs = apply_anti_reidemeister_move(sgd_1, arm[0])
    
    sgd_cs_yp = sgd_cs.normalized_yamada_polynomial()
    assert sgd_cs_yp == yp_ground_truth


# ## Check two: knot-to-unknot
# 
# We define a circle with a figure-eight knot in it. If we apply a crossing swap to the middle crossing, then It should become the unknot. Applying the crossing swap should also make an R2 and then an R1 move possible (which wouldn't affect the Yamada polynomial, but we should make sure that it still is detected and can  be correctly applied)
# 
# ![R1 Move](./images/knot_to_unknot_crossing_swap.jpg)

# 

# In[ ]:


def test_anti_reidemeister_2():
    a = pari('A')

    yp_ground_truth = -a**2 - a - 1
    
    e1, e2, e3, e4, e5, e6 = Edge(1), Edge(2), Edge(3), Edge(4), Edge(5), Edge(6)

    x1, x2, x3 = Crossing("x1"), Crossing("x2"), Crossing("x3")

    x1[0] = e2[1]
    x1[1] = e1[0]
    x1[2] = e4[0]
    x1[3] = e3[1]

    x2[0] = e6[0]
    x2[1] = e2[0]
    x2[2] = e3[0]
    x2[3] = e5[0]

    x3[0] = e5[1]
    x3[1] = e4[1]
    x3[2] = e1[1]
    x3[3] = e6[1]

    sgd = SpatialGraphDiagram([e1, e2, e3, e4, e5, e6, x1, x2, x3])

    
    yp_before = sgd.normalized_yamada_polynomial()
    # TODO Calculate what the Yamada polynomial should be for the original diagram, but we at least knot it should not be the unknot Yamada polynomial
    assert yp_before != yp_ground_truth
    
    arm = anti_reidemeister_moves(sgd)
    
    # There should be 3 possible crossing swaps
    assert len(arm) == 3
    assert set(arm) == {'x1', 'x2', 'x3'}
    
    # Ensure the crossing swap is correct
    sgd = apply_anti_reidemeister_move(sgd, 'x1')
    yp_after = sgd.normalized_yamada_polynomial()
    assert yp_after == yp_ground_truth
    
    # Ensure the R2 move is correct
    sgd_has_r2 = has_r2(sgd)
    assert len(sgd_has_r2) > 0
    sgd = apply_r2(sgd, ("x2", "x3"))
    yp_after_r2 = sgd.normalized_yamada_polynomial()
    assert yp_after_r2 == yp_ground_truth
    sgd_has_r1 = has_r1(sgd)
    assert len(sgd_has_r1) > 0
    sgd = apply_r1(sgd, "x1")
    yp_after_r1 = sgd.normalized_yamada_polynomial()
    assert yp_after_r1 == yp_ground_truth
    

