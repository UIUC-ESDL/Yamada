"""
This module contains functions to apply the anti-Reidemeister moves to a Yamada graph diagram.

An anti-Reidemeister move is a move that is not guaranteed to preserve the Yamada polynomial of a spatial graph diagram.

The anti-Reidemeister moves are as follows:
...
"""

from yamada.diagram_elements import Vertex, Edge, Crossing

# %% Anti-Reidemeister Move

def has_anti_r1(sgd):
    """
    Criteria:
    1. The diagram must have a crossing.
    """

    sgd_has_anti_r1 = False
    anti_r1_inputs = []

    for crossing in sgd.crossings:
        (A, i), (B, j), (C, k), (D, l) = crossing.adjacent
        sgd_has_anti_r1 = True
        anti


        if A == B:
            sgd_has_anti_r1 = True
            anti_r1_inputs['crossing'] = crossing.label
            anti_r1_inputs['edge'] = A.label
            anti_r1_inputs['other_edges'] = [(C.label, k), (D.label, l)]
            break
        elif B == C:
            sgd_has_anti_r1 = True
            anti_r1_inputs['crossing'] = crossing.label
            anti_r1_inputs['edge'] = B.label
            anti_r1_inputs['other_edges'] = [(A.label, i), (D.label, l)]
            break
        elif C == D:
            sgd_has_anti_r1 = True
            anti_r1_inputs['crossing'] = crossing.label
            anti_r1_inputs['edge'] = C.label
            anti_r1_inputs['other_edges'] = [(A.label, i), (B.label, j)]
            break
        elif D == A:
            sgd_has_anti_r1 = True
            anti_r1_inputs['crossing'] = crossing.label
            anti_r1_inputs['edge'] = D.label
            anti_r1_inputs['other_edges'] = [(B.label, j), (C.label, k)]
            break

    return sgd_has_anti_r1, anti_r1_inputs

def apply_anti_r1(sgd, r1_inputs):
    """
    1. Remove the crossing.
    2. Remove the edge that two adjacent crossing corners share.
    3. Connect the edges from the other two crossing corners.
    """

    # Make a copy of the sgd object to avoid modifying the original
    sgd = sgd.copy()

    # Get the inputs
    crossing_label = r1_inputs['crossing']
    edge_label = r1_inputs['edge']
    other_edge_labels_and_indices = r1_inputs['other_edges']

    # Find the SGD objects associated with the given labels
    crossing = [crossing for crossing in sgd.crossings if crossing.label == crossing_label][0]
    edge = [edge for edge in sgd.edges if edge.label == edge_label][0]
    other_edge_1_label, other_edge_1_index = other_edge_labels_and_indices[0]
    other_edge_2_label, other_edge_2_index = other_edge_labels_and_indices[1]
    other_edge_1 = [edge for edge in sgd.edges if edge.label == other_edge_1_label][0]
    other_edge_2 = [edge for edge in sgd.edges if edge.label == other_edge_2_label][0]

    # Remove the crossing
    sgd.remove_crossing(crossing)

    # Remove the shared edge
    sgd.remove_edge(edge)

    # Connect the remaining edges
    sgd.connect(other_edge_1, other_edge_1_index, other_edge_2, other_edge_2_index)

    return sgd


# Apply multiple ani-R moves to the diagram