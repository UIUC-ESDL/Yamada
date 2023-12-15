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

candidate_face = get_candidate_face(faces)
candidate_crossings = get_candidate_crossings(candidate_face)

keep_crossing = candidate_crossings[0]
remove_crossings = candidate_crossings[1:]



# Define a circle
circle = Vertex(2,'circle')
circle[0]=circle[1]








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

