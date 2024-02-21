from .diagram_elements import Edge, Crossing

# TODO Do I Need to Return the sgd object?

# %% Reidemeister 0

# NOT IMPLEMENTED

# %% Reidemeister 1

def has_r1(sgd):
    for C in sgd.crossings:
        for i in range(4):
            E, e = C.adjacent[i]
            D, d = E.flow(e)
            if D == C and (i + 1) % 4 == d:
                return True
    return False

def r1(sgd):

    # Make a copy of the sgd object
    sgd = sgd.copy()

    for C in sgd.crossings:
        for i in range(4):
            E, e = C.adjacent[i]
            D, d = E.flow(e)
            if D == C and (i + 1) % 4 == d:

                # Remove crossing and merge edges
                sgd.remove_crossing_fuse_edges(C)

                sgd._merge_edges()

                return sgd

    raise ValueError("No R1 move")

# %% Reidemeister 2

def has_r2(sgd):
    for E in sgd.edges:
        A, a = E.adjacent[0]
        if isinstance(A, Crossing):
            B, b = E.adjacent[1]
            if isinstance(B, Crossing):
                if (a + b) % 2 == 0:
                    return True, E, A, B
    return False

def r2(sgd):

    # Make a copy of the sgd object
    sgd = sgd.copy()

    has_r2, edge, crossing_a, crossing_b = sgd.has_r2()

    sgd.remove_crossing_fuse_edges(crossing_a)
    sgd.remove_crossing_fuse_edges(crossing_b)

    sgd._merge_edges()

    return sgd

# %% Reidemeister 3

def has_r3(sgd):
    """
    Determine if we can apply a Reidemeister 3 move to the given Spatial Graph Diagram (SGD).

    params: sgd: Spatial Graph Diagram

    Prerequisite 1: The SGD has at least one face with 3 crossings
    Prerequisite 2: At least one of the three edges of the face passes
    over or under the other two edges
    """

    faces = sgd.faces()
    candidate_faces_indices = []
    candidate_faces_edges_labels = []

    for i, face in enumerate(faces):
        prerequisite_1 = face_has_3_crossings(face)
        prerequisite_2, candidate_face_edges_labels = face_has_double_over_or_under_edge(face)
        if prerequisite_1 and prerequisite_2:
            candidate_faces_indices.append(i)
            candidate_faces_edges_labels.append(candidate_face_edges_labels)

    if len(candidate_faces_indices) > 0:
        return True, candidate_faces_indices, candidate_faces_edges_labels
    else:
        return False, None, None


def face_has_3_crossings(face):
    crossings = [entrypoint.vertex for entrypoint in face if isinstance(entrypoint.vertex, Crossing)]
    return len(crossings) == 3

def face_has_double_over_or_under_edge(face):

    edges = [entrypoint.vertex for entrypoint in face if isinstance(entrypoint.vertex, Edge)]
    candidate_edges = []
    for edge in edges:
        is_double_over_or_under, _ = edge_is_double_over_or_under(edge)
        if is_double_over_or_under:
            candidate_edges.append(edge.label)

    if len(candidate_edges) > 0:
        return True, candidate_edges
    else:
        return False, None


def edge_is_double_over_or_under(edge):
    crossing_1 = edge.adjacent[0][0]
    crossing_2 = edge.adjacent[1][0]
    edge_over_crossing_1 = edge_is_over(edge, crossing_1)
    edge_over_crossing_2 = edge_is_over(edge, crossing_2)

    if edge_over_crossing_1 and edge_over_crossing_2:
        return True, 'over'
    elif not edge_over_crossing_1 and not edge_over_crossing_2:
        return True, 'under'
    else:
        return False, 'mixed'


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


def r3(sgd, face_index, edge_label):

    # Make a copy of the sgd object
    sgd = sgd.copy()

    face = sgd.faces()[face_index]
    edge = [entrypoint.vertex for entrypoint in face if isinstance(entrypoint.vertex, Edge) and entrypoint.vertex.label == edge_label][0]

    # Label the crossings
    crossings = [entrypoint.vertex for entrypoint in face if isinstance(entrypoint.vertex, Crossing)]
    reidemeister_crossing_1 = edge.adjacent[0][0]
    reidemeister_crossing_2 = edge.adjacent[1][0]
    keep_crossing = [crossing for crossing in crossings if crossing != reidemeister_crossing_1 and crossing != reidemeister_crossing_2][0]

    # Label the edges
    common_edge_1 = find_common_edge(keep_crossing, reidemeister_crossing_1)
    common_edge_2 = find_common_edge(keep_crossing, reidemeister_crossing_2)

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

    # Add Edges?
    # TODO Automate naming
    er1 = Edge('er1')
    er2 = Edge('er2')

    sgd.add_edge(er1,
                 reidemeister_crossing_1, rc1_common_flipside_edge_index,
                 keep_crossing, shifted_index1)

    sgd.add_edge(er2,
                 reidemeister_crossing_2, rc2_common_flipside_edge_index,
                 keep_crossing, shifted_index2)

    return sgd


def find_common_edge(crossing1, crossing2):
    for adjacent1 in crossing1.adjacent:
        for adjacent2 in crossing2.adjacent:
            if adjacent1[0] == adjacent2[0]:
                return adjacent1[0]


def find_opposite_edge(crossing, face):
    for entrypoint in face:
        if isinstance(entrypoint.vertex, Edge):
            crossing_adjacent = [adjacent[0] for adjacent in crossing.adjacent]
            if entrypoint.vertex not in crossing_adjacent:
                return entrypoint.vertex


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