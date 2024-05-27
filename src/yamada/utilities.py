import glob
import json
import pickle


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


def split_edge(edge):
    """
    Splits an edge with more than two nodes into a series of edges which each have two nodes.
    """

    edges = []
    for i in range(len(edge)-1):
        edges.append((edge[i], edge[i+1]))
    return edges


def split_edges(edges):
    """
    Splits a list of edges with more than two nodes into a series of edges which each have two nodes.
    """

    # Strip crossings from edges
    edges_without_crossings = []
    for edge in edges:
        edge_without_crossings = [node for node in edge if "C" not in node]
        edges_without_crossings.append(edge_without_crossings)

    new_edges = []
    for edge in edges_without_crossings:
        new_edges.extend(split_edge(edge))
    return new_edges


def extract_graph_from_json_file(filename):
    """
    Reads a json file and returns a networkx graph
    """

    data = read_json_file(filename)

    # Extract the dictionary inputs
    nodes              = list(data['3D_positions'][0].keys())
    node_positions     = list(data['3D_positions'][0].values())
    crossings          = list(data['3D_positions'][1].keys())
    crossing_positions = list(data['3D_positions'][1].values())
    edges              = list(data['3D_positions'][2])

    # Extract non crossings from crossings
    noncrossings, noncrossing_positions = zip(*[(crossing, crossing_position) for crossing, crossing_position in zip(crossings, crossing_positions) if "C" not in crossing])

    # Only extract non crossings
    # Merge nodes and crossings
    nodes.extend(noncrossings)
    node_positions.extend(noncrossing_positions)

    # Remove crossings from edges

    # Format edges so that each edge has two nodes
    edges = split_edges(edges)

    return nodes, node_positions, edges


def pickle_yamada(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)


def load_yamada(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)


def read_pickle(nodes):
    file = open(max(glob.glob(f'pickles/G{nodes}_C*.pickle')), 'rb')
    return pickle.load(file)
