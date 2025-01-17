from cypari import pari
from yamada import SpatialGraphDiagram, Edge, Crossing, available_r3_moves, apply_r3_move


def test_does_not_have_r3():
    # TODO: Implement
    pass


def test_has_r3(two_unknots_1):
    # Conventions _1, _2 follow clockwise ordering.

    r3_moves = available_r3_moves(two_unknots_1)
    assert len(r3_moves) == 8

    # Face c1, c2, c3 has 2 possible R3 moves
    r3_1 = {'stationary_crossing': 'c1',
            'stationary_edge_1': 'e1',
            'stationary_edge_2': 'e2',
            'moving_crossing_1': 'c2',
            'moving_crossing_2': 'c3',
            'moving_edge': 'e6'}

    r3_2 = {'stationary_crossing': 'c2',
            'stationary_edge_1': 'e6',
            'stationary_edge_2': 'e1',
            'moving_crossing_1': 'c3',
            'moving_crossing_2': 'c1',
            'moving_edge': 'e2'}

    assert r3_1 in r3_moves
    assert r3_2 in r3_moves

    # Face c1, c3, c4 has 2 possible R3 moves
    r3_3 = {'stationary_crossing': 'c1',
            'stationary_edge_1': 'e2',
            'stationary_edge_2': 'e3',
            'moving_crossing_1': 'c3',
            'moving_crossing_2': 'c4',
            'moving_edge': 'e7'}

    r3_4 = {'stationary_crossing': 'c4',
            'stationary_edge_1': 'e3',
            'stationary_edge_2': 'e7',
            'moving_crossing_1': 'c1',
            'moving_crossing_2': 'c3',
            'moving_edge': 'e2'}

    assert r3_3 in r3_moves
    assert r3_4 in r3_moves

    # Face c1, c4, c5 has 2 possible R3 moves
    r3_5 = {'stationary_crossing': 'c1',
            'stationary_edge_1': 'e3',
            'stationary_edge_2': 'e4',
            'moving_crossing_1': 'c4',
            'moving_crossing_2': 'c5',
            'moving_edge': 'e8'}

    r3_6 = {'stationary_crossing': 'c4',
            'stationary_edge_1': 'e8',
            'stationary_edge_2': 'e3',
            'moving_crossing_1': 'c5',
            'moving_crossing_2': 'c1',
            'moving_edge': 'e4'}

    assert r3_5 in r3_moves
    assert r3_6 in r3_moves

    # Face c1, c5, c2 has 2 possible R3 moves
    r3_7 = {'stationary_crossing': 'c1',
            'stationary_edge_1': 'e4',
            'stationary_edge_2': 'e1',
            'moving_crossing_1': 'c5',
            'moving_crossing_2': 'c2',
            'moving_edge': 'e5'}

    r3_3 = {'stationary_crossing': 'c2',
            'stationary_edge_1': 'e1',
            'stationary_edge_2': 'e5',
            'moving_crossing_1': 'c1',
            'moving_crossing_2': 'c5',
            'moving_edge': 'e4'}

    assert r3_7 in r3_moves
    assert r3_3 in r3_moves

def test_r3(two_unknots_1, poly_two_unknots):

    sgd = two_unknots_1

    assert sgd.yamada_polynomial() == poly_two_unknots

    r3_moves = available_r3_moves(sgd)
    assert len(r3_moves) > 0

    # Hard-coded demo
    stationary_crossing = 'c1'
    moving_crossing_1 = 'c4'
    moving_crossing_2 = 'c3'
    crossing_edge = 'e7'
    stationary_edge_1 = 'e3'
    stationary_edge_2 = 'e2'
    r3_input = {
        'stationary_crossing': stationary_crossing,
        'moving_crossing_1': moving_crossing_1,
        'moving_crossing_2': moving_crossing_2,
        'crossing_edge': crossing_edge,
        'stationary_edge_1': stationary_edge_1,
        'stationary_edge_2': stationary_edge_2
    }

    # TODO Asser r3 move in r3 moves...

    sgd_r3 = apply_r3_move(sgd, r3_input)

    assert sgd_r3.yamada_polynomial() == poly_two_unknots

    r3_moves = available_r3_moves(sgd_r3)
    assert len(r3_moves) > 0


def test_r3_try_different(two_unknots_1, poly_two_unknots):
    """With one diagram, try each available R3 move in parallel."""

    sgd = two_unknots_1
    assert sgd.yamada_polynomial() == poly_two_unknots
    r3_moves = available_r3_moves(sgd)
    sgd_copies = [sgd.copy() for _ in range(len(r3_moves))]

    for sgd_copy, r3_move in zip(sgd_copies, r3_moves):
        sgd_copy = apply_r3_move(sgd_copy, r3_move)
        assert sgd_copy.yamada_polynomial() == poly_two_unknots



def test_r3_repeat(two_unknots_1, poly_two_unknots):
    """With one diagram, try applying R3 moves in succession."""
    # TODO Fix Error
    sgd = two_unknots_1

    assert sgd.yamada_polynomial() == poly_two_unknots

    n_tries = 2
    for i in range(n_tries):
        r3_moves = available_r3_moves(sgd)
        assert len(r3_moves) > 0
        sgd = apply_r3_move(sgd, r3_moves[0])
        assert sgd.yamada_polynomial() == poly_two_unknots

    # n_tries = 5
    # for i in range(n_tries):
    #     r3_moves = available_r3_moves(sgd)
    #     assert len(r3_moves) > 0
    #     sgd = apply_r3_move(sgd, r3_moves[i])
    #     assert sgd.yamada_polynomial() == poly_two_unknots


