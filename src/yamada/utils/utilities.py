import glob
import json
import pickle

# from yamada.sgd.sgd_operations import split_edges


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


def create_sgd_from_json(filename):
    """
    Reads a json file and returns a networkx-based Spatial Graph Diagram.

    FIXME: Some 2D projections of 3D coordinates may be invalid. Rather than indexing
    FIXME: and y coordinates, the JSON should deliberately provide valid 2D coordinates.
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


def save_pickle(graph):
    pass


def read_pickle(nodes):
    file = open(max(glob.glob(f'pickles/G{nodes}_C*.pickle')), 'rb')
    return pickle.load(file)
