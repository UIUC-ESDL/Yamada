import numpy as np
from yamada import SpatialGraph

# TODO I think the labels are out of date of cyclic ordering at crossings. REDO. Make visualization easier in 2D. Include in pub.

# nodes = ["0", "1", "2", "3", "4", "5", "6", "7"]
#
# pos= {
#     "0": (0, 0, 0),
#     "1": (1, 0, 0),
#     "2": (0, 1, 0),
#     "3": (1, 1, 0),
#     "4": (0, 0, 1),
#     "5": (1, 0, 1),
#     "6": (0, 1, 1),
#     "7": (1, 1, 1),
# }
#
# edges = [
#     ("0", "1"), ("0", "2"), ("0", "4"),
#     ("1", "3"), ("1", "5"),
#     ("2", "3"), ("2", "6"),
#     ("3", "7"),
#     ("4", "5"), ("4", "6"),
#     ("5", "7"),
#     ("6", "7")
# ]
#
# # Instantiate the SpatialGraph object
# sg = SpatialGraph(nodes=nodes,
#                   edges=edges,
#                   pos=pos)
#
# # sg.subdivide_edges()
#
# sg.to_spatial_graph_diagram()
#
# # sg.plot()

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

nodes = [component_a, component_b, component_c, component_d, component_e, component_f,
         component_g, component_h, waypoint_ab, waypoint_ad, waypoint_ae, waypoint_bc,
         waypoint_bf, waypoint_cd, waypoint_cg, waypoint_dh, waypoint_ef, waypoint_eh,
         waypoint_fg, waypoint_gh]

component_positions = [(0, 0, 0),  # a
                       (1, 0, 0),  # b
                       (1, 1, 0),  # c
                       (0, 1, 0),  # d
                       (0, 0, 1),  # e
                       (1, 0, 1),  # f
                       (1, 1, 1),  # g
                       (0, 1, 1)]  # h

waypoint_positions = [(0.5, 0, 0),  # ab
                      (0, 0.5, 0),  # ad
                      (0, 0, 0.5),  # ae
                      (1, 0.5, 0),  # bc
                      (1, 0, 0.5),  # bf
                      (0.5, 1, 0),  # cd
                      (1, 1, 0.5),  # cg
                      (0, 1, 0.5),  # dh
                      (0.5, 0, 1),  # ef
                      (0, 0.5, 1),  # eh
                      (1, 0.5, 1),  # fg
                      (0.5, 1, 1)]  # gh

pos = (component_positions + waypoint_positions)

pos = {node: pos for node, pos in zip(nodes, pos)}

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

# Define the random rotation that previously caused issues
rotation = np.array([3.44829694, 4.49366732, 3.78727399])

sg = SpatialGraph(nodes=nodes,
                  pos=pos,
                  edges=edges,
                  rotation=rotation)

ordering_dict = sg.cyclic_orderings()

expected_dict = {'crossing_0': {'comp_c': 2, 'w_ef': 3, 'w_bc': 0, 'comp_f': 1},
                 'crossing_1': {'w_cd': 0, 'w_eh': 1, 'comp_d': 2, 'comp_e': 3}}



# assert ordering_dict == expected_dict


sg.plot()