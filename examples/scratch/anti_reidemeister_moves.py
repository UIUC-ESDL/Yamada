from cypari import pari
from yamada import Edge, Crossing, Vertex, SpatialGraphDiagram
from yamada.Reidemeister import apply_r1, apply_r2
from yamada.Anti_Reidemeister import anti_reidemeister_moves, apply_anti_reidemeister_move
from yamada.topological_distance import compute_min_distance

def create_sgd1():
    """Infinity symbol"""

    a = pari('A')

    yp_ground_truth = -a ** 2 - a - 1

    e1, e2 = Edge(1), Edge(2)
    x1 = Crossing("x1")

    e1[0] = x1[2]
    e1[1] = x1[3]
    e2[0] = x1[1]
    e2[1] = x1[0]

    sgd = SpatialGraphDiagram([e1, e2, x1])

    return sgd

def create_sgd2():
    """Infinity symbol Opposite Twist"""

    a = pari('A')

    yp_ground_truth = -a ** 2 - a - 1

    e1, e2 = Edge(1), Edge(2)
    x1 = Crossing("x1")

    e1[0] = x1[3]
    e1[1] = x1[0]
    e2[0] = x1[2]
    e2[1] = x1[1]

    sgd = SpatialGraphDiagram([e1, e2, x1])

    return sgd


def create_sgd3():
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

    return sgd

def crossing_swap(sgd, crossing_label):

    sgd = sgd.copy()

    X = sgd.get_object(crossing_label)

    (A, i), (B, j), (C, k), (D, l) = X.adjacent

    # Swap the under-crossing strand and over-crossing strand
    X[0] = D[l]
    X[1] = A[i]
    X[2] = B[j]
    X[3] = C[k]

    return sgd

# Infinity symbol crossing swap
a = pari('A')
yp_ground_truth = -a**2 - a - 1

sgd1 = create_sgd1()
sgd2 = create_sgd2()

print(sgd1.normalized_yamada_polynomial())
print(sgd2.normalized_yamada_polynomial())

sgd3 = crossing_swap(sgd1, "x1")

print(sgd3.normalized_yamada_polynomial())

assert sgd1.normalized_yamada_polynomial() == yp_ground_truth
assert sgd2.normalized_yamada_polynomial() == yp_ground_truth
assert sgd3.normalized_yamada_polynomial() == yp_ground_truth

#

# sgd2 = create_sgd2()
# dist = compute_min_distance(sgd1, sgd2, max_depth=5, max_runtime=30)




