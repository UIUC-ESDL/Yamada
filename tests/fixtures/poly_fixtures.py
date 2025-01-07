import pytest
from cypari import pari


@pytest.fixture
def unknot_yamada_poly():
    a = pari('A')
    return -a ** 2 - a - 1

