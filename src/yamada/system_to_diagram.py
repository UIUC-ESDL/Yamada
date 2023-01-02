import networkx as nx
from cypari import pari

import string
# Warning snappy
from yamada_polynomials import Edge, Vertex, Crossing, SpatialGraphDiagram, normalize_poly
from snappy.exterior_to_link.link_projection import fig8_points, project_to_diagram
from collections import OrderedDict

alphabet = list(string.ascii_uppercase)


A, B, C, D = [Vertex(3, L) for L in 'ABCD']
X, Y, Z = [Crossing(L) for L in 'XYZ']

A[0], A[1], A[2] = D[0], B[2], X[2]
B[0], B[1] = C[0], X[3]
C[1], C[2] = D[2], Z[0]
D[1] = Z[1]
X[0], X[1] = Y[3], Y[2]
Y[0], Y[1] = Z[3], Z[2]

D = SpatialGraphDiagram([A, B, C, D, X, Y, Z])

d_yamada = normalize_poly(D.yamada_polynomial())

print("Omega-2 Graph Yamada Polynomial:", d_yamada )


# Reference https://github.com/3-manifolds/Spherogram/blob/master/spherogram_src/links/links_base.py#L579

f8 = fig8_points()
d8 = project_to_diagram(f8)
print(d8.PD_code())

# crossings = []
code = d8.PD_code()

# for i, pd_code in enumerate(pd_codes):
#     print('crossing:', pd_code)
#
#     crossings.append(Crossing(alphabet[i]))





C = Crossing('X')

C[0], C[2] = C[1], C[3]

D = SpatialGraphDiagram([C])

print("Infinity Symbol Yamada Polynomial:", D.yamada_polynomial() )










# labels = set()
# for X in code:
#     for i in X:
#         labels.add(i)
#
# gluings = OrderedDict()
#
# for c, X in enumerate(code):
#     for i, x in enumerate(X):
#         if x in gluings:
#             gluings[x].append((c, i))
#         else:
#             gluings[x] = [(c, i)]
#
# if set(len(v) for v in gluings.values()) != set([2]):
#     raise ValueError("PD code isn't consistent")
#
# component_starts = d8._component_starts_from_PD(code, labels, gluings)
#
# crossings = [Crossing(i) for i, d in enumerate(code)]
# for (c, i), (d, j) in gluings.values():
#     crossings[c][i] = crossings[d][j]
#
# sd1 = SpatialGraphDiagram([crossings[0], crossings[1], crossings[2], crossings[3]])

# component_starts = [crossings[c].crossing_strands()[i] for (c, i) in component_starts]






