import numpy as np
from yamada.projection import SpatialGraph

# Problems, what about 3 nodes?
# Check quadrivalent nodes
# Check double crossings on single edge

# for i in range(6):
np.random.seed(0)


# sg1 = SpatialGraph(nodes=['a', 'b', 'c'],
#                    node_positions=np.array([[0, 0.5, 0], [-1, 0.5, 1], [1, 0, 0]]),
#                    edges=[('a', 'b'), ('b', 'c'), ('c', 'a')])
# sg1.project()
# sg1.plot()
# sgd1 = sg1.create_spatial_graph_diagram()
# yamada_polynomial_infinity_symbol = sgd1.yamada_polynomial()
# print("Infinity Symbol Yamada Polynomial:", yamada_polynomial_infinity_symbol)







# Making it -1 0.5 1 breaks it

sg1 = SpatialGraph(nodes=['a', 'b', 'c','d'],
                   node_positions=np.array([[0, 0.5, 0], [1, 0.5, 1], [1, 0, 0], [0, 0, 1]]),
                   edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a')])
sg1.project()
sg1.plot()
sgd1 = sg1.create_spatial_graph_diagram()
yamada_polynomial_infinity_symbol = sgd1.yamada_polynomial()
print("Infinity Symbol Yamada Polynomial:", yamada_polynomial_infinity_symbol)







