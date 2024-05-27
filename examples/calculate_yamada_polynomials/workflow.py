"""EXAMPLE

Extract spatial graphs from jsons and calculate their Yamada polynomials.

"""
# %% Import Statements

import os
from yamada import extract_graph_from_json_file, SpatialGraph

# Set the random seed for reproducibility
import numpy as np
np.random.seed(0)

# %% Define the JSON file location

# Obtain the local path of this example's directory
directory = os.path.dirname(__file__) + '/'

# User Input: Set the path to the json file you want to evaluate

# Example 1
filepath = directory + "enumerated_spatial_topologies/G6/C1/G6C1I0.json"

# Example 2
# filepath = directory + "enumerated_spatial_topologies/G10/C4/G10C4I7.json"

# # Example 3
# filepath = directory + "enumerated_spatial_topologies/G14/C3/G14C3I11.json"

# %% Extract the spatial graph from the json file

nodes, node_positions, edges = extract_graph_from_json_file(filepath)

# Convert the node_positions to a dictionary
# TODO Change input formatter
node_positions = {node: position for node, position in zip(nodes, node_positions)}

# %% Create a SpatialGraph object and calculate the Yamada polynomial

# Instantiate the SpatialGraph object
sg = SpatialGraph(nodes=nodes,
                  node_positions=node_positions,
                  edges=edges)

# Plot the Spatial Graph in 3D and the projected 2D plane to see what's going on. Crossings will be circled in red.
# Note: Crossings occur when two edges that do not intersect, but appear to when they are projected onto a 2D plane.
# sg.plot()

# Create the spatial graph diagram (necessary for calculating the Yamada polynomial)
sgd = sg.create_spatial_graph_diagram()

# Calculate the Yamada polynomial
# We use the normalized version because it is more useful for comparing polynomials
yamada_polynomial = sgd.normalized_yamada_polynomial()
print("Yamada Polynomial: ", yamada_polynomial)





