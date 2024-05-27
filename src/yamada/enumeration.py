import networkx as nx
import collections
import itertools
import subprocess
import io
import time
from yamada.diagram_elements import Vertex, Crossing, Edge
from yamada.spatial_graph_diagrams import SpatialGraphDiagram


def shadows_via_plantri_by_ascii(plantri_directory, num_tri_verts, num_crossings):
    assert num_tri_verts % 2 == 0
    vertices = num_tri_verts + num_crossings
    edges = (3 * num_tri_verts + 4 * num_crossings) // 2
    faces = 2 - vertices + edges
    cmd = [plantri_directory+'plantri',
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


def shadows_via_plantri_by_edge_codes(plantri_directory, num_tri_verts, num_crossings):
    assert num_tri_verts % 2 == 0
    vertices = num_tri_verts + num_crossings
    edges = (3 * num_tri_verts + 4 * num_crossings) // 2
    faces = 2 - vertices + edges
    cmd = [plantri_directory+'plantri',
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


def spatial_graph_diagrams_fixed_crossings(plantri_directory, G, crossings):
    """
    Let's start with the theta graph

    >>> T = nx.MultiGraph(3*[(0, 1)])
    >>> len(list(spatial_graph_diagrams_fixed_crossings(T, 3)))
    2
    """
    assert all(d == 3 for v, d in G.degree)
    assert all(a != b for a, b in G.edges())

    raw_shadows = shadows_via_plantri_by_edge_codes(plantri_directory, G.number_of_nodes(), crossings)

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


def enumerate_yamada_classes(plantri_directory, G, max_crossings):
    examined = 0
    polys = dict()
    for crossings in range(0, max_crossings + 1):
        for D in spatial_graph_diagrams_fixed_crossings(plantri_directory, G, crossings):
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


def num_automorphisms(graph):
    matcher = nx.isomorphism.GraphMatcher(graph, graph)
    return len(list(matcher.isomorphisms_iter()))