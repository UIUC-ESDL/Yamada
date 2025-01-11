import pytest
from cypari import pari


@pytest.fixture
def poly_empty():
    return 1


@pytest.fixture
def poly_unknot():
    a = pari('A')
    return -a ** 2 - a - 1


@pytest.fixture
def poly_double_unknot():
    pass


@pytest.fixture
def poly_fig_8():
    pass



