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

crossings = sgd.crossings





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

