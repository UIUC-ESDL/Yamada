import pickle

from cypari import pari


def get_coefficients_and_exponents(poly):

    """
    A helper function to extract the coefficients and exponents from a Yamada polynomial.

    The Yamada polynomial calculator was originally written with SageMath and the Laurent polynomial objects
    had explicit attributes for coefficients and exponents that you could directly query. However, switching
    to the cypari library to improve OS compatibility added a few complications, including that there is no native
    method to access the coefficients and exponents of Yamada polynomials. This function obtains them.
    """

    # Assumes all denominators are only A**n with no coefficient
    coefficients = poly.numerator().Vec()
    coeff_len = len(coefficients)

    exponents = []
    degree = poly.poldegree()

    for _ in range(coeff_len):
        exponents.append(degree)
        degree -= 1

    return coefficients, exponents


def pickle_yamada(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)


def load_yamada(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)


def reverse_poly(poly):
    """
    """

    A = pari('A')

    coeffs, exps = get_coefficients_and_exponents(poly)

    ans = pari(0)

    for c, e in zip(coeffs, exps):
        ans += c * A ** (-e)

    return ans


def normalize_poly(yamada_polynomial):
    """normalized_yamada_polynomial
    """

    A = pari('A')

    _, exps = get_coefficients_and_exponents(yamada_polynomial)
    a, b = min(exps), max(exps)
    ans1 = (-A) ** (-a) * yamada_polynomial
    ans2 = (-A) ** b * reverse_poly(yamada_polynomial)

    normalized_yamada_polynomial = min([ans1, ans2], key=list)

    return normalized_yamada_polynomial
