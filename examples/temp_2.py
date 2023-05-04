import numpy as np
from yamada import SpatialGraph

# np.random.seed(2)
# np.random.seed(5)
# 1, is broken, maybe edges with 3 crossings?

# save seed 5. It was broken but then fixed


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

# nodes = [component_a, component_b, component_c, component_d, component_e, component_f, component_g, component_h,
#          waypoint_ab, waypoint_ad, waypoint_ae, waypoint_bc, waypoint_bf, waypoint_cd, waypoint_cg, waypoint_dh,
#          waypoint_ef, waypoint_eh, waypoint_fg, waypoint_gh]
#
# component_positions = np.array([[0, 0, 0],  # a
#                                 [1, 0, 0],  # b
#                                 [1, 1, 0],  # c
#                                 [0, 1, 0],  # d
#                                 [0, 0, 1],  # e
#                                 [1, 0, 1],  # f
#                                 [1, 1, 1],  # g
#                                 [0, 1, 1]])  # h
#
# waypoint_positions = np.array([[0.5, 0.1, 0],  # ab
#                                [0.1, 0.7, 0.2],  # ad
#                                [0.1, 0, 0.5],  # ae
#                                [1, 0.5, 0],  # bc
#                                [1, 0.1, 0.5],  # bf
#                                [0.5, 1, 0],  # cd
#                                [0.7, 0.6, 0.5],  # cg
#                                [0.1, 1, 0.5],  # dh
#                                [0.5, 0.1, 1],  # ef
#                                [0.1, 0.6, 1],  # eh
#                                [1, 0.5, 1],  # fg
#                                [0.5, 0.95, 1]])  # gh

# nodes = [component_a, component_b, component_c, component_d,
#          waypoint_ab, waypoint_ad, waypoint_ae, waypoint_bc, waypoint_bf, waypoint_cd, waypoint_cg, waypoint_dh]

nodes = [component_a, component_b, component_c, component_d]

component_positions = np.array([[0, 0, 0],  # a
                                [1, 0, 0],  # b
                                [1, 1, 0],  # c
                                [0, 1, 0]])  # d

# waypoint_positions = np.array([[0.5, 0.1, 0],  # ab
#                                [0.1, 0.7, 0.2],  # ad
#                                [0.1, 0, 0.5],  # ae
#                                [1, 0.5, 0],  # bc
#                                [1, 0.1, 0.5],  # bf
#                                [0.5, 1, 0],  # cd
#                                [0.7, 0.6, 0.5],  # cg
#                                [0.1, 1, 0.5]])  # dh

waypoint_positions = np.array([[0.5, 0.1, 0],  # ab
                               [0.1, 0.7, 0.2],  # ad
                               [1, 0.5, 0],  # bc
                               [0.5, 1, 0]])  # cd

node_positions = np.concatenate((component_positions, waypoint_positions), axis=0)


# edges = [(component_a, waypoint_ab), (waypoint_ab, component_b),
#          (component_a, waypoint_ad), (waypoint_ad, component_d),
#          (component_a, waypoint_ae), (waypoint_ae, component_e),
#          (component_b, waypoint_bc), (waypoint_bc, component_c),
#          (component_b, waypoint_bf), (waypoint_bf, component_f),
#          (component_c, waypoint_cd), ,
#          (component_c, waypoint_cg), (waypoint_cg, component_g),
#          (component_d, waypoint_dh), (waypoint_dh, component_h),
#          (component_e, waypoint_ef), (waypoint_ef, component_f),
#          (component_e, waypoint_eh), (waypoint_eh, component_h),
#          (component_f, waypoint_fg), (waypoint_fg, component_g),
#          (component_g, waypoint_gh), (waypoint_gh, component_h)]

# edges = [(component_a, waypoint_ab), (waypoint_ab, component_b),
#          (component_a, waypoint_ad), (waypoint_ad, component_d),
#          (component_a, waypoint_ae), (waypoint_ae, component_e),
#          (component_b, waypoint_bc), (waypoint_bc, component_c),
#          (component_b, waypoint_bf),
#          (component_c, waypoint_cd),
#          (component_c, waypoint_cg),
#          (component_d, waypoint_dh)]

# edges = [(component_a, waypoint_ab), (waypoint_ab, component_b),
#          (component_a, waypoint_ad), (waypoint_ad, component_d),
#          (component_a, waypoint_ae),
#          (component_b, waypoint_bc), (waypoint_bc, component_c),
#          (component_b, waypoint_bf),
#          (component_c, waypoint_cd), (waypoint_cd, component_d),
#          (component_c, waypoint_cg),
#          (component_d, waypoint_dh)]

edges = [(component_a, waypoint_ab), (waypoint_ab, component_b),
         (component_a, waypoint_ad), (waypoint_ad, component_d),
         (component_b, waypoint_bc), (waypoint_bc, component_c),
         (component_c, waypoint_cd), (waypoint_cd, component_d)]

sg = SpatialGraph(nodes=nodes, node_positions=node_positions, edges=edges)

sg.plot()

sgd = sg.create_spatial_graph_diagram()
yp = sgd.normalized_yamada_polynomial()
print("Yamada Polynomial:", yp)

