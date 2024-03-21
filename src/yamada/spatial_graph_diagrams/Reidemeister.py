from itertools import combinations
from .diagram_elements import Vertex, Edge, Crossing
from random import choice

# TODO Remove



# %% Reidemeister 0

# NOT IMPLEMENTED

# %% Reidemeister 1

def has_r1(sgd):
    """
    Criteria:
    1. The diagram must have a crossing.
    2. Two adjacent corners of the crossing must share the same exact edge
       (i.e., the edge forms a loop and nothing is over-laying, under-laying, or poking through that loop).

    Note: Applying the R1 move monotonically simplifies the diagram. Further, since applying the R1 move will change
    the diagram, it might invalidate other identified R1 moves. Therefore, we will only provide the first identified R1.
    """

    sgd_has_r1 = False
    r1_inputs = {}

    for crossing in sgd.crossings:
        (A, i), (B, j), (C, k), (D, l) = crossing.adjacent
        if A == B:
            sgd_has_r1 = True
            r1_inputs['crossing'] = crossing.label
            r1_inputs['edge'] = A.label
            r1_inputs['other_edges'] = [(C.label, k), (D.label, l)]
            break
        elif B == C:
            sgd_has_r1 = True
            r1_inputs['crossing'] = crossing.label
            r1_inputs['edge'] = B.label
            r1_inputs['other_edges'] = [(A.label, i), (D.label, l)]
            break
        elif C == D:
            sgd_has_r1 = True
            r1_inputs['crossing'] = crossing.label
            r1_inputs['edge'] = C.label
            r1_inputs['other_edges'] = [(A.label, i), (B.label, j)]
            break
        elif D == A:
            sgd_has_r1 = True
            r1_inputs['crossing'] = crossing.label
            r1_inputs['edge'] = D.label
            r1_inputs['other_edges'] = [(B.label, j), (C.label, k)]
            break

    return sgd_has_r1, r1_inputs


def apply_r1(sgd, r1_inputs):
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
    sgd.connect_edges(other_edge_1, other_edge_1_index, other_edge_2, other_edge_2_index)

    return sgd

# %% Reidemeister 2

def has_r2(sgd):
    """
    Criteria:
    1. There must exist a pair of crossings that share two common edges.
       (again, the edges form uninterrupted arcs and nothing is over-laying, under-laying, or poking through them).
    2. One of these edges must pass over both crossings, and the other edge must pass under both crossings.

    Note: Applying the R2 move monotonically simplifies the diagram. Further, since applying the R2 move will change
    the diagram, it might invalidate other identified R1 moves. Therefore, we will only provide the first identified R2.
    """

    # Initialize the lists
    sgd_has_r2 = False
    r2_inputs = {}

    # Identify all possible pairs of crossings
    crossing_combinations = list(combinations(sgd.crossings, 2))

    # Loop through each crossing pair
    for crossing1, crossing2 in crossing_combinations:

        # Does the crossing pair share at least two edges?
        common_edges = find_common_edges(crossing1, crossing2)
        if len(common_edges) >= 2:

            pairs_of_common_edges = list(combinations(common_edges, 2))
            for edge1, edge2 in pairs_of_common_edges:
                if edge_is_double_over_or_under(edge1) and edge_is_double_over_or_under(edge2):
                    sgd_has_r2 = True
                    crossing_1_label = crossing1.label
                    crossing_2_label = crossing2.label
                    common_edge_1_crossing_1_index = get_index_of_crossing_corner(crossing1, edge1)
                    common_edge_1_crossing_2_index = get_index_of_crossing_corner(crossing2, edge1)
                    common_edge_2_crossing_1_index = get_index_of_crossing_corner(crossing1, edge2)
                    common_edge_2_crossing_2_index = get_index_of_crossing_corner(crossing2, edge2)
                    common_edge_1_continuation_1_crossing_index = get_index_of_crossing_corner(crossing1, edge1, opposite_side=True)
                    common_edge_1_continuation_2_crossing_index = get_index_of_crossing_corner(crossing2, edge1, opposite_side=True)
                    common_edge_2_continuation_1_crossing_index = get_index_of_crossing_corner(crossing1, edge2, opposite_side=True)
                    common_edge_2_continuation_2_crossing_index = get_index_of_crossing_corner(crossing2, edge2, opposite_side=True)

                    r2_inputs['crossing_1_label'] = crossing_1_label
                    r2_inputs['crossing_2_label'] = crossing_2_label
                    r2_inputs['common_edge_1_crossing_1_index'] = common_edge_1_crossing_1_index
                    r2_inputs['common_edge_1_crossing_2_index'] = common_edge_1_crossing_2_index
                    r2_inputs['common_edge_2_crossing_1_index'] = common_edge_2_crossing_1_index
                    r2_inputs['common_edge_2_crossing_2_index'] = common_edge_2_crossing_2_index
                    r2_inputs['common_edge_1_continuation_1_crossing_index'] = common_edge_1_continuation_1_crossing_index
                    r2_inputs['common_edge_1_continuation_2_crossing_index'] = common_edge_1_continuation_2_crossing_index
                    r2_inputs['common_edge_2_continuation_1_crossing_index'] = common_edge_2_continuation_1_crossing_index
                    r2_inputs['common_edge_2_continuation_2_crossing_index'] = common_edge_2_continuation_2_crossing_index

                    return sgd_has_r2, r2_inputs

    return sgd_has_r2, r2_inputs


def apply_r2(sgd, r2_inputs):
    """
    0. Get the indices
    1. Remove the two crossings
    2. Remove the two common edges
    3. Connect the continuations of the common edges

    Note: Deleting edges can impact labels...
    """

    # Make a copy of the sgd object to avoid modifying the original
    sgd = sgd.copy()

    # Get the inputs
    crossing_1_label = r2_inputs['crossing_1_label']
    crossing_2_label = r2_inputs['crossing_2_label']
    common_edge_1_crossing_1_index = r2_inputs['common_edge_1_crossing_1_index']
    common_edge_1_crossing_2_index = r2_inputs['common_edge_1_crossing_2_index']
    common_edge_2_crossing_1_index = r2_inputs['common_edge_2_crossing_1_index']
    common_edge_2_crossing_2_index = r2_inputs['common_edge_2_crossing_2_index']
    common_edge_1_continuation_1_crossing_index = r2_inputs['common_edge_1_continuation_1_crossing_index']
    common_edge_1_continuation_2_crossing_index = r2_inputs['common_edge_1_continuation_2_crossing_index']
    common_edge_2_continuation_1_crossing_index = r2_inputs['common_edge_2_continuation_1_crossing_index']
    common_edge_2_continuation_2_crossing_index = r2_inputs['common_edge_2_continuation_2_crossing_index']

    # Find the objects given the labels
    crossing_1 = [crossing for crossing in sgd.crossings if crossing.label == crossing_1_label][0]
    crossing_2 = [crossing for crossing in sgd.crossings if crossing.label == crossing_2_label][0]

    # Remove the first crossing and connect the continuations of the common edges
    common_edge_1, common_edge_1_index_1 = crossing_1.adjacent[common_edge_1_crossing_1_index]
    common_edge_1_continuation_1, common_edge_1_continuation_1_index = crossing_1.adjacent[common_edge_1_continuation_1_crossing_index]
    sgd.connect_edges(common_edge_1, common_edge_1_index_1, common_edge_1_continuation_1,
                      common_edge_1_continuation_1_index)

    common_edge_2, common_edge_2_index_1 = crossing_1.adjacent[common_edge_2_crossing_1_index]
    common_edge_2_continuation_1, common_edge_2_continuation_1_index = crossing_1.adjacent[common_edge_2_continuation_1_crossing_index]
    sgd.connect_edges(common_edge_2, common_edge_2_index_1, common_edge_2_continuation_1,
                      common_edge_2_continuation_1_index)

    sgd.remove_crossing(crossing_1)


    # Remove the second crossing and connect the continuations of the common edges
    common_edge_1, common_edge_1_index_2 = crossing_2.adjacent[common_edge_1_crossing_2_index]
    common_edge_1_continuation_2, common_edge_1_continuation_2_index = crossing_2.adjacent[
        common_edge_1_continuation_2_crossing_index]
    sgd.connect_edges(common_edge_1, common_edge_1_index_2, common_edge_1_continuation_2,
                      common_edge_1_continuation_2_index)

    common_edge_2, common_edge_2_index_2 = crossing_2.adjacent[common_edge_2_crossing_2_index]
    common_edge_2_continuation_2, common_edge_2_continuation_2_index = crossing_2.adjacent[common_edge_2_continuation_2_crossing_index]
    sgd.connect_edges(common_edge_2, common_edge_2_index_2, common_edge_2_continuation_2,
                      common_edge_2_continuation_2_index)

    sgd.remove_crossing(crossing_2)

    return sgd


# %% Reidemeister 3

def has_r3(sgd):
    """
    Criteria:
    1. There must be a face with exactly three crossings.
    2. At least one of the edges of the face must pass either fully under or fully over two crossings.

    Note: A face can have more than one possible R3 move.

    Terminology:
    - stationary_crossing: The crossing that is not being moved
    - crossing_edge: The edge that is crossing the stationary crossing
    - moving_crossings (1 & 2): The two crossings connected to the r3_edge and therefore move with it.
    - stationary_edges (1 & 2): The two edges that connect the moving_crossings to the stationary_crossing.
    """

    # Initialize the lists
    sgd_has_r3 = False
    r3_inputs = []

    # Criteria 1: There must be a face with exactly three crossings (i.e., no vertices).
    candidate_faces = []
    for face in sgd.faces():
        if face_has_3_crossings(face):
            candidate_faces.append(face)

    # Criteria 2: At least one of the edges of the face must pass either fully under or fully over two crossings.
    for face in candidate_faces:
        candidate_edges = double_over_or_under_edges(face)
        for candidate_edge in candidate_edges:
            r3_input = {}
            crossings = [entrypoint.vertex for entrypoint in face if isinstance(entrypoint.vertex, Crossing)]

            stationary_crossing = find_opposite_crossing(face, candidate_edge)
            moving_crossings = [crossing for crossing in crossings if crossing != stationary_crossing]
            stationary_edge_1 = find_common_edge(stationary_crossing, moving_crossings[0])
            stationary_edge_2 = find_common_edge(stationary_crossing, moving_crossings[1])

            sgd_has_r3 = True
            r3_input['stationary_crossing'] = stationary_crossing.label
            r3_input['moving_crossing_1'] = moving_crossings[0].label
            r3_input['moving_crossing_2'] = moving_crossings[1].label
            r3_input['crossing_edge'] = candidate_edge.label
            r3_input['stationary_edge_1'] = stationary_edge_1.label
            r3_input['stationary_edge_2'] = stationary_edge_2.label
            r3_inputs.append(r3_input)

    return sgd_has_r3, r3_inputs



def apply_r3(sgd, r3_input):
    """
    We apply the R3 move by sliding the moving crossings along the moving edges, though the stationary crossing,
    and over/under an adjacent stationary crossing edge. Doing so requires us to

    Steps:
    1.
    """

    # Make a copy of the sgd object to avoid modifying the original
    sgd = sgd.copy()

    # Get the inputs
    stationary_crossing_label = r3_input['stationary_crossing']
    moving_crossing_1_label = r3_input['moving_crossing_1']
    moving_crossing_2_label = r3_input['moving_crossing_2']
    crossing_edge_label = r3_input['crossing_edge']
    stationary_edge_1_label = r3_input['stationary_edge_1']
    stationary_edge_2_label = r3_input['stationary_edge_2']

    # Find the objects given the labels
    stationary_crossing = [crossing for crossing in sgd.crossings if crossing.label == stationary_crossing_label][0]
    moving_crossing_1 = [crossing for crossing in sgd.crossings if crossing.label == moving_crossing_1_label][0]
    moving_crossing_2 = [crossing for crossing in sgd.crossings if crossing.label == moving_crossing_2_label][0]
    stationary_edge_1 = [edge for edge in sgd.edges if edge.label == stationary_edge_1_label][0]
    stationary_edge_2 = [edge for edge in sgd.edges if edge.label == stationary_edge_2_label][0]

    # Get the indices of the
    mc1_stationary_edge_index = get_index_of_crossing_corner(moving_crossing_1, stationary_edge_1)
    mc1_stationary_edge_flipside_index = get_index_of_crossing_corner(moving_crossing_1, stationary_edge_1,
                                                                      opposite_side=True)

    mc2_stationary_edge_index = get_index_of_crossing_corner(moving_crossing_2, stationary_edge_2)
    mc2_stationary_edge_flipside_index = get_index_of_crossing_corner(moving_crossing_2, stationary_edge_2,
                                                                      opposite_side=True)

    se1_continuation_mc1, se1_continuation_mc1_index = moving_crossing_1.adjacent[mc1_stationary_edge_flipside_index]

    se1_mc1_index = [i for (edge, i) in moving_crossing_1.adjacent if edge == stationary_edge_1][0]


    # Get the new stationary crossing indices that the moving crossings will connect to
    shifted_index1, shifted_index2 = get_crossing_shift_indices(stationary_crossing,
                                                                moving_crossing_1, moving_crossing_2)

    # Connect the stationary edges with their continuations on the opposite side of the moving crossings
    # Warning this deletes edges, and can disrupt other parts of this code
    # TODO, again, deleting the edge in the first connect impacts the second... fix by indexes and indexing mc adjacent...
    sgd.connect_edges(stationary_edge_1, se1_mc1_index, se1_continuation_mc1, se1_continuation_mc1_index)

    se2_continuation_mc2, se2_continuation_mc2_index = moving_crossing_2.adjacent[mc2_stationary_edge_flipside_index]
    se2_mc2_index = [i for (edge, i) in moving_crossing_2.adjacent if edge == stationary_edge_2][0]

    sgd.connect_edges(stationary_edge_2, se2_mc2_index, se2_continuation_mc2, se2_continuation_mc2_index)

    # Get the edges that connect to the stationary crossing where we will insert the moving crossings
    mc1_new_edge, mc1_new_edge_index = stationary_crossing.adjacent[shifted_index1]
    mc2_new_edge, mc2_new_edge_index = stationary_crossing.adjacent[shifted_index2]

    # Reassign the edges that connect to the stationary crossing to the moving crossings
    moving_crossing_1[mc1_stationary_edge_index] = mc1_new_edge[mc1_new_edge_index]
    moving_crossing_2[mc2_stationary_edge_index] = mc2_new_edge[mc2_new_edge_index]

    # Create two new edges and insert them between the moving crossings and the stationary crossing (post-shift)
    new_edge_1_label = 'ne' + str(len(sgd.edges) + 1)
    new_edge_2_label = 'ne' + str(len(sgd.edges) + 2)
    new_edge_1 = Edge(new_edge_1_label)
    new_edge_2 = Edge(new_edge_2_label)

    sgd.add_edge(new_edge_1,
                 moving_crossing_1, mc1_stationary_edge_flipside_index,
                 stationary_crossing, shifted_index1)

    sgd.add_edge(new_edge_2,
                 moving_crossing_2, mc2_stationary_edge_flipside_index,
                 stationary_crossing, shifted_index2)

    return sgd


def face_has_3_crossings(face):
    crossings = [entrypoint.vertex for entrypoint in face if isinstance(entrypoint.vertex, Crossing)]
    has_3_crossings = len(crossings) == 3
    return has_3_crossings


def double_over_or_under_edges(face):
    edges = [entrypoint.vertex for entrypoint in face if isinstance(entrypoint.vertex, Edge)]
    candidate_edges = []
    for edge in edges:
        if edge_is_double_over_or_under(edge):
            candidate_edges.append(edge)
    return candidate_edges


def edge_is_double_over_or_under(edge):
    edge_adjacent_1 = edge.adjacent[0][0]
    edge_adjacent_2 = edge.adjacent[1][0]

    if not isinstance(edge_adjacent_1, Crossing) or not isinstance(edge_adjacent_2, Crossing):
        return False

    crossing_1 = edge_adjacent_1
    crossing_2 = edge_adjacent_2

    edge_over_crossing_1 = edge_is_over(edge, crossing_1)
    edge_over_crossing_2 = edge_is_over(edge, crossing_2)

    # Double over
    if edge_over_crossing_1 and edge_over_crossing_2:
        return True

    # Double under
    elif not edge_over_crossing_1 and not edge_over_crossing_2:
        return True

    # One over, one under
    else:
        return False


def edge_is_over(edge, crossing):
    """
    Crossing indices 1 and 3 indicate the over edge. Indices 0 and 2 indicate the under edge.
    If an edge is not over, then it must be under. Therefore, we only check for
    one of these two conditions.
    """
    if crossing.adjacent[1][0] == edge or crossing.adjacent[3][0] == edge:
        return True
    else:
        return False

def find_opposite_crossing(face, edge):
    for entrypoint in face:
        if isinstance(entrypoint.vertex, Crossing):
            edge_adjacent = [adjacent[0] for adjacent in edge.adjacent]
            if entrypoint.vertex not in edge_adjacent:
                return entrypoint.vertex




def find_common_edge(crossing1, crossing2):
    for adjacent1 in crossing1.adjacent:
        for adjacent2 in crossing2.adjacent:
            if adjacent1[0] == adjacent2[0]:
                return adjacent1[0]

def find_common_edges(crossing1, crossing2):
    common_edges = []
    for adjacent1 in crossing1.adjacent:
        for adjacent2 in crossing2.adjacent:
            if adjacent1[0] == adjacent2[0]:
                common_edges.append(adjacent1[0])

    return common_edges



def get_index_of_crossing_corner(crossing, corner, opposite_side=False):
    for i in range(4):
        if crossing.adjacent[i][0] == corner:
            if not opposite_side:
                return i
            else:
                return (i + 2) % 4
    raise Exception('Corner not found in crossing')


def get_crossing_shift_indices(keep_crossing, remove_crossing1, remove_crossing2):
    edge1 = find_common_edge(keep_crossing, remove_crossing1)
    edge2 = find_common_edge(keep_crossing, remove_crossing2)

    keep_crossing_index_e1 = get_index_of_crossing_corner(keep_crossing, edge1)
    keep_crossing_index_e2 = get_index_of_crossing_corner(keep_crossing, edge2)

    if keep_crossing_index_e1 == (keep_crossing_index_e2 - 1) % 4:
        shifted_crossing_index_e1 = (keep_crossing_index_e1 - 1) % 4
        shifted_crossing_index_e2 = (keep_crossing_index_e2 + 1) % 4
    elif keep_crossing_index_e1 == (keep_crossing_index_e2 + 1) % 4:
        shifted_crossing_index_e1 = (keep_crossing_index_e1 + 1) % 4
        shifted_crossing_index_e2 = (keep_crossing_index_e2 - 1) % 4
    else:
        raise Exception('Edges are not adjacent')

    return shifted_crossing_index_e1, shifted_crossing_index_e2


# %% Reidemeister 4

# NOT IMPLEMENTED

# %% Reidemeister 5

# NOT IMPLEMENTED

# %% Reidemeister 6

# NOT FULLY IMPLEMENTED

def has_r6(sgd):
    for V in sgd.vertices:
        for i in range(V.degree):
            E, e = V.adjacent[i]
            A, a = E.flow(e)
            if isinstance(A, Crossing):
                E, e = V.adjacent[(i + 1) % V.degree]
                B, b = E.flow(e)
                if A == B and (b + 1) % 4 == a:
                    return True
    return False



# %% Reidemeister Simplification

def r1_and_r2_simplify(sgd, r1_count, r2_count):
    max_iter = 100
    i = 0
    sgd_has_r1 = True
    sgd_has_r2 = True
    while sgd_has_r1 and sgd_has_r2:

        sgd_has_r1, r1_inputs = has_r1(sgd)
        if sgd_has_r1:
            sgd = apply_r1(sgd, r1_inputs)
            r1_count += 1

        sgd_has_r2, r2_inputs = has_r2(sgd)
        if sgd_has_r2:
            sgd = apply_r2(sgd, r2_inputs)
            r2_count += 1

        if i > max_iter:
            raise ValueError(f"R1 and R2 simplification has been looping for {i} times. This is likely an error.")

        i += 1

    return sgd, r1_count, r2_count

def reidemeister_simplify(sgd, n_tries=10):

    # Make a copy of the sgd object
    sgd = sgd.copy()

    # Initialize the counts
    total_r1_count = 0
    total_r2_count = 0
    total_r3_count = 0

    # Check for any initial moves that will monotonically simplify the diagram
    sgd, r1_count, r2_count = r1_and_r2_simplify(sgd, total_r1_count, total_r2_count)
    total_r1_count += r1_count
    total_r2_count += r2_count

    # Perform Reidemeister 3 moves to see if they set up any R1 or R2 moves
    for i in range(n_tries):
        sgd_has_r3, r3_inputs = has_r3(sgd)
        if sgd_has_r3:
            # Pick a random candidate
            r3_input = choice(r3_inputs)
            sgd = apply_r3(sgd, r3_input)
            total_r3_count += 1

            # Check for any R1 or R2 moves that will monotonically simplify the diagram
            sgd, r1_count, r2_count = r1_and_r2_simplify(sgd, total_r1_count, total_r2_count)
            total_r1_count += r1_count
            total_r2_count += r2_count
        else:
            break

    return sgd, total_r1_count, total_r2_count, total_r3_count
