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
    candidate_faces = []
    candidate_faces_edges = []

    for face in faces:
        prerequisite_1 = face_has_3_crossings(face)
        prerequisite_2, candidate_face_edges = face_has_double_over_or_under_edge(face)
        if prerequisite_1 and prerequisite_2:
            candidate_faces.append(face)
            candidate_faces_edges.append(candidate_face_edges)

    if len(candidate_faces) > 0:
        return True, candidate_faces, candidate_faces_edges
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
            candidate_edges.append(edge)

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


def r3():
    pass



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