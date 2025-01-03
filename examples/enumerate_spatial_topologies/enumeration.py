import networkx as nx
from yamada import enumerate_yamada_classes

G = nx.MultiGraph([(0,1), (0,1), (0,1), (2,3), (2,3),(2,5),(3,4),(4,5),(4,5)])

number_of_crossings = 4
data = enumerate_yamada_classes('./plantri53/', G, number_of_crossings)
print(data)