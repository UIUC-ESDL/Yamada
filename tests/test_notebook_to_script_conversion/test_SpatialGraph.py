#!/usr/bin/env python
# coding: utf-8

# 

# In[6]:


import numpy as np
from yamada import SpatialGraph
from yamada import Vertex, Edge, Crossing, SpatialGraphDiagram, h_poly, reverse_poly, normalize_yamada_polynomial


# ## Verifying the cyclic ordering of nodes for a vertex
# 
# ![Abstract Graph G5](./images/abstract_graph_G5.png)

# In[7]:


def test_cyclic_node_ordering_vertex():

    nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    node_positions = np.array([[0, 0, 0], [1, 0, 0], [0.5, 1, 0], [0.5, 0.5, 0], [0.25,0.75, 0], [0.75, 0.75, 0], [0, 1, 0], [1, 1, 0]])

    edges = [('a', 'b'), ('a', 'g'), ('a', 'd'), ('b', 'd'), ('b', 'h'), ('d', 'e'), ('d', 'f'), ('e', 'c'), ('f', 'c'), ('g', 'c'), ('h', 'c')]

    sg = SpatialGraph(nodes=nodes,
                      node_positions=node_positions,
                      edges=edges)

    # Use a predefined rotation (from a random seed) that previously produced an error
    rotation = np.array([3.44829694, 4.49366732, 3.78727399])
    sg.rotation = rotation
    sg.rotated_node_positions = sg.rotate(sg.node_positions, sg.rotation)
    sg.project()

    order = sg.cyclic_order_vertex('c')
    expected_order = {'c': {'e': 3, 'f': 0, 'g': 2, 'h': 1}}

    assert order == expected_order


# ## Verify the cyclic ordering of nodes for a crossing
# 
# Note: I've gotten tripped up with the optical illusion of which faces are in front and which are in back. The annotations show the correct orientation.
# 
# Note: The
# 
# ![Crossing Ordering](./images/crossing_ordering.png)

# In[8]:


def test_cyclic_ordering_crossing():

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

    component_positions = np.array([[0, 0, 0],  # a
                                [1, 0, 0],  # b
                                [1, 1, 0],  # c
                                [0, 1, 0],  # d
                                [0, 0, 1],  # e
                                [1, 0, 1],  # f
                                [1, 1, 1],  # g
                                [0, 1, 1]])  # h

    waypoint_positions = np.array([[0.5, 0, 0],  # ab
                               [0, 0.5, 0],  # ad
                               [0, 0, 0.5],  # ae
                               [1, 0.5, 0],  # bc
                               [1, 0, 0.5],  # bf
                               [0.5, 1, 0],  # cd
                               [1, 1, 0.5],  # cg
                               [0, 1, 0.5],  # dh
                               [0.5, 0, 1],  # ef
                               [0, 0.5, 1],  # eh
                               [1, 0.5, 1],  # fg
                               [0.5, 1, 1]])  # gh

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


    sg = SpatialGraph(nodes=nodes, node_positions=list(node_positions), edges=edges)

    # Define the random rotation that previously caused issues
    rotation = np.array([3.44829694, 4.49366732, 3.78727399])
    sg.rotation = rotation
    sg.rotated_node_positions = sg.rotate(sg.node_positions, sg.rotation)
    sg.project()


    ordering_dict = sg.cyclic_order_crossings()

    expected_dict = {'crossing_0': {'comp_c': 2, 'w_ef': 3, 'w_bc': 0, 'comp_f': 1},
                     'crossing_1': {'w_cd': 0, 'w_eh': 1, 'comp_d': 2, 'comp_e': 3}}

    assert ordering_dict == expected_dict


# ## Example 2
# 
# ![Crossing Ordering](./images/crossing_ordering_2.png)

# In[9]:


def test_cyclic_ordering_crossing_2():

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

    component_positions = np.array([[0, 0, 0],  # a
                                [1, 0, 0],  # b
                                [1, 1, 0],  # c
                                [0, 1, 0],  # d
                                [0, 0, 1],  # e
                                [1, 0, 1],  # f
                                [1, 1, 1],  # g
                                [0, 1, 1]])  # h

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


    sg = SpatialGraph(nodes=nodes, node_positions=node_positions, edges=edges)

    # Set rotation
    rotation = np.array([2.73943676, 0.16289932, 3.4536312])
    sg.rotation = rotation
    sg.rotated_node_positions = sg.rotate(sg.node_positions, sg.rotation)
    sg.project()


    ordering_dict = sg.cyclic_order_crossings()

    expected_dict = {'crossing_0': {'comp_a': 1, 'comp_d': 2, 'w_ab': 3,   'w_dh': 0},
                     'crossing_1': {'comp_b': 1, 'comp_c': 2, 'crossing_2': 3,   'w_cg': 0},
                     'crossing_2': {'w_cg': 0,   'crossing_1': 1, 'comp_g': 2, 'w_bf': 3},
                     'crossing_3': {'w_gh': 0,   'w_bf': 1,   'comp_g': 2, 'comp_f': 3}}

    assert ordering_dict == expected_dict


# ## Example 3

# ![Crossing Ordering](./images/crossing_ordering_3.png)

# ## Divide edges into sub-edges
# 
# ![Infinity Symbol](./images/infinity_symbol.png)
# 
# 

# In[11]:


def test_get_sub_edges():

    sg = SpatialGraph(nodes=['a', 'b', 'c', 'd'],
                      node_positions=np.array([[0, 0.5, 0], [1, 0.5, 1], [1, 0, 0], [0, 0, 1]]),
                      edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a')])

    # Set rotation

    rotation = np.array([3.44829694, 4.49366732, 3.78727399])
    sg.rotation = rotation
    sg.rotated_node_positions = sg.rotate(sg.node_positions, sg.rotation)
    sg.project()

    sep = sg.get_sub_edges()

    expected_sub_edges = [('b', 'crossing_0'), ('crossing_0', 'a'), ('b', 'c'), ('d', 'crossing_0'), ('crossing_0', 'c'), ('d', 'a')]

    assert sep == expected_sub_edges


# In[11]:


# def test_edge_order():
#
        # TODO Implement this

#         np.random.seed(0)
#
#         sg = SpatialGraph(nodes=['a', 'b', 'c', 'd'],
#                         node_positions=np.array([[0, 0.5, 0], [1, 0.5, 1], [1, 0, 0], [0, 0, 1]]),
#                         edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a')])
#
#         edge_0 = sg.edges[0]
#
#         vertices_and_crossings = sg.get_vertices_and_crossings_of_edge(edge_0)
#
#         edge_order = [vertices_and_crossings[i][0] < vertices_and_crossings[i+1][0] for i in range(len(vertices_and_crossings)-1)]
#
#         assert all(edge_order)

