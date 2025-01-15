import pytest
# TODO Implement

def test_empty_0e_0v_0c(empty_0e_0v_0c, poly_empty):

    sgd = empty_0e_0v_0c

    with pytest.warns(UserWarning, match="Empty diagram."):
        sgd._correct_diagram()

    assert sgd
    assert sgd.yamada_polynomial() == poly_empty

    # Simplify the graph
    sgd.simplify_diagram()
    assert len(sgd.edges) == 0
    assert len(sgd.vertices) == 0
    assert len(sgd.crossings) == 0
    assert sgd.yamada_polynomial() == poly_empty
