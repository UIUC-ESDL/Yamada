import numpy as np
from yamada.projection import SpatialGraph


def test_unknot():
    for i in range(6):
        np.random.seed(i)

        sg1 = SpatialGraph(nodes=['a', 'b', 'c'],
                           node_positions=np.array([[0, 0.5, 0], [-1, 0.5, 1], [1, 0, 0]]),
                           edges=[('a', 'b'), ('b', 'c'), ('c', 'a')])
        sg1.project()
        sgd1 = sg1.create_spatial_graph_diagram()
        sgd1.normalized_yamada_polynomial()


def test_infinity_symbol_single_twist():
    np.random.seed(0)

    sg1 = SpatialGraph(nodes=['a', 'b', 'c', 'd'],
                       node_positions=np.array([[0, 0.5, 0], [1, 0.5, 1], [1, 0, 0], [0, 0, 1]]),
                       edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a')])
    sg1.project()
    sgd1 = sg1.create_spatial_graph_diagram()
    sgd1.normalized_yamada_polynomial()


def test_infinity_symbol_double_twist():
    for i in range(6):
        np.random.seed(i)
        sg1 = SpatialGraph(nodes=['a', 'b', 'c', 'd', 'e', 'f'],
                           node_positions=np.array([[0, 0.5, 0], [1, 0, 1], [2, 0.5, 0], [3, 0, 1], [1, 1, 0], [-1, 0, 1]]),
                           edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'f'), ('f', 'a')])
        sg1.project()
        sgd1 = sg1.create_spatial_graph_diagram()
        sgd1.normalized_yamada_polynomial()


def test_double_crossing_single_edge():
    # TODO Implement this test.
    pass


def test_triple_crossing_single_edge():
    # TODO Implement this test.
    pass


def test_quadrivalent_node():
    pass


def test_complicated_topology_1():

    for i in range(6):
        np.random.seed(i)
        sg1 = SpatialGraph(nodes=['a', 'b', 'c', 'd', 'e', 'f'],
                           node_positions=np.array([[0, 0.5, 0], [1, 0, 1], [2, 0.5, 0], [3, 0, 1], [1, 1, 0], [-1, 0, 1]]),
                           edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'f'), ('f', 'a'), ('b', 'f')])

        sg1.project()
        sgd1 = sg1.create_spatial_graph_diagram()
        sgd1.normalized_yamada_polynomial()
