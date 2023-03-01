# Cyclic edge order
from matplotlib import pyplot as plt
import numpy as np

nodes = ['a', 'b', 'c', 'd', 'e']
node_positions = np.array([[1, 1], [2, 2], [2.25, 1.5], [0, 2], [0, 0]])
edges = [('a', 'b'), ('a', 'c'), ('a', 'd'), ('a', 'e')]

reference_node = 'a'
reference_position = node_positions[nodes.index(reference_node)]

shifted_node_positions = node_positions - reference_position



ab = np.array([[1, 1], [2, 2]])
ac = np.array([[1, 1], [2.25, 1.5]])
ad = np.array([[1, 1], [0, 2]])
ae = np.array([[1, 1], [0, 0]])

edges = [ab, ac, ad, ae]

# todo set first index to origin

plt.plot(ab[:, 0], ab[:, 1])
plt.plot(ac[:, 0], ac[:, 1])
plt.plot(ad[:, 0], ad[:, 1])
plt.plot(ae[:, 0], ae[:, 1])

edge_labels = ['ab', 'ac', 'ad', 'ae']
plt.legend(['ab', 'ac', 'ad', 'ae'])

plt.show()

ab_v = ab[1]
ac_v = ac[1]
ad_v = ad[1]
ae_v = ae[1]

# Horizontal line
reference_vector = [1, 0]

edges_v = [ab_v, ac_v, ad_v, ae_v]


# convert to unit vectors
# ab_u = ab / np.linalg.norm(ab)
# ac_u = ac / np.linalg.norm(ac)
# ad_u = ad / np.linalg.norm(ad)

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'"""
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


rotations = []

for edge_v in edges_v:
    rotations.append(angle_between(reference_vector, edge_v))

sorted_index = np.argsort(rotations)

ccw_edge_ordering = {}
for edge, order in zip(edge_labels, sorted_index):
    ccw_edge_ordering[edge] = order
