import numpy as np
from yamada import SpatialGraph

from time import time_ns

np.random.seed(2)


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

# waypoint_positions = np.random.rand(12, 3)
waypoint_positions = np.array([[0.5, 0, 0],  # ab
                               [0, 0.5, 0],  # ad
                               np.random.rand(3),  # [0, 0, 0.5],  # ae
                               [1, 0.5, 0],  # bc
                               [1, 0, 0.5],  # bf
                               [0.5, 1, 0],  # cd
                               np.random.rand(3),  # [1, 1, 0.5],  # cg
                               [0, 1, 0.5],  # dh
                               [0.5, 0, 1],  # ef
                               [0, 0.5, 1],  # eh
                               np.random.rand(3),  # [1, 0.5, 1],  # fg
                               [0.5, 1, 1]])  # gh

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





positions = []
num_crossings = []
yps = []
runtime = []



for i in range(5):

    np.random.seed(i+70)

    sg = SpatialGraph(nodes=nodes, node_positions=list(node_positions), edges=edges)

    sg.plot()

    t1 = time_ns()

    sgd = sg.create_spatial_graph_diagram()

    t2 = time_ns()

    yp = sgd.normalized_yamada_polynomial()

    t3 = time_ns()

    print("Yamada Polynomial:", yp)


    print("Time to create spatial graph diagram:", (t2 - t1)/1e9/60, "minutes")
    print("Time to compute yamada polynomial:",    (t3 - t2)/1e9/60, "minutes")

    positions.append(sg.rotated_node_positions)
    num_crossings.append(len(sgd.crossings))
    yps.append(yp)
    runtime.append((t3 - t1)/1e9/60)


