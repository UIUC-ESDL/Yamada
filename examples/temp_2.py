import numpy as np
from yamada import SpatialGraph

# np.random.seed(2)
np.random.seed(2)
# 1, 2 is broken, maybe edges with 3 crossings?


component_a = 'comp_a'
component_b = 'comp_b'
component_c = 'comp_c'
component_d = 'comp_d'
component_e = 'comp_e'
component_f = 'comp_f'
component_g = 'comp_g'
component_h = 'comp_h'
waypoint_ab = 'w_ab'
waypoint_ad = 'w_ad'
waypoint_ae = 'w_ae'
waypoint_bc = 'w_bc'
waypoint_bf = 'w_bf'
waypoint_cd = 'w_cd'
waypoint_cg = 'w_cg'
waypoint_dh = 'w_dh'
waypoint_ef = 'w_ef'
waypoint_eh = 'w_eh'
waypoint_fg = 'w_fg'
waypoint_gh = 'w_gh'

nodes = [component_a, component_b, component_c, component_d, component_e, component_f, component_g, component_h,
         waypoint_ab, waypoint_ad, waypoint_ae, waypoint_bc, waypoint_bf, waypoint_cd, waypoint_cg, waypoint_dh,
         waypoint_ef, waypoint_eh, waypoint_fg, waypoint_gh]

component_positions = np.array([[0, 0, 0],  # a
                                [1, 0, 0],  # b
                                [1, 1, 0],  # c
                                [0, 1, 0],  # d
                                [0, 0, 1],  # e
                                [1, 0, 1],  # f
                                [1, 1, 1],  # g
                                [0, 1, 1]])  # h

# waypoint_positions = np.random.rand(12, 3)
# waypoint_positions = np.array([[0.5, 0, 0],  # ab
#                                [0, 0.5, 0],  # ad
#                                [0, 0, 0.5],  # ae
#                                [1, 0.5, 0],  # bc
#                                [1, 0, 0.5],  # bf
#                                [0.5, 1, 0],  # cd
#                                [1, 1, 0.5],  # cg
#                                [0, 1, 0.5],  # dh
#                                [0.5, 0, 1],  # ef
#                                [0, 0.5, 1],  # eh
#                                [1, 0.5, 1],  # fg
#                                [0.5, 1, 1]])  # gh

waypoint_positions = np.array([[0.5, 0.1, 0],  # ab
                               [0.1, 0.7, 0.2],  # ad
                               [0.1, 0, 0.5],  # ae
                               [1, 0.5, 0],  # bc
                               [1, 0.1, 0.5],  # bf
                               [0.5, 1, 0],  # cd
                               [0.7, 0.6, 0.5],  # cg
                               [0.1, 1, 0.5],  # dh
                               [0.5, 0.1, 1],  # ef
                               [0.1, 0.6, 1],  # eh
                               [1, 0.5, 1],  # fg
                               [0.5, 0.95, 1]])  # gh

node_positions = np.concatenate((component_positions, waypoint_positions), axis=0)

edges = [(component_a, waypoint_ab), (waypoint_ab, component_b),
         (component_a, waypoint_ad), (waypoint_ad, component_d),
         (component_a, waypoint_ae), (waypoint_ae, component_e),
         (component_b, waypoint_bc), (waypoint_bc, component_c),
         (component_b, waypoint_bf), (waypoint_bf, component_f),
         (component_c, waypoint_cd), (waypoint_cd, component_d),
         (component_c, waypoint_cg), (waypoint_cg, component_g),
         (component_d, waypoint_dh), (waypoint_dh, component_h),
         (component_e, waypoint_ef), (waypoint_ef, component_f),
         (component_e, waypoint_eh), (waypoint_eh, component_h),
         (component_f, waypoint_fg), (waypoint_fg, component_g),
         (component_g, waypoint_gh), (waypoint_gh, component_h)]


# sg = SpatialGraph(nodes=nodes, node_positions=list(node_positions), edges=edges)
# sg.plot()
#
# # sgd = sg.create_spatial_graph_diagram()
# # yp = sgd.normalized_yamada_polynomial()
# #
# # print("Yamada Polynomial:", yp)
#
# # in front?
# a = np.array([-0.50385, -0.06584, -0.04247])
# b = np.array([0., 0., 0.])
#
# # behind?
# c = np.array([-0.42589332,  1.03516007, -0.0840149 ])
# d = np.array([-0.3429191,   0.85629405,  0.38622144])
#
# x_int = -0.41727468
# z_int = -0.03517084
#
# y_int_1 = sg.calculate_intermediate_y_position(a, b, x_int, z_int)
# y_int_2 = sg.calculate_intermediate_y_position(c, d, x_int, z_int)
#
# print("y_int_1:", y_int_1)
# print("y_int_2:", y_int_2)


sg = SpatialGraph(nodes=nodes, node_positions=list(node_positions), edges=edges)

sg.plot()

# sgd = sg.create_spatial_graph_diagram()
# yp = sgd.normalized_yamada_polynomial()
# print("Yamada Polynomial:", yp)

ordering_dict = sg.cyclic_node_ordering_crossings()


# expected_dict = {'crossing_0': {'comp_c': 0, 'w_ef': 1, 'w_bc': 2, 'comp_f': 3},
#                  'crossing_1': {'w_cd': 0, 'w_eh': 1, 'comp_d': 2, 'comp_e': 3}}


print("ordering_dict:", ordering_dict)
# print("expected_dict:", expected_dict)
#
# assert ordering_dict == expected_dict


# BF is the issue wrong order
# TOP LEFT NODE WRONG