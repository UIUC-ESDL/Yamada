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
    return False, None, None, None

def r2(sgd):

    # Make a copy of the sgd object
    sgd = sgd.copy()

    sgd_has_r2, edge, crossing_a, crossing_b = has_r2(sgd)

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

    Returns: ...
    """

    faces = sgd.faces()
    candidates = []

    for face in faces:
        prerequisite_1, crossings = face_has_3_crossings(face)
        prerequisite_2, reidemeister_edges, other_edges = face_has_double_over_or_under_edge(face)
        if prerequisite_1 and prerequisite_2:
            for reidemeister_edge, other_two_edges in zip(reidemeister_edges, other_edges):
                reidemeister_crossing = find_opposite_crossing(face, reidemeister_edge)
                other_two_crossings = [crossing for crossing in crossings if crossing != reidemeister_crossing]
                other_crossing_1 = other_two_crossings[0]
                other_crossing_2 = other_two_crossings[1]
                other_edge_1 = find_common_edge(reidemeister_crossing, other_crossing_1)
                other_edge_2 = find_common_edge(reidemeister_crossing, other_crossing_2)

                candidate = {'reidemeister crossing': reidemeister_crossing.label,
                             'other crossing 1': other_crossing_1.label,
                             'other crossing 2': other_crossing_2.label,
                             'reidemeister edge': reidemeister_edge.label,
                             'other edge 1': other_edge_1.label,
                             'other edge 2': other_edge_2.label}
                candidates.append(candidate)

    if len(candidates) > 0:
        return True, candidates
    else:
        return False, None


def face_has_3_crossings(face):
    crossings = [entrypoint.vertex for entrypoint in face if isinstance(entrypoint.vertex, Crossing)]
    has_3_crossings = len(crossings) == 3
    return has_3_crossings, crossings

def face_has_double_over_or_under_edge(face):

    edges = [entrypoint.vertex for entrypoint in face if isinstance(entrypoint.vertex, Edge)]
    reidemeister_edges = []
    other_edges = []
    for edge in edges:
        is_double_over_or_under, _ = edge_is_double_over_or_under(edge)
        reidemeister_edge = edge
        other_two_edges = [e for e in edges if e != edge]
        if is_double_over_or_under:
            reidemeister_edges.append(reidemeister_edge)
            other_edges.append(other_two_edges)

    if len(reidemeister_edges) > 0:
        return True, reidemeister_edges, other_edges
    else:
        return False, None, None


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


# TODO VERIFY INPUT IS A VALID FACE

def r3(sgd, reidemeister_crossing, other_crossing_1, other_crossing_2, reidemeister_edge, other_edge_1, other_edge_2):

    # Make a copy of the sgd object
    sgd = sgd.copy()

    # Find the objects given the labels
    keep_crossing = [crossing for crossing in sgd.crossings if crossing.label == reidemeister_crossing][0]
    reidemeister_crossing_1 = [crossing for crossing in sgd.crossings if crossing.label == other_crossing_1][0]
    reidemeister_crossing_2 = [crossing for crossing in sgd.crossings if crossing.label == other_crossing_2][0]
    reidemeister_edge = [edge for edge in sgd.edges if edge.label == reidemeister_edge][0]
    common_edge_1 = [edge for edge in sgd.edges if edge.label == other_edge_1][0]
    common_edge_2 = [edge for edge in sgd.edges if edge.label == other_edge_2][0]


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