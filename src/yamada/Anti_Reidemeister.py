"""
This module contains functions to apply the anti-Reidemeister moves to a Yamada graph diagram.

An anti-Reidemeister move is a move that is not guaranteed to preserve the Yamada polynomial of a spatial graph diagram.

The anti-Reidemeister moves are as follows:
...
"""

from yamada.diagram_elements import Vertex, Edge, Crossing

# %% Anti-Reidemeister Move

def anti_reidemeister_moves(sgd):
    crossing_labels = [c.label for c in sgd.crossings]
    return crossing_labels

def apply_anti_reidemeister_move(sgd, crossing_label):

    sgd = sgd.copy()

    X = sgd.get_object(crossing_label)

    (A, i), (B, j), (C, k), (D, l) = X.adjacent

    # Currently X[0] = A[i], X[1] = B[j], X[2] = C[k], X[3] = D[l]
    # Increment the edge ordering by one

    X[0] = D[l]
    X[1] = A[i]
    X[2] = B[j]
    X[3] = C[k]

    return sgd




