import json
import networkx as nx
import numpy as np
from numpy import sin, cos


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

def generate_isomorphism(g, pos, n=3, rotate=False):
    """
    Generates an isomorphism of a graph with subdivided edges.
    """

    def subdivide_edge(g, edge, pos, n=3):
        u, v = edge
        g.remove_edge(u, v)

        nodes = [f"{u}{v}{i}" for i in range(1, n)]

        # Add the initial and final nodes
        nodes.insert(0, u)
        nodes.append(v)

        nx.add_path(g, nodes)

        for i in range(1, n):
            g.add_node(f"{u}{v}{i}")
            pos[f"{u}{v}{i}"] = pos[u] + (pos[v] - pos[u]) * i / n

        return g, pos


    for edge in list(g.edges()):
        g, pos = subdivide_edge(g, edge, pos, n=n)

    def rotate_points(positions: np.ndarray,
               rotation:  np.ndarray = 2*np.random.rand(3)) -> np.ndarray:
        """
        Rotates a set of points about the first 3D point in the array.

        :param positions: A numpy array of 3D points.
        :param rotation: A numpy array of 3 Euler angles in radians.

        :return: new_positions:
        """

        # Shift the object to origin
        reference_position = positions[0]
        origin_positions = positions - reference_position

        alpha, beta, gamma = rotation

        # Rotation matrix Euler angle convention r = r_z(gamma) @ r_y(beta) @ r_x(alpha)

        r_x = np.array([[1., 0., 0.],
                        [0., cos(alpha), -sin(alpha)],
                        [0., sin(alpha), cos(alpha)]])

        r_y = np.array([[cos(beta), 0., sin(beta)],
                        [0., 1., 0.],
                        [-sin(beta), 0., cos(beta)]])

        r_z = np.array([[cos(gamma), -sin(gamma), 0.],
                        [sin(gamma), cos(gamma), 0.],
                        [0., 0., 1.]])

        # TODO Replace with explicitly formulated matrix
        r = r_z @ r_y @ r_x

        # Transpose positions from [[x1,y1,z1],[x2... ] to [[x1,x2,x3],[y1,... ]
        rotated_origin_positions = (r @ origin_positions.T).T

        # Shift back from origin
        new_positions = rotated_origin_positions + reference_position

        rotated_node_positions = new_positions

        return rotated_node_positions

    if rotate:
        pos = rotate_points(np.array(list(pos.values())))
        pos = {k: v for k, v in zip(list(g.nodes), pos)}

    # k = 1000 * 1/len(g.nodes)
    # nx.set_edge_attributes(g, 5, "weight")
    pos = nx.spring_layout(g, iterations=50, dim=3, pos=pos)



    return g, pos




