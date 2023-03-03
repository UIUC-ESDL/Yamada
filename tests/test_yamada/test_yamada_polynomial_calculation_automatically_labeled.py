import numpy as np
from yamada.projection import SpatialGraph


def test_unknot():

    np.random.seed(0)

    # sg1 = SpatialGraph(nodes=['a', 'b', 'c', 'd'],
    #                    node_positions=np.array([[0, 0.5, 0], [1, 0.5, 1], [1, 0, 0], [0, 0, 1]]),
    #                    edges=[('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a')])
    # sg1.project()
    # sg1.plot()
    # sgd1 = sg1.create_spatial_graph_diagram()
    # yamada_polynomial_infinity_symbol = sgd1.yamada_polynomial()
    # print("Infinity Symbol Yamada Polynomial:", yamada_polynomial_infinity_symbol)

def test_infinity_symbol_single_twist():
    # TODO Implement this test.
    pass

def test_double_crossing_single_edge():
    # TODO Implement this test.
    pass

def test_triple_crossing_single_edge():
    # TODO Implement this test.
    pass

def test_quadrivalent_node():
    pass