import json


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


def read_json_file(filename):
    """
    Reads a json file and returns a dictionary
    """

    with open(filename) as f:
        data = json.load(f)
    return data


def read_json_files(filenames):
    """
    Reads a list of json files and returns a dictionary
    """

    data = {}
    for filename in filenames:
        data.update(read_json_file(filename))
    return data
