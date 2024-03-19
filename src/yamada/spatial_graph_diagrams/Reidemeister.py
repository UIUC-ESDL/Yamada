from itertools import combinations
from .diagram_elements import Vertex, Edge, Crossing
from random import choice


# %% Reidemeister 0

# NOT IMPLEMENTED

# %% Reidemeister 1

def has_r1(sgd):
    """
    Criteria:
    1. The diagram must have a crossing.
    2. Two adjacent corners of the crossing must share the same exact edge
       (i.e., the edge forms a loop and nothing is over-laying, under-laying, or poking through that loop).
    """

    sgd_has_r1 = False
    r1_crossings = []
    r1_edges = []
    r1_other_edges = []

    for crossing in sgd.crossings:
        (A, i), (B, j), (C, k), (D, l) = crossing.adjacent
        if A == B:
            sgd_has_r1 = True
            r1_crossings.append(crossing.label)
            r1_edges.append(A.label)
            r1_other_edges.append([(C.label, k), (D.label, l)])
        elif B == C:
            sgd_has_r1 = True
            r1_crossings.append(crossing.label)
            r1_edges.append(B.label)
            r1_other_edges.append([(A.label, i), (D.label, l)])
        elif C == D:
            sgd_has_r1 = True
            r1_crossings.append(crossing.label)
            r1_edges.append(C.label)
            r1_other_edges.append([(A.label, i), (B.label, j)])
        elif D == A:
            sgd_has_r1 = True
            r1_crossings.append(crossing.label)
            r1_edges.append(D.label)
            r1_other_edges.append([(B.label, j), (C.label, k)])

    return sgd_has_r1, r1_crossings, r1_edges, r1_other_edges


def apply_r1(sgd, crossing_label, edge_label, other_edges):
    """
    1. Remove the crossing.
    2. Remove the edge that two adjacent crossing corners share.
    3. Connect the edges from the other two crossing corners.
    """

    # Make a copy of the sgd object to avoid modifying the original
    sgd = sgd.copy()

    # Verify that the sgd object has an R1 move
    # Not Implemented for now, may consider this in the future

    # Find the SGD objects associated with the given labels
    crossing = [crossing for crossing in sgd.crossings if crossing.label == crossing_label][0]
    edge = [edge for edge, _ in sgd.edges if edge.label == edge_label][0]
    other_edges = [(edge, i) for edge, i in sgd.edges if edge.label in other_edges]

    # Remove the crossing
    sgd.remove_crossing(crossing)

    # Remove the shared edge
    sgd.remove_edge(edge)

    # Connect the remaining edges
    (A, i), (B, j) = other_edges
    sgd.connect_edges(A, i, B, j)

    return sgd

# %% Reidemeister 2

def has_r2(sgd):
    """
    Criteria:
    1. There must exist a pair of crossings that share two common edges.
       (again, the edges form uninterrupted arcs and nothing is over-laying, under-laying, or poking through them).
    2. One of these edges must pass over both crossings, and the other edge must pass under both crossings.
    """

    # Initialize the lists
    sgd_has_r2 = False
    crossings_pairs = []

    # Identify all possible pairs of crossings
    crossing_combinations = list(combinations(sgd.crossings, 2))

    # Loop through each crossing pair
    for crossing1, crossing2 in crossing_combinations:

        # Does the crossing pair share at least two edges?
        common_edges = find_common_edges(crossing1, crossing2)
        if len(common_edges) >= 2:

            # For good measure, we'll check all pairs of common edges
            # However, we only need to find one pair that satisfies the R2 criteria. The R2 move will effect all edge
            # pairs the same.
            pairs_of_common_edges = list(combinations(common_edges, 2))
            for edge1, edge2 in pairs_of_common_edges:
                if edge_is_double_over_or_under(edge1) and edge_is_double_over_or_under(edge2):
                    sgd_has_r2 = True
                    crossings_pairs.append((crossing1.label, crossing2.label))

    return sgd_has_r2, crossings_pairs


def apply_r2(sgd, crossing_pair):
    """
    1. Find the edges that are on the flip side of the crossings of the common edges.
    2. Find the vertices/crossings that are on the far sides of those edges.
    3. Remove those edges and the common edges.
    4. Delete the crossings
    5. Create two new edges
    6. Connect the new edges to the far side vertices/crossings
    """

    # Make a copy of the sgd object to avoid modifying the original
    sgd = sgd.copy()

    # Verify that the sgd object has an R2 move
    # Not Implemented for now, may consider this in the future

    # Find the objects given the labels
    crossing1 = [crossing for crossing in sgd.crossings if crossing.label == crossing_pair[0]][0]
    crossing2 = [crossing for crossing in sgd.crossings if crossing.label == crossing_pair[1]][0]

    sgd.remove_crossing_connect_opposing_edges(crossing1)
    sgd.remove_crossing_connect_opposing_edges(crossing2)

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
    - moving_edges (1 & 2): The two edges that connect the moving_crossings to the stationary_crossing and therefore move with them.
    """

    # Initialize the lists
    sgd_has_r3 = False
    stationary_crossing = []
    crossing_edge  = []
    moving_crossing_1 = []
    moving_crossing_2 = []
    moving_edge_1 = []
    moving_edge_2 = []

    # Criteria 1: There must be a face with exactly three crossings (i.e., no vertices).
    candidate_faces = []
    for face in sgd.faces():
        if face_has_3_crossings(face):
            candidate_faces.append(face)

    # Criteria 2: At least one of the edges of the face must pass either fully under or fully over two crossings.
    candidate_stationary_crossings = []
    candidate_moving_crossings_1 = []
    candidate_moving_crossings_2 = []
    candidate_crossing_edges = []
    candidate_moving_edges_1 = []
    candidate_moving_edges_2 = []

    for face in candidate_faces:

        candidate_edges = double_over_or_under_edges(face)
        for candidate_edge in candidate_edges:

            crossings = [entrypoint.vertex for entrypoint in face if isinstance(entrypoint.vertex, Crossing)]

            stationary_crossing = find_opposite_crossing(face, candidate_edge)
            moving_crossings = [crossing for crossing in crossings if crossing != stationary_crossing]
            moving_edge_1 = find_opposite_edge(face, moving_crossings[0])
            moving_edge_2 = find_opposite_edge(face, moving_crossings[1])

            candidate_crossing_edges.append(candidate_edge)
            candidate_stationary_crossings.append(stationary_crossing)
            candidate_moving_edges_1.append(moving_edge_1)
            candidate_moving_edges_2.append(moving_edge_2)
            candidate_moving_crossings_1.append(moving_crossings[0])
            candidate_moving_crossings_2.append(moving_crossings[1])

            sgd_has_r3 = True

    return sgd_has_r3, candidate_stationary_crossings, candidate_moving_crossings_1, candidate_moving_crossings_2, candidate_crossing_edges, candidate_moving_edges_1, candidate_moving_edges_2


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
    crossing_1 = edge.adjacent[0][0]
    crossing_2 = edge.adjacent[1][0]
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

def find_opposite_edge(face, crossing):
    for entrypoint in face:
        if isinstance(entrypoint.vertex, Edge):
            crossing_adjacent = [adjacent[0] for adjacent in crossing.adjacent]
            if entrypoint.vertex not in crossing_adjacent:
                return entrypoint.vertex

def find_opposite_crossing(face, edge):
    for entrypoint in face:
        if isinstance(entrypoint.vertex, Crossing):
            edge_adjacent = [adjacent[0] for adjacent in edge.adjacent]
            if entrypoint.vertex not in edge_adjacent:
                return entrypoint.vertex


def r3(sgd, stationary_crossing, moving_crossing_1, moving_crossing_2, r3_edge, moving_edge_1, moving_edge_2):

    # Make a copy of the sgd object to avoid modifying the original
    sgd = sgd.copy()

    # Find the objects given the labels
    keep_crossing = [crossing for crossing in sgd.crossings if crossing.label == stationary_crossing][0]
    reidemeister_crossing_1 = [crossing for crossing in sgd.crossings if crossing.label == moving_crossing_1][0]
    reidemeister_crossing_2 = [crossing for crossing in sgd.crossings if crossing.label == moving_crossing_2][0]
    r3_edge = [edge for edge in sgd.edges if edge.label == r3_edge][0]
    common_edge_1 = [edge for edge in sgd.edges if edge.label == moving_edge_1][0]
    common_edge_2 = [edge for edge in sgd.edges if edge.label == moving_edge_2][0]


    # Find the Reidemeister crossing indices of the common edges, and their continuations on the other sides
    rc1_common_edge_index = get_index_of_crossing_corner(reidemeister_crossing_1, common_edge_1)
    rc1_common_flipside_edge_index = get_index_of_crossing_corner(reidemeister_crossing_1, common_edge_1,
                                                                  opposite_side=True)

    rc2_common_edge_index = get_index_of_crossing_corner(reidemeister_crossing_2, common_edge_2)
    rc2_common_flipside_edge_index = get_index_of_crossing_corner(reidemeister_crossing_2, common_edge_2,
                                                                  opposite_side=True)

    # ...
    kc_rc1_index = get_index_of_crossing_corner(keep_crossing, common_edge_1)
    kc_rc2_index = get_index_of_crossing_corner(keep_crossing, common_edge_2)

    # Remove the edges between the Reidemeister crossings and the keep crossing.
    sgd.remove_edge(common_edge_1)
    sgd.remove_edge(common_edge_2)

    # Connect the Reidemeister crossing flipside edges to the keep crossing
    keep_crossing[kc_rc1_index] = reidemeister_crossing_1.adjacent[rc1_common_flipside_edge_index]
    keep_crossing[kc_rc2_index] = reidemeister_crossing_2.adjacent[rc2_common_flipside_edge_index]

    # Find the shifted indices of the Reidemeister crossings
    shifted_index1, shifted_index2 = get_crossing_shift_indices(keep_crossing, reidemeister_crossing_1,
                                                                reidemeister_crossing_2)

    rc1_new_edge, rc1_new_edge_index = keep_crossing.adjacent[shifted_index1]
    rc2_new_edge, rc2_new_edge_index = keep_crossing.adjacent[shifted_index2]

    reidemeister_crossing_1[rc1_common_edge_index] = rc1_new_edge[rc1_new_edge_index]
    reidemeister_crossing_2[rc2_common_edge_index] = rc2_new_edge[rc2_new_edge_index]

    # Add two new edges
    new_edge_1_label = 'ne' + str(len(sgd.edges) + 1)
    new_edge_2_label = 'ne' + str(len(sgd.edges) + 2)
    new_edge_1 = Edge(new_edge_1_label)
    new_edge_2 = Edge(new_edge_2_label)

    sgd.add_edge(new_edge_1,
                 reidemeister_crossing_1, rc1_common_flipside_edge_index,
                 keep_crossing, shifted_index1)

    sgd.add_edge(new_edge_2,
                 reidemeister_crossing_2, rc2_common_flipside_edge_index,
                 keep_crossing, shifted_index2)


    return sgd


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

def reidemeister_simplify(sgd, num_trys=10):

    # Make a copy of the sgd object
    sgd = sgd.copy()

    r1_count = 0
    r2_count = 0
    r3_count = 0

    def r1_and_r2_simplify(sgdi, r1_counti, r2_counti):
        max_iter = 100
        i=0
        sgd_has_r1 = True
        sgd_has_r2 = True
        while sgd_has_r1 and sgd_has_r2:

            sgd_has_r1, r1_crossings, r1_edges, r1_other_edges = has_r1(sgdi)
            if sgd_has_r1:
                sgdi = apply_r1(sgdi, r1_crossings[0], r1_edges[0], r1_other_edges[0])
                r1_counti += 1

            sgd_has_r2, r2_crossings, _ = has_r2(sgdi)
            if sgd_has_r2:
                sgdi = apply_r2(sgdi, r2_crossings[0])
                r2_counti += 1

            if i > max_iter:
                raise ValueError("R1 and R2 simplification did not converge")

        return sgdi, r1_counti, r2_counti

    # Apply initial simplifications
    sgd, r1_counta, r2_counta = r1_and_r2_simplify(sgd, r1_count, r2_count)
    r1_count += r1_counta
    r2_count += r2_counta

    # Apply Reidemeister 3 moves
    for i in range(num_trys):
        sgd_has_r3, candidates = has_r3(sgd)
        if sgd_has_r3:
            # Pick a random candidate
            candidate = choice(candidates)
            sgd = r3(sgd, candidate['reidemeister crossing'], candidate['other crossing 1'],
                     candidate['other crossing 2'], candidate['reidemeister edge'],
                     candidate['other edge 1'], candidate['other edge 2'])
            r3_count += 1

            sgd, r1_counta, r2_counta = r1_and_r2_simplify(sgd, r1_count, r2_count)
            r1_count += r1_counta
            r2_count += r2_counta
        else:
            break



    # TODO NEED ONE MORE R1
    return sgd, r1_count, r2_count, r3_count
