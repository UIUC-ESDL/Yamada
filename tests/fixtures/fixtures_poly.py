import pytest
from cypari import pari


@pytest.fixture
def poly_empty():
    return 1


@pytest.fixture
def poly_unknot():
    # Peddada et al. 2021, Proof Y1: A + 1 + A^(-1)
    # This can be normalized to -A^2 - A - 1 (explain normalization)
    a = pari('A')
    return -a ** 2 - a - 1


@pytest.fixture
def poly_two_unknots():
    a = pari('A')
    # Peddada et al. 2021, Property P2. H(G1 disjoint union G2) = H(G1)H(G2)
    # Normalized, (-A^2 - A - 1)^2 = A^4 + 2A^3 + 3A^2 + 2A + 1
    return a**4 + 2*a**3 + 3*a**2 + 2*a + 1


@pytest.fixture
def poly_fig_8():
    pass



