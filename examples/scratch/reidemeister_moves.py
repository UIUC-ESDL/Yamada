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

    e0 = Edge('e0')
    e1 = Edge('e1')
    e2 = Edge('e2')
    e3 = Edge('e3')
    e4 = Edge('e4')
    e5 = Edge('e5')
    e6 = Edge('e6')
    e7 = Edge('e7')
    e8 = Edge('e8')
    e9 = Edge('e9')

    x0[0] = e0[0]
    x0[1] = e3[0]
    x0[2] = e2[0]
    x0[3] = e1[0]

    x1[0] = e4[1]
    x1[1] = e0[1]
    x1[2] = e5[0]
    x1[3] = e8[0]

    x2[0] = e5[1]
    x2[1] = e1[1]
    x2[2] = e6[1]
    x2[3] = e8[1]

    x3[0] = e7[1]
    x3[1] = e9[1]
    x3[2] = e6[0]
    x3[3] = e2[1]

    x4[0] = e4[0]
    x4[1] = e9[0]
    x4[2] = e7[0]
    x4[3] = e3[1]

    sgd = SpatialGraphDiagram([x0, x1, x2, x3, x4, e0, e1, e2, e3, e4, e5, e6, e7, e8, e9])

    return sgd


sgd = pre_r3()

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

# TODO Temporarily hardcode candidate face; double check this later.
# candidate_face = sgd.has_r3()[1]
# candidate_crossings = get_candidate_crossings(candidate_face)
faces = sgd.faces()
desired_crossings = ['x0', 'x2', 'x3']
# candidate_face = [face for face in faces if all([entrypoint.vertex.label in desired_crossings for entrypoint in face])]

# Find the face that has all 3 desired crossings
for face in faces:
    entrypoints = [entrypoint.vertex.label for entrypoint in face]
    if all([desired_crossing in entrypoints for desired_crossing in desired_crossings]):
        candidate_face = face
        break

candidate_crossings = get_candidate_crossings(candidate_face)

# keep_crossing = candidate_crossings[0]
# remove_crossing_1 = candidate_crossings[1]
# remove_crossing_2 = candidate_crossings[2]
# TODO Remove hard-coding
keep_crossing = [crossing for crossing in candidate_crossings if crossing.label == 'x0'][0]
reidemeister_crossing_1 = [crossing for crossing in candidate_crossings if crossing.label == 'x2'][0]
reidemeister_crossing_2 = [crossing for crossing in candidate_crossings if crossing.label == 'x3'][0]

# Define the Reidemeister crossing corners, and which are under/over
rc1_0_under = reidemeister_crossing_1.adjacent[0]
rc1_1_over = reidemeister_crossing_1.adjacent[1]
rc1_2_under = reidemeister_crossing_1.adjacent[2]
rc1_3_over = reidemeister_crossing_1.adjacent[3]
rc1_edges = [rc1_0_under, rc1_1_over, rc1_2_under, rc1_3_over]



rc2_0_under = reidemeister_crossing_2.adjacent[0]
rc2_1_over = reidemeister_crossing_2.adjacent[1]
rc2_2_under = reidemeister_crossing_2.adjacent[2]
rc2_3_over = reidemeister_crossing_2.adjacent[3]
rc2_edges = [rc2_0_under, rc2_1_over, rc2_2_under, rc2_3_over]

# Find the edges the keep and each remove crossing have in common
common_edge_1 = find_common_edge(keep_crossing, reidemeister_crossing_1)
common_edge_2 = find_common_edge(keep_crossing, reidemeister_crossing_2)
uncommon_edge = find_opposite_edge(keep_crossing, candidate_face)

# Find the indices of common and uncommon edges
rc1_common_edge_index = get_index_of_crossing_corner(reidemeister_crossing_1, common_edge_1)
rc2_common_edge_index = get_index_of_crossing_corner(reidemeister_crossing_2, common_edge_2)
rc1_common_flipside_edge_index = get_index_of_crossing_corner(reidemeister_crossing_1, common_edge_1, opposite_side=True)
rc2_common_flipside_edge_index = get_index_of_crossing_corner(reidemeister_crossing_2, common_edge_2, opposite_side=True)

# Fuse the edges of the keep crossing that are not being shifted by the Reidemeister move
sgd.fuse_edges(reidemeister_crossing_1.adjacent[rc1_common_edge_index], reidemeister_crossing_1.adjacent[rc1_common_flipside_edge_index])
sgd.fuse_edges(reidemeister_crossing_2.adjacent[rc2_common_edge_index], reidemeister_crossing_2.adjacent[rc2_common_flipside_edge_index])

# Reassign the Reidemeister crossing edges

shifted_index1, shifted_index2 = get_crossing_shift_indices(keep_crossing, reidemeister_crossing_1, reidemeister_crossing_2)


# edge, index = keep_crossing.adjacent[keep/rcx shift index]
# rcx_crossing[rcx common edge index] = edge[index]
# rcx_crossing[rcx common flipside edge index] = keep_crossing[keep/rcx shift index]

rc1_new_edge, rc1_new_edge_index = keep_crossing.adjacent[shifted_index1]
rc2_new_edge, rc2_new_edge_index = keep_crossing.adjacent[shifted_index2]

reidemeister_crossing_1[rc1_common_edge_index] = rc1_new_edge[rc1_new_edge_index]
reidemeister_crossing_2[rc2_common_edge_index] = rc2_new_edge[rc2_new_edge_index]

# Shift the two R3 crossings (commented out while trying to add edges manually)
# reidemeister_crossing_1[rc1_common_flipside_edge_index] = keep_crossing[shifted_index1]
# reidemeister_crossing_2[rc2_common_flipside_edge_index] = keep_crossing[shifted_index2]

# Add Edges?
er1 = Edge('er1')
er2 = Edge('er2')

sgd.add_edge(er1,
             reidemeister_crossing_1, rc1_common_flipside_edge_index,
             keep_crossing, shifted_index1)

sgd.add_edge(er2,
             reidemeister_crossing_2, rc2_common_flipside_edge_index,
             keep_crossing, shifted_index2)

# Is it necessary to merge the vertices?
# sgd._merge_vertices()

yp = sgd.normalized_yamada_polynomial()
print('YP', yp)

