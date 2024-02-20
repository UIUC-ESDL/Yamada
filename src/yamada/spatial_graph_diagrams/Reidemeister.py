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
    faces = sgd.faces()
    r3_faces = []
    for face in faces:
        requirement_1 = _face_has_3_crossings(face)
        requirement_2 = _face_has_double_over_or_under_edge(face)
        if requirement_1 and requirement_2:
            r3_faces.append(face)

    if len(r3_faces) > 0:
        return True, r3_faces
    else:
        return False, None


def _face_has_r3(faces):
    for face in faces:
        requirement_1 = _face_has_3_crossings(face)
        requirement_2 = _face_has_double_over_or_under_edge(face)
        if requirement_1 and requirement_2:
            return True
    return False


def _face_has_3_crossings(face):

    crossings = 0
    entrypoints = face
    for entrypoint in entrypoints:
        if isinstance(entrypoint.vertex, Crossing):
            crossings += 1

    return crossings == 3

def _face_has_double_over_or_under_edge(face):
    double_over_or_under_edge = False
    entrypoints = face
    crossings = []
    for entrypoint in entrypoints:
        if isinstance(entrypoint.vertex, Edge):
            if _edge_is_double_over_or_under(entrypoint.vertex):
                double_over_or_under_edge = True

    return double_over_or_under_edge


def _edge_is_double_over_or_under(edge):
    crossings = edge.adjacent
    if len(crossings) != 2:
        raise Exception('Edge is not adjacent to exactly two crossings')

    if _edge_is_both_under_or_over(edge, crossings[0][0], crossings[1][0]) == 'both under':
        return True
    elif _edge_is_both_under_or_over(edge, crossings[0][0], crossings[1][0]) == 'both over':
        return True
    else:
        return False

def _edge_is_both_under_or_over(edge, crossing1, crossing2):
    if _edge_is_under_or_over(edge, crossing1) == _edge_is_under_or_over(edge, crossing2):
        return 'both ' + _edge_is_under_or_over(edge, crossing1)
    else:
        return 'neither'

def _edge_is_under_or_over(edge, crossing):
    if crossing.adjacent[0][0] == edge or crossing.adjacent[2][0] == edge:
        return 'under'
    elif crossing.adjacent[1][0] == edge or crossing.adjacent[3][0] == edge:
        return 'over'
    else:
        raise Exception('Edge not adjacent to crossing')

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