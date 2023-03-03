import numpy as np
from yamada.projection import SpatialGraph

np.random.seed(0)

# Quadrivalent Example
# TODO Debug code for quadrivalent example

# nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
# node_positions = np.array([[0, 0, 0], [1, 0, 0], [0.5, 1, 0], [0.5, 0.5, 0], [0.25,0.75,0], [0.75,0.75,0], [0,1,0], [1,1,0]])
# edges = [('a', 'b'), ('a', 'g'), ('a', 'd'), ('b', 'd'), ('b', 'h'), ('d', 'e'), ('d', 'f'), ('e', 'c'), ('f', 'c'), ('g', 'c'), ('h', 'c')]
#
# sg1 = SpatialGraph(nodes=nodes,
#                    node_positions=node_positions,
#                    edges=edges)
# sg1.project()
# sg1.plot()
# sgd1 = sg1.create_spatial_graph_diagram()
# print("Yamada Polynomial:", sgd1.yamada_polynomial())


# Double-Crossing Single Edge Example
# TODO Check more than one cross per edge (i.e., 2 and 3) works

nodes = ['a', 'b', 'c', 'd', 'e']
node_positions = np.array([[0,0,0], [1,0,1], [-1,0,1], [-2,0,2], [0,1,3]])
edges = [('a', 'b'), ('a', 'c'), ('a', 'e'), ('c', 'd'), ('c', 'b'), ('d', 'b'), ('e','b')]

sg1 = SpatialGraph(nodes=nodes,
                   node_positions=node_positions,
                   edges=edges)

sg1.project()
sg1.plot()

sgd1 = sg1.create_spatial_graph_diagram()

print("Yamada Polynomial:", sgd1.yamada_polynomial())
