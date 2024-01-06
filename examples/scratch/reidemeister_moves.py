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

print('Has R3?', sgd.has_r3()[0])



def r3(face):
    pass


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


def find_opposite_edge(crossing, face):
    for entrypoint in face:
        if isinstance(entrypoint.vertex, Edge):
            crossing_adjacent = [adjacent[0] for adjacent in keep_crossing.adjacent]
            if entrypoint.vertex not in crossing_adjacent:
                return entrypoint.vertex


def get_index_of_crossing_corner(crossing, corner, opposite_side=False):
    for i in range(4):
        if crossing.adjacent[i][0] == corner:
            if not opposite_side:
                return i
            else:
                return (i+2) % 4
    raise Exception('Corner not found in crossing')



def get_crossing_shift_indices(keep_crossing, remove_crossing1, remove_crossing2):

    edge1 = find_common_edge(keep_crossing, remove_crossing1)
    edge2 = find_common_edge(keep_crossing, remove_crossing2)

    keep_crossing_index_e1 = get_index_of_crossing_corner(keep_crossing, edge1)
    keep_crossing_index_e2 = get_index_of_crossing_corner(keep_crossing, edge2)

    if keep_crossing_index_e1 == (keep_crossing_index_e2-1) % 4:
        shifted_crossing_index_e1 = (keep_crossing_index_e1-1) % 4
        shifted_crossing_index_e2 = (keep_crossing_index_e2+1) % 4
    elif keep_crossing_index_e1 == (keep_crossing_index_e2+1) % 4:
        shifted_crossing_index_e1 = (keep_crossing_index_e1+1) % 4
        shifted_crossing_index_e2 = (keep_crossing_index_e2-1) % 4
    else:
        raise Exception('Edges are not adjacent')

    return shifted_crossing_index_e1, shifted_crossing_index_e2


candidate_face = sgd.has_r3()[1]
candidate_crossings = get_candidate_crossings(candidate_face)

keep_crossing = candidate_crossings[0]
remove_crossing_1 = candidate_crossings[1]
remove_crossing_2 = candidate_crossings[2]

# Define the remove crossing corners, and which are under/over
rc1_0_under = remove_crossing_1.adjacent[0]
rc1_1_over = remove_crossing_1.adjacent[1]
rc1_2_under = remove_crossing_1.adjacent[2]
rc1_3_over = remove_crossing_1.adjacent[3]
rc1_edges = [rc1_0_under, rc1_1_over, rc1_2_under, rc1_3_over]

rc2_0_under = remove_crossing_2.adjacent[0]
rc2_1_over = remove_crossing_2.adjacent[1]
rc2_2_under = remove_crossing_2.adjacent[2]
rc2_3_over = remove_crossing_2.adjacent[3]
rc2_edges = [rc2_0_under, rc2_1_over, rc2_2_under, rc2_3_over]

# Find the edges the keep and each remove crossing have in common
common_edge_1 = find_common_edge(keep_crossing, remove_crossing_1)
common_edge_2 = find_common_edge(keep_crossing, remove_crossing_2)
uncommon_edge = find_opposite_edge(keep_crossing, candidate_face)

# Find the indices of common and uncommon edges
rc1_common_indices = [get_index_of_crossing_corner(remove_crossing_1, common_edge_1, opposite_side=False),
                      get_index_of_crossing_corner(remove_crossing_1, common_edge_1, opposite_side=True)]

rc1_uncommon_indices = [get_index_of_crossing_corner(remove_crossing_1, uncommon_edge, opposite_side=False),
                        get_index_of_crossing_corner(remove_crossing_1, uncommon_edge, opposite_side=True)]

rc2_common_indices = [get_index_of_crossing_corner(remove_crossing_2, common_edge_2, opposite_side=False),
                        get_index_of_crossing_corner(remove_crossing_2, common_edge_2, opposite_side=True)]

rc2_uncommon_indices = [get_index_of_crossing_corner(remove_crossing_2, uncommon_edge, opposite_side=False),
                        get_index_of_crossing_corner(remove_crossing_2, uncommon_edge, opposite_side=True)]

# Delete remove crossing 1, delete remove crossing 2
sgd.remove_crossing(remove_crossing_1)
sgd.remove_crossing(remove_crossing_2)


# Fuse the edges of the keep crossing that are not being shifted by the Reidemeister move
sgd.fuse_edges(remove_crossing_1.adjacent[rc1_common_indices[0]], remove_crossing_1.adjacent[rc1_common_indices[1]])
sgd.fuse_edges(remove_crossing_2.adjacent[rc2_common_indices[0]], remove_crossing_2.adjacent[rc2_common_indices[1]])

# Insert the new crossings





shifted_index1, shifted_index2 = get_crossing_shift_indices(keep_crossing, remove_crossing_1, remove_crossing_2)



# Fuse common edge 1, fuse common edge 2

# Insert new crossing 1, insert new crossing 2
# Keep crossing edge-->shift index, under/over edge -->



# sgd.remove_crossing_fuse_edges(keep_crossing)
# sgd.remove_crossing(remove_crossing_1)

# print('adjacent', remove_crossing_1.adjacent)



