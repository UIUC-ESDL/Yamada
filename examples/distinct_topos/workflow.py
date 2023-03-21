"""

"""

import numpy as np
from yamada.spatial_graph_enumeration import extract_graph_from_json_file, read_json_file
from yamada import SpatialGraph

# Set the random seed for reproducibility
np.random.seed(0)

filepath = "C:/Users/cpgui/PycharmProjects/Yamada/examples/distinct_topos/G6/C1/G6C1I0.json"


nodes, node_positions, edges = extract_graph_from_json_file(filepath)

sg = SpatialGraph(nodes=nodes,
                  node_positions=node_positions,
                  edges=edges)
sg.project()
sg.plot()
sgd = sg.create_spatial_graph_diagram()

print(sgd.normalized_yamada_polynomial())
