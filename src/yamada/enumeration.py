import networkx as nx
import pickle
import collections
import itertools
import subprocess
import io
import time
import glob
from .spatial_graph_diagrams import Vertex, Edge, Crossing, SpatialGraphDiagram
from .utilities import read_json_file


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

# def extract_graph_from_dict(data, index):






# def generate_random_layout(layout):
#     """
#     Generates random layouts using a force-directed algorithm

#     Initially assumes 0 rotation and 1x6 design vector


#     :return:
#     """

#     g = nx.MultiGraph()
#     g.add_nodes_from(layout.nodes)
#     g.add_edges_from(layout.edges)

#     # Optimal distance between nodes
#     k = 1

#     scale = 6

#     # TODO remove this random number seed for actual problems
#     seed = 11

#     # Dimension of layout
#     dim = 3

#     positions = nx.spring_layout(g, k=k, dim=dim, scale=scale, seed=seed)

#     # Generate random angles too?

#     # Temporarily pad zeros for rotations
#     design_vectors = []
#     rotation = np.array([0, 0, 0])

#     for i in positions:
#         position = positions[i]
#         design_vector = np.concatenate((position, rotation))
#         design_vectors.append(design_vector)

#     # Flatten design vectors
#     # TODO Make more efficient?
#     design_vector = np.concatenate(design_vectors)

#     return design_vector


# """Generate Yamada polynomial spatial topologies..."""








def shadows_via_plantri_by_ascii(num_tri_verts, num_crossings):
    assert num_tri_verts % 2 == 0
    vertices = num_tri_verts + num_crossings
    edges = (3 * num_tri_verts + 4 * num_crossings) // 2
    faces = 2 - vertices + edges
    cmd = ['plantri',
           '-p -d',  # simple planar maps, but return the dual
           '-f4',  # maximum valence in the returned dual is <= 4
           '-c1',  # graph should be 1-connected
           '-m2',  # no valence 1 vertices = no loops in the dual
           '-a',  # return in ascii format
           '-e%d' % edges,
           '%d' % faces]
    proc = subprocess.run(' '.join(cmd), shell=True, text=True, capture_output=True)
    ans = []
    for line in proc.stdout.splitlines():
        graph_data = line.split()[1].split(',')
        counts = collections.Counter(len(v) for v in graph_data)
        assert counts[3] == num_tri_verts and counts[4] == num_crossings
        ans.append(graph_data)
    return ans


def read_edge_code(stream, size):
    """
    Read 1 byte form of edge code
    """
    ans = [[]]
    for _ in range(size):
        i = int.from_bytes(stream.read(1), 'big')
        if i < 255:
            ans[-1].append(i)
        else:
            ans.append([])
    return ans


def shadows_via_plantri_by_edge_codes(num_tri_verts, num_crossings):
    assert num_tri_verts % 2 == 0
    vertices = num_tri_verts + num_crossings
    edges = (3 * num_tri_verts + 4 * num_crossings) // 2
    faces = 2 - vertices + edges
    cmd = ['.plantri',
           '-p -d',  # simple planar maps, but return the dual
           '-f4',  # maximum valence in the returned dual is <= 4
           '-c1',  # graph should be 1-connected
           '-m2',  # no valence 1 vertices = no loops in the dual
           '-E',  # return binary edge code format
           '-e%d' % edges,
           '%d' % faces]
    proc = subprocess.run(' '.join(cmd), shell=True, capture_output=True)
    stdout = io.BytesIO(proc.stdout)
    assert stdout.read(13) == b'>>edge_code<<'
    shadows = []
    while True:
        b = stdout.read(1)
        if len(b) == 0:
            break
        size = int.from_bytes(b, 'big')
        assert size != 0
        shadows.append(read_edge_code(stdout, size))

    return shadows


class Shadow:
    def __init__(self, edge_codes):
        self.edge_codes = edge_codes
        self.vertices = [edges for edges in edge_codes if len(edges) == 3]
        self.crossings = [edges for edges in edge_codes if len(edges) == 4]
        self.num_edges = sum(len(edges) for edges in edge_codes) // 2

    def spatial_graph_diagram(self, signs=None, check=True):
        num_cross = len(self.crossings)
        if signs is None:
            signs = num_cross * [0]
        else:
            assert len(signs) == num_cross

        classes = [Edge(i) for i in range(self.num_edges)]
        for v, edges in enumerate(self.vertices):
            d = len(edges)
            V = Vertex(d, 'V%d' % v)
            classes.append(V)
            for i, e in enumerate(edges):
                E = classes[e]
                e = 0 if E.adjacent[0] is None else 1
                V[i] = E[e]

        for c, edges in enumerate(self.crossings):
            C = Crossing('C%d' % c)
            classes.append(C)
            for i, e in enumerate(edges):
                E = classes[e]
                e = 0 if E.adjacent[0] is None else 1
                C[(i + signs[c]) % 4] = E[e]

        return SpatialGraphDiagram(classes, check=check)


# def spatial_graph_diagrams_from_shadow(shadow, signs):
#    assert len(signs

# TODO Compile Plantri for Windows
def spatial_graph_diagrams_fixed_crossings(G, crossings):
    """
    Let's start with the theta graph

    >>> T = nx.MultiGraph(3*[(0, 1)])
    >>> len(list(spatial_graph_diagrams_fixed_crossings(T, 3)))
    2
    """
    assert all(d == 3 for v, d in G.degree)
    assert all(a != b for a, b in G.edges())

    raw_shadows = shadows_via_plantri_by_edge_codes(G.number_of_nodes(), crossings)

    for raw_shadow in raw_shadows:
        shadow = Shadow(raw_shadow)
        diagram = shadow.spatial_graph_diagram(check=False)
        U = diagram.underlying_graph()
        if U is not None:
            if nx.is_isomorphic(G, U):
                if not diagram.has_r6():
                    num_cross = len(shadow.crossings)
                    if num_cross == 0:
                        yield diagram
                    else:
                        for signs in itertools.product((0, 1), repeat=num_cross - 1):
                            signs = (0,) + signs
                            D = shadow.spatial_graph_diagram(signs=signs, check=False)
                            if not D.has_r2():
                                yield D


def enumerate_yamada_classes(G, max_crossings):
    examined = 0
    polys = dict()
    for crossings in range(0, max_crossings + 1):
        for D in spatial_graph_diagrams_fixed_crossings(G, crossings):
            p = D.normalized_yamada_polynomial()
            if p not in polys:
                polys[p] = D
            examined += 1
    return polys, examined


def to_poly(diagram):
    p = diagram.normalized_yamada_polynomial()
    return p, diagram


def enumerate_yamada_classes_multicore(G, max_crossings, pool):
    examined = 0
    polys = dict()
    timings = dict()
    for crossings in range(0, max_crossings + 1):
        start = time.time()
        diagrams = spatial_graph_diagrams_fixed_crossings(G, crossings)
        some_polys = pool.imap_unordered(to_poly, diagrams)
        for p, D in some_polys:
            if p not in polys:
                polys[p] = D
            examined += 1
        timings[crossings] = time.time() - start
    return polys, timings, examined


def pickle_yamada(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)


def load_yamada(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

def read_pickle(nodes):
    file = open(max(glob.glob(f'pickles/G{nodes}_C*.pickle')), 'rb')
    return pickle.load(file)

def num_automorphisms(graph):
    matcher = nx.isomorphism.GraphMatcher(graph, graph)
    return len(list(matcher.isomorphisms_iter()))