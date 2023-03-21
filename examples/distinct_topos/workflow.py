"""EXAMPLE

Extract spatial graphs from jsons and calculate their Yamada polynomials.

"""

# %% Import local packages
import os

# %% Import third-party packages

import numpy as np
from yamada import extract_graph_from_json_file, SpatialGraph

# %% Set the random seed for reproducibility (used in the SpatialGraph.project() method)

np.random.seed(0)

# %% Set file locations

# Obtain the local path of this example's directory
directory = os.path.dirname(__file__) + '/'

# User Input: Set the path to the json file you want to evaluate
# filepath = directory + "G6/C1/G6C1I0.json"
filepath = directory + "G10/C4/G10C4I7.json"

# %% Extract the spatial graph from the json file

nodes, node_positions, edges = extract_graph_from_json_file(filepath)


# %% Create a SpatialGraph object and calculate the Yamada polynomial

# Instantiate the SpatialGraph object
sg = SpatialGraph(nodes=nodes,
                  node_positions=node_positions,
                  edges=edges)

# Plot the Spatial Graph in 3D and the projected 2D plane to verify everything looks good.
# Crossings will be circled in red.
sg.plot()

# Create the spatial graph diagram (necessary for calculating the Yamada polynomial)
sgd = sg.create_spatial_graph_diagram()

# Calculate the Yamada polynomial
yamada_polynomial = sgd.normalized_yamada_polynomial()
print("Yamada Polynomial: ", yamada_polynomial)
