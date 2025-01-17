from cypari import pari
from yamada import SpatialGraphDiagram, Crossing, Edge, available_r2_moves, apply_r2_move


def test_r2_unknot_over_loop(unknot_over_loop, poly_unknot):

    sgd = unknot_over_loop()

    assert sgd.yamada_polynomial() == poly_unknot

    r2_crossing_labels = available_r2_moves(sgd)

    assert len(r2_crossing_labels) == 1
    assert ('c1', 'c2') in r2_crossing_labels or ('c2', 'c1') in r2_crossing_labels

    sgd = apply_r2_move(sgd, ('c1', 'c2'))

    assert sgd.yamada_polynomial() == poly_unknot


def test_r2_unknot_two_over_loops(unknot_two_over_loops, poly_unknot):

    # Initialize the spatial graph diagram
    sgd = unknot_two_over_loops()

    # Sanity check the initial state
    assert len(sgd.edges) == 8
    assert len(sgd.vertices) == 0
    assert len(sgd.crossings) == 4
    assert sgd.yamada_polynomial() == poly_unknot

    # Remove the first loop
    r2_moves = available_r2_moves(sgd)

    # The two over-loops form third over loop in the middle. Each loop has an R2 move.
    assert len(r2_moves) == 3

    # Faces are not ordered, so we need to check both directions
    assert ('c1', 'c2') in r2_moves or ('c2', 'c1') in r2_moves
    assert ('c3', 'c4') in r2_moves or ('c4', 'c3') in r2_moves
    assert ('c2', 'c3') in r2_moves or ('c3', 'c2') in r2_moves

    sgd = apply_r2_move(sgd, ('c1', 'c2'), simplify=False)

    # Disable "simplify" to ensure that "apply_r2_move" removes the crossings in a diagrammatically correct way.
    # It should delete two crossings and connect the opposite edges with 2-valent vertices.
    assert len(sgd.edges) == 8
    assert len(sgd.vertices) == 4
    assert len(sgd.crossings) == 2
    assert sgd.yamada_polynomial() == poly_unknot

    # Now simplify the diagram
    sgd.simplify_diagram()
    assert len(sgd.edges) == 4
    assert len(sgd.vertices) == 0
    assert len(sgd.crossings) == 2
    assert sgd.yamada_polynomial() == poly_unknot

    # Remove the second loop
    r2_moves = available_r2_moves(sgd)

    assert len(r2_moves) == 1
    assert ('c3', 'c4') in r2_moves or ('c4', 'c3') in r2_moves

    sgd = apply_r2_move(sgd, ('c3', 'c4'), simplify=False)
    assert len(sgd.edges) == 4
    assert len(sgd.vertices) == 4
    assert len(sgd.crossings) == 0
    assert sgd.yamada_polynomial() == poly_unknot

    sgd.simplify_diagram()
    assert len(sgd.edges) == 1
    assert len(sgd.vertices) == 1
    assert len(sgd.crossings) == 0
    assert sgd.yamada_polynomial() == poly_unknot

    # Verify that there are no more R2 moves
    r2_moves = available_r2_moves(sgd)
    assert len(r2_moves) == 0


def test_r2_unknot_one_over_one_under_loop(unknot_one_over_one_under_loop, poly_unknot):

    sgd = unknot_one_over_one_under_loop()

    # Remove the first loop

    r2_crossing_labels = available_r2_moves(sgd)

    assert len(r2_crossing_labels) == 2
    assert ('c1', 'c2') in r2_crossing_labels or ('c2', 'c1') in r2_crossing_labels

    sgd = apply_r2_move(sgd, ('c1', 'c2'))

    yp_after_first_r2 = sgd.yamada_polynomial()

    assert yp_after_first_r2 == poly_unknot

    # Remove the second loop

    r2_crossing_labels = available_r2_moves(sgd)

    assert len(r2_crossing_labels) == 1
    assert ('c3', 'c4') in r2_crossing_labels or ('c4', 'c3') in r2_crossing_labels

    sgd = apply_r2_move(sgd, ('c3', 'c4'))

    yp_after_second_r2 = sgd.yamada_polynomial()

    assert yp_after_second_r2 == poly_unknot

    r2_crossing_labels = available_r2_moves(sgd)

    assert len(r2_crossing_labels) == 0
