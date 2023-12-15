from cypari import pari
from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing

a = pari('A')

# Define a circle
o = Vertex(2, 'o')
e1 = Edge('e1')

o[0] = e1[0]
o[1] = e1[1]

sgd = SpatialGraphDiagram([o, e1])

print(sgd.normalized_yamada_polynomial())

x = Crossing('x')

# TODO How to deal with a single edge twist?
sgd.insert_crossing(x, e1, 0)

print(sgd.normalized_yamada_polynomial())

