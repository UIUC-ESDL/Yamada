#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# TODO Add


# e1, e2, e3, e4, e5, e6 = Edge(1), Edge(2), Edge(3), Edge(4), Edge(5), Edge(6)
#
# v1 = Vertex(degree=2, label="v1")
# v2 = Vertex(degree=2, label="v2")
# v3 = Vertex(degree=2, label="v3")
# v4 = Vertex(degree=2, label="v4")
# v5 = Vertex(degree=2, label="v5")
# v6 = Vertex(degree=2, label="v6")
#
# x1 = Crossing("x1")

# Test 2E 2V
# e1[0] = v1[0]
# e1[1] = v2[0]
# e2[0] = v1[1]
# e2[1] = v2[1]
# sgd = SpatialGraphDiagram([e1, e2, v1, v2])

# # Test 3E 3V
# e1[0] = v1[0]
# v1[1] = e2[0]
# e2[1] = v2[0]
# v2[1] = e3[0]
# e3[1] = v3[0]
# v3[1] = e1[1]
# sgd = SpatialGraphDiagram([e1, e2, e3, v1, v2, v3])


# # Test 4E 3V 1C
# e1[0] = x1[0]
# e1[1] = v1[0]
# v1[1] = e2[0]
# e2[1] = v2[0]
# v2[1] = e3[0]
# e3[1] = x1[1]
# x1[3] = e4[0]
# e4[1] = x1[2]
# sgd = SpatialGraphDiagram([e1, e2, e3, e4, v1, v2, x1])
# sgd.normalized_yamada_polynomial()



# test 4
# e1[0] = v5[0]  # e1[0] = x1[0]
# e1[1] = v1[0]
# v1[1] = e2[0]
# e2[1] = v2[0]
# v2[1] = e3[0]
# e3[1] = v5[1]  # e3[1] = x1[1]
# v6[0] = e4[0]  # x1[3] = e4[0]
# e2[1] = x1[0]  # e4[1] = x1[2]
# sgd = SpatialGraphDiagram([e1, e2, e3, e4, e5, e6, v1, v2, v2, v3, v4, v5, v6])

