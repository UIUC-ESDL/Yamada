from cypari import pari
from yamada import SpatialGraphDiagram, Vertex, Edge, Crossing

a = pari('A')

# R3: Infinity symbol and circle

def pre_r3():

    x0 = Crossing('x0')
    x1 = Crossing('x1')
    x2 = Crossing('x2')
    x3 = Crossing('x3')
    x4 = Crossing('x4')

    x0[0] = x2[3]
    x0[1] = x1[1]
    x0[2] = x3[3]
    x0[3] = x4[1]

    x1[0] = x3[0]
    x1[2] = x2[2]
    x1[3] = x3[1]

    x2[0] = x4[0]
    x2[1] = x4[3]
    x3[2] = x4[2]

    sgd = SpatialGraphDiagram([x0, x1, x2, x3, x4])

    return sgd

def post_r3():

        x0 = Crossing('x0')
        x1 = Crossing('x1')
        x2 = Crossing('x2')
        x5 = Crossing('x5')
        x6 = Crossing('x6')

        x0[0] = x6[1]
        x0[1] = x5[3]
        x0[2] = x1[3]
        x0[3] = x2[1]

        x1[0] = x5[2]
        x1[1] = x5[1]
        x1[2] = x2[2]

        x2[0] = x6[2]
        x2[3] = x6[3]

        x5[0] = x6[0]

        sgd = SpatialGraphDiagram([x0, x1, x2, x5, x6])

        return sgd


sgd = pre_r3()

# sgd_post = post_r3()

print('Before R3:', sgd.normalized_yamada_polynomial())

print('Has R3?', sgd.has_r3())

faces = sgd.faces()

def has_3_crossings(face):

    crossings = 0
    entrypoints = face
    for entrypoint in entrypoints:
        if isinstance(entrypoint.vertex, Crossing):
            crossings += 1

    return crossings == 3

def has_r3(sgd):
    faces = sgd.faces()
    for face in faces:
        requirement_1 = has_3_crossings(face)
        requirement_2 = has_double_over_or_under_edge(face)
        if requirement_1 and requirement_2:
            return True
    return False

def face_has_r3(faces):
    for face in faces:
        requirement_1 = has_3_crossings(face)
        requirement_2 = has_double_over_or_under_edge(face)
        if requirement_1 and requirement_2:
            return True
    return False

def has_double_over_or_under_edge(face):
    has_double_over_or_under_edge = False
    entrypoints = face
    for entrypoint in entrypoints:
        if isinstance(entrypoint.vertex, Edge):
            if edge_is_double_over_or_under(entrypoint.vertex):
                has_double_over_or_under_edge = True

    return has_double_over_or_under_edge

def edge_is_double_over_or_under(edge):
    crossings = edge.adjacent
    if len(crossings) != 2:
        raise Exception('Edge is not adjacent to exactly two crossings')
    if both_under_or_over(edge, crossings[0][0], crossings[1][0]) == 'both under':
        return True
    elif both_under_or_over(edge, crossings[0][0], crossings[1][0]) == 'both over':
        return True
    else:
        return False


def under_or_over(edge, crossing):
    if crossing.adjacent[0][0] == edge or crossing.adjacent[2][0] == edge:
        return 'under'
    elif crossing.adjacent[1][0] == edge or crossing.adjacent[3][0] == edge:
        return 'over'
    else:
        raise Exception('Edge not adjacent to crossing')

def both_under_or_over(edge, crossing1, crossing2):
    if under_or_over(edge, crossing1) == under_or_over(edge, crossing2):
        return 'both ' + under_or_over(edge, crossing1)
    else:
        return 'neither'



def get_candidate_face(faces):
    candidate_faces = []
    for face in faces:
        if has_3_crossings(face):
            candidate_faces.append(face)

    if len(candidate_faces) == 0:
        return None
    else:
        return candidate_faces[0]

def get_candidate_crossings(face):
    entrypoints = face
    crossings = []
    for entrypoint in entrypoints:
        if isinstance(entrypoint.vertex, Crossing):
            crossings.append(entrypoint.vertex)
    return crossings


def find_common_edge(crossing1, crossing2):
    for adjacent1 in crossing1.adjacent:
        for adjacent2 in crossing2.adjacent:
            if adjacent1[0] == adjacent2[0]:
                return adjacent1[0]


def get_crossing_index(crossing, edge):
    for i in range(4):
        if crossing.adjacent[i][0] == edge:
            return i
    raise Exception('Edge not found in crossing')


def get_crossing_shift_indices(keep_crossing, remove_crossing1, remove_crossing2):

    edge1 = find_common_edge(keep_crossing, remove_crossing1)
    edge2 = find_common_edge(keep_crossing, remove_crossing2)

    keep_crossing_index_e1 = get_crossing_index(keep_crossing, edge1)
    keep_crossing_index_e2 = get_crossing_index(keep_crossing, edge2)

    if keep_crossing_index_e1 == (keep_crossing_index_e2-1) % 4:
        shifted_crossing_index_e1 = (keep_crossing_index_e1-1) % 4
        shifted_crossing_index_e2 = (keep_crossing_index_e2+1) % 4
    elif keep_crossing_index_e1 == (keep_crossing_index_e2+1) % 4:
        shifted_crossing_index_e1 = (keep_crossing_index_e1+1) % 4
        shifted_crossing_index_e2 = (keep_crossing_index_e2-1) % 4
    else:
        raise Exception('Edges are not adjacent')

    return shifted_crossing_index_e1, shifted_crossing_index_e2




candidate_face = get_candidate_face(faces)
candidate_crossings = get_candidate_crossings(candidate_face)

keep_crossing = candidate_crossings[0]
remove_crossing_1 = candidate_crossings[1]
remove_crossing_2 = candidate_crossings[2]

common_edge_1 = find_common_edge(keep_crossing, remove_crossing_1)
common_edge_2 = find_common_edge(keep_crossing, remove_crossing_2)

# sgd.remove_crossing_fuse_edges(keep_crossing)
# sgd.remove_crossing(remove_crossing_1)

# print('adjacent', remove_crossing_1.adjacent)

shifted_index1, shifted_index2 = get_crossing_shift_indices(keep_crossing, remove_crossing_1, remove_crossing_2)

# Define a circle
# circle = Vertex(2,'circle')
# circle[0]=circle[1]








# # print('vertices:', sgd.vertices)
# # print('edges:', sgd.edges)
# # print('crossings:', sgd.crossings)
#
# print('Has R2?', sgd.has_r2())
# sgd.r2()
# print('After R2:', sgd.normalized_yamada_polynomial())
#
# print('Has R2?', sgd.has_r2())
# # print('vertices:', sgd.vertices)
# # print('edges:', sgd.edges)
# # print('crossings:', sgd.crossings)

