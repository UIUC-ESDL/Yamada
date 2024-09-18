# from cypari import pari
# from yamada import SpatialGraphDiagram, Vertex, Crossing, Edge, has_r2, apply_r2
#
# a = pari('A')
#
# expected = -a ** 2 - a - 1
#
# x1 = Crossing('x1')
# x2 = Crossing('x2')
# x3 = Crossing('x3')
# x4 = Crossing('x4')
#
# e1, e2, e3, e4, e5, e6, e7, e8 = Edge(1), Edge(2), Edge(3), Edge(4), Edge(5), Edge(6), Edge(7), Edge(8)
#
# # x1
# x1[0] = e8[0]
# x1[1] = e2[0]
# x1[2] = e1[0]
# x1[3] = e1[1]
#
# # x2
# x2[0] = e7[1]
# x2[1] = e2[1]
# x2[2] = e8[1]
# x2[3] = e3[0]
#
# # x3
# x3[0] = e3[1]
# x3[1] = e6[1]
# x3[2] = e4[0]
# x3[3] = e7[0]
#
# # x4
# x4[0] = e5[1]
# x4[1] = e4[1]
# x4[2] = e6[0]
# x4[3] = e5[0]
#
# sgd = SpatialGraphDiagram([x1, x2, x3, x4, e1, e2, e3, e4, e5, e6, e7, e8])
#
# yp_before = sgd.normalized_yamada_polynomial()
#
# # Remove the first loop
#
# sgd_has_r2, r2_input = has_r2(sgd)
#
# assert sgd_has_r2
#
# sgd = apply_r2(sgd, r2_input)
#
# yp_after_1 = sgd.normalized_yamada_polynomial()
#
# assert yp_before == yp_after_1
# assert yp_after_1 == expected
#
# # Remove the second loop
#
# # sgd_has_r2_again, r2_input_again = has_r2(sgd)
#
# # assert sgd_has_r2
#
# # sgd = apply_r2(sgd, r2_input)
# #
# # yp_after_2 = sgd.normalized_yamada_polynomial()
# #
# # assert yp_after_1 == yp_after_2
# # assert yp_after_2 == expected
#
#
# # a = pari('A')
# #
# # expected = -a ** 2 - a - 1
# #
# # x1 = Crossing('x1')
# # x2 = Crossing('x2')
# # x3 = Crossing('x3')
# # x4 = Crossing('x4')
# #
# # e1, e2, e3, e4, e5, e6, e7, e8 = Edge(1), Edge(2), Edge(3), Edge(4), Edge(5), Edge(6), Edge(7), Edge(8)
# #
# # # x1
# # x1[0] = e8[0]
# # x1[1] = e2[0]
# # x1[2] = e1[0]
# # x1[3] = e1[1]
# #
# # # x2
# # x2[0] = e7[1]
# # x2[1] = e2[1]
# # x2[2] = e8[1]
# # x2[3] = e3[0]
# #
# # # x3
# # x3[0] = e6[1]
# # x3[1] = e4[0]
# # x3[2] = e7[0]
# # x3[3] = e3[1]
# #
# # # x4
# # x4[0] = e5[1]
# # x4[1] = e4[1]
# # x4[2] = e6[0]
# # x4[3] = e5[0]
# #
# # sgd = SpatialGraphDiagram([x1, x2, x3, x4, e1, e2, e3, e4, e5, e6, e7, e8])
# #
# # yp_before = sgd.normalized_yamada_polynomial()
# #
# # # Remove the first loop
# #
# # sgd_has_r2, r2_input = has_r2(sgd)
# #
# # assert sgd_has_r2
# #
# # sgd = apply_r2(sgd, r2_input)
# #
# # yp_after_1 = sgd.normalized_yamada_polynomial()
# #
# # assert yp_before == yp_after_1
# # assert yp_after_1 == expected
# #
# # # Remove the second loop
# #
# # sgd_has_r2, r2_input = has_r2(sgd)
# #
# # assert sgd_has_r2
# #
# # sgd = apply_r2(sgd, r2_input)
# #
# # yp_after_2 = sgd.normalized_yamada_polynomial()
# #
# # assert yp_after_1 == yp_after_2
# # assert yp_after_2 == expected