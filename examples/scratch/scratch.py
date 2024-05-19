import numpy as np
from yamada import SpatialGraph
from yamada import normalize_yamada_polynomial
from cypari import pari

np.random.seed(0)



a = pari('A')

n = 1  # 6
for i in range(n):
    np.random.seed(i)

    sg = SpatialGraph(nodes=['a', 'b', 'c'],
                      node_positions=np.array([[0, 0.5, 0], [-1, 0.5, 1], [1, 0, 0]]),
                      edges=[('a', 'b'), ('b', 'c'), ('c', 'a')])
    sg.project()
    sgd = sg.create_spatial_graph_diagram()

    assert sgd.normalized_yamada_polynomial() == normalize_yamada_polynomial(-a ** 2 - a - 1)
