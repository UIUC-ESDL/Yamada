import numpy as np
from yamada import SpatialGraph
from yamada.sgd.utilities import edges_form_a_strand

# %% Strands

def test_forms_a_strand_unknot_1e_1v(unknot_1e_1v):

    e1 = unknot_1e_1v.edges[0]
    v1 = unknot_1e_1v.vertices[0]

    forms_a_strand = edges_form_a_strand(e1, v1)

    assert forms_a_strand == True







def test_get_sub_edges():

    # Set rotation
    rotation = np.array([3.44829694, 4.49366732, 3.78727399])

    sg = SpatialGraph(nodes=['a', 'b', 'c', 'd'],
                      node_positions={'a':[0, 0.5, 0],
                                      'b': [1, 0.5, 1],
                                      'c': [1, 0, 0],
                                      'd': [0, 0, 1]},
                      edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a')],
                      rotation=rotation)

    sep = sg.get_sub_edges()

    expected_sub_edges = [('b', 'crossing_0'), ('crossing_0', 'a'), ('b', 'c'), ('d', 'crossing_0'), ('crossing_0', 'c'), ('d', 'a')]

    assert sep == expected_sub_edges

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