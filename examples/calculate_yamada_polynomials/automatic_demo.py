import numpy as np
from yamada.projection import SpatialGraph


# TODO Debug code for quadrivalent example
# TODO Check more than one cross per edge (i.e., 2 and 3) works

# for i in range(6):
np.random.seed(0)

nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
node_positions = np.array([[0, 0, 0], [1, 0, 0], [0.5, 1, 0], [0.5, 0.5, 0], [0.25,0.75,0], [0.75,0.75,0], [0,1,0], [1,1,0]])
edges = [('a', 'b'), ('a', 'g'), ('a', 'd'), ('b', 'd'), ('b', 'h'), ('d', 'e'), ('d', 'f'), ('e', 'c'), ('f', 'c'), ('g', 'c'), ('h', 'c')]

sg1 = SpatialGraph(nodes=nodes,
                   node_positions=node_positions,
                   edges=edges)
sg1.project()
sg1.plot()
sgd1 = sg1.create_spatial_graph_diagram()
yamada_polynomial_infinity_symbol = sgd1.yamada_polynomial()
print("Infinity Symbol Yamada Polynomial:", yamada_polynomial_infinity_symbol)







