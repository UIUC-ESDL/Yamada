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


def edges_form_a_strand(edge_1, edge_2):
    """
    Check whether two edges are form part, or a whole, of a strand.
    A strand is a series of edges and 2-valent vertices that are connected in a line.
    """

    def edges_form_a_strand_along_a_direction(e1, e2, direction_index):

        # Initialize the current object and the index of the next object
        current_object = e1
        index_of_next_object = direction_index

        # Loop through the strand until the second edge is reached or the strand ends
        strand = [current_object.label]
        max_iter = 1000
        for i in range(max_iter):

            # Identify the next object and the index it assigns to the current object
            next_object, next_object_index = current_object.adjacent[index_of_next_object]
            strand + [next_object.label]

            # If the next object is the second edge, then the edges form a strand
            if next_object == e2:
                return True, strand

            # If the next object is not the second edge and is also not 2-valent,
            # then the strand ends and the edges do not form a strand.
            elif next_object.degree != 2:
                return False, strand

            # If not the next object is admissible, then continue moving along the strand
            else:
                # Set the next object as the current object
                current_object = next_object

                # Set the index of the next object
                # Since this is a 2-valent vertex, the index of the next object is the opposite of the current index
                index_of_next_object = (next_object_index + 1) % 2

        return False, strand

    # Check if the edges form a strand in either direction
    cond_1, strand_dir1 = edges_form_a_strand_along_a_direction(edge_1, edge_2, 0)
    cond_2, strand_dir2 = edges_form_a_strand_along_a_direction(edge_1, edge_2, 1)
    does_form_strand = cond_1 or cond_2
    strands_checked = [strand_dir1, strand_dir2]
    return does_form_strand, strands_checked


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
