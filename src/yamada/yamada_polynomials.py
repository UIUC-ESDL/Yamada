"""
Enumerating spatial graph diagrams
==================================

Current code is limited to trivalent system architectures.

The basic approach differs somewhat from the one in the paper.
Namely, I use "plantri" to enumerate possible diagram shadows with the
specified number of crossings::

  http://users.cecs.anu.edu.au/~bdm/plantri/

You need to compile plantri and have it in the same directory as this
file (or somewhere in your path) for the enumeration to work.

Due to a limitation of plantri, this restricts us to shadows which are
"diagrammatically prime" in that there is not a circle meeting the
shadow in two points that has vertices of the shadow on both sides.
Equivalently, the dual planar graph is simple.

If the system architecture graph cannot be disconnected by removing
two edges, this only excludes shadows all of whose spatial diagrams
are the connect sum of a spatial graph diagram with the desired system
architecture and a knot.  Presumably, we would want to exclude such in
any event.  However, the example in Case Study 1 can be so
disconnected...

Validation
==========

Compared to Dobrynin and Vesnin:

1. For the theta graph, the list of Yamada polynomials through 5
   crossings matches after removing the non-prime examples from their
   list (theta_3, theta_5, theta_10, theta_14).

2. For the tetrahedral graph, the list of Yamada polynomials through 4
   crossings matches after removing the non-prime Omega_5.

Note: The way this script is written w/ pickling you must import this script into another script
rather than directly calculate Yamada polynomials in this script (you'll get error messages)

"""

import networkx as nx
import pickle
import collections
from cypari import pari


def has_cut_edge(abstract_graph):
    """
    """
    G = nx.Graph(abstract_graph)
    for u, v in nx.bridges(G):
        if abstract_graph.number_of_edges(u, v) == 1:
            return True
    return False


def an_edge(graph):
    return next(iter(graph.edges()))


def remove_valence_two_vertices(graph):
    """

    """
    G = graph.copy()
    valence_two = {v for v, d in G.degree if d == 2}
    T = G.subgraph(valence_two)
    new_edges = []
    for comp in nx.connected_components(T):
        C = T.subgraph(comp)
        if C.number_of_nodes() == C.number_of_edges():
            x = next(iter(comp))
            y = x
        else:
            if len(comp) == 1:
                c = next(iter(comp))
                x, y = [e[1] for e in G.edges(c)]
            else:
                a, b = [c for c, d in C.degree if d == 1]
                x = [e[1] for e in G.edges(a) if e[1] not in comp][0]
                y = [e[1] for e in G.edges(b) if e[1] not in comp][0]
        new_edges.append((x, y))
    G.remove_nodes_from(valence_two)
    G.add_edges_from(new_edges)
    return G


def graph_hash(graph):
    return nx.weisfeiler_lehman_graph_hash(graph, iterations=3)


H_poly_cache = collections.defaultdict(list)


def h_poly(abstract_graph):
    """

    """
    A = pari('A')
    G = abstract_graph

    if not isinstance(G, nx.MultiGraph):
        G = nx.MultiGraph(G)
    if G.number_of_nodes() == 0:
        return pari(1)

    if nx.is_connected(G):
        its_hash = graph_hash(G)
        for H, poly in H_poly_cache[its_hash]:
            if nx.is_isomorphic(G, H):
                return poly
        G_for_cache = G.copy()

        if has_cut_edge(G):
            ans = pari(0)

        else:
            G = remove_valence_two_vertices(G)

            loop_factor = pari(1)

            loops = [e for e in G.edges() if e[0] == e[1]]
            for u, v in loops:
                G.remove_edge(u, v)
                loop_factor = -loop_factor * (A + 1 + A ** -1)
            if G.number_of_nodes() == 1:
                ans = -loop_factor
            elif G.number_of_nodes() == 2:
                b = -(A ** -1 + 2 + A)
                q = G.number_of_edges()

                h = ((b + 1) - (b + 1) ** q) / b

                ans = loop_factor * h
            else:
                e = an_edge(G)
                G_mod_e = nx.contracted_edge(G, e, self_loops=True)
                G_mod_e.remove_edge(e[0], e[0])
                G.remove_edge(*e)
                ans = (h_poly(G_mod_e) + h_poly(G)) * loop_factor

        H_poly_cache[its_hash].append((G_for_cache, ans))
        return ans
    else:

        ans = pari(1)

        for vertices in nx.connected_components(G):
            S = G.subgraph(vertices).copy()
            h = h_poly(S)
            if h == 0:
                # return R(0)
                return pari(0)

            ans = ans * h
        return ans


class EntryPoint:
    def __init__(self, vertex_like, index):
        self.vertex = vertex_like
        self.index = index

    def __eq__(self, other):
        return self.vertex == other.vertex and self.index == other.index

    def __hash__(self):
        return hash((self.vertex, self.index))

    def __repr__(self):
        return "<EP %s %d>" % (self.vertex, self.index)

    def next_corner(self):
        """
        Moves around face clockwise.
        """
        V, i = self.vertex, self.index
        j = (i + 1) % V.degree
        W, k = V.adjacent[j]
        return EntryPoint(W, k)


class BaseVertex:
    """
    A flat vertex has n inputs, labeled 0, 1, ..., n-1 in
    anticlockwise order.

    The adjacents should be edges, not other flat vertices.
    """

    def __init__(self, degree, label):
        self.label = label
        self.degree = degree
        self.adjacent = degree * [None]

    def __getitem__(self, i):
        return (self, i % self.degree)

    def __setitem__(self, i, other):
        o, j = other
        i = i % self.degree
        self.adjacent[i] = other
        o.adjacent[j] = (self, i)

    def __repr__(self):
        return repr(self.label)

    def entry_points(self):
        return [EntryPoint(self, i) for i in range(self.degree)]


class Vertex(BaseVertex):
    pass


class Crossing(BaseVertex):
    """
    A crossing has four inputs, labeled 0, 1, 2, 3 in anticlockwise
    order.  Convention is 0 - 2 crosses *under* 1, 3.
    """

    def __init__(self, label):
        BaseVertex.__init__(self, 4, label)

    def flow(self, i):
        return self.adjacent[(i + 2) % 4]


class Edge(BaseVertex):
    def __init__(self, label):
        BaseVertex.__init__(self, 2, label)

    def fuse(self):
        """
        Joins the incoming and outgoing strands and removes
        self from the picture.
        """
        (A, i), (B, j) = self.adjacent
        A[i] = B[j]

    def flow(self, i):
        return self.adjacent[(i + 1) % 2]


class SpatialGraphDiagram:
    """

    """

    def __init__(self, data, check=True):
        # Need labels of vertices/crossings to be unique and hashable
        self.data = {d.label: d for d in data}
        assert len(data) == len(self.data)
        self.crossings = [d for d in data if isinstance(d, Crossing)]
        self.vertices = [d for d in data if isinstance(d, Vertex)]
        self.edges = [d for d in data if isinstance(d, Edge)]
        if len(self.edges) == 0 and len(data) > 0:
            self._inflate_edges()
        if check:
            self._check()

    def faces(self):
        """
        The faces are the complementary regions of the diagram. Each
        face is given as a list of corners of BaseVertices as one goes
        around *clockwise*.  These corners are recorded as
        EntryPoints, where EntryPoints(c, j) denotes the corner of the
        face abutting crossing c between strand j and j + 1.

        Alternatively, the sequence of EntryPoints can be regarded as
        the *heads* of the oriented edges of the face.
        """
        entry_points = []
        for V in self.data.values():
            entry_points += V.entry_points()
        corners = set(entry_points)
        faces = []
        while len(corners):
            face = [corners.pop()]
            while True:
                next = face[-1].next_corner()
                if next == face[0]:
                    faces.append(face)
                    break
                else:
                    corners.remove(next)
                    face.append(next)

        return faces

    def euler(self):
        v = len(self.crossings) + len(self.vertices)
        e = len(self.edges)
        f = len(self.faces())
        return v - e + f

    def is_planar(self):
        return self.euler() == 2 * len(list(nx.connected_components(self.projection_graph())))

    def _check(self):
        assert 2 * len(self.edges) == sum(d.degree for d in self.crossings + self.vertices)
        for C in self.crossings:
            assert all(isinstance(v, Edge) for v, j in C.adjacent)
        for V in self.vertices:
            assert all(isinstance(v, Edge) for v, j in V.adjacent)
        for E in self.edges:
            assert all(not isinstance(v, Edge) for v, j in E.adjacent)
        assert self.is_planar()

    def _inflate_edges(self):
        curr_index = 0
        edges = []
        for A in self.crossings + self.vertices:
            for i in range(A.degree):
                B, j = A.adjacent[i]
                if not isinstance(B, Edge):
                    E = Edge(curr_index)
                    curr_index += 1
                    edges.append(E)
                    self.data[E.label] = E
                    E[0] = (A, i)
                    E[1] = (B, j)
        self.edges = edges

    def copy(self):
        return pickle.loads(pickle.dumps(self))

    def projection_graph(self):
        G = nx.MultiGraph()
        for e in self.edges:
            v = e.adjacent[0][0].label
            w = e.adjacent[1][0].label
            G.add_edge(v, w)
        return G

    def underlying_graph(self):
        G = nx.MultiGraph()
        vertex_inputs = set()
        for V in self.vertices:
            vertex_inputs.update((V, i) for i in range(V.degree))
        edges_used = 0
        while len(vertex_inputs):
            V, i = vertex_inputs.pop()
            W, j = V.adjacent[i]
            while not isinstance(W, Vertex):
                if isinstance(W, Edge):
                    edges_used += 1
                W, j = W.flow(j)
            vertex_inputs.remove((W, j))
            v, w = V.label, W.label
            G.add_edge(v, w)
        if edges_used == len(self.edges):
            return G

    def underlying_planar_embedding(self):
        G = nx.PlanarEmbedding()
        parts = self.vertices + self.crossings + self.edges
        for A in parts:
            for i in range(A.degree):
                B, j = A.adjacent[i]
                ref_nbr = None if i == 0 else A.adjacent[i - 1][0].label
                G.add_half_edge_ccw(A.label, B.label, ref_nbr)

        G.check_structure()
        return G

    def remove_crossing(self, C):
        self.crossings.remove(C)
        self.data.pop(C.label)

    def remove_edge(self, E):
        self.edges.remove(E)
        self.data.pop(E.label)

    def add_vertex(self, V):
        self.vertices.append(V)
        self.data[V.label] = V

    def short_cut(self, crossing, i0):
        i1 = (i0 + 1) % 4
        E0, j0 = crossing.adjacent[i0]
        E1, j1 = crossing.adjacent[i1]
        if E0 == E1:
            V0 = Vertex(2, repr(E0) + '_stopper')
            self.add_vertex(V0)
            V0[0] = E0[j0]
            V0[1] = E1[j1]
        else:
            E1[j1] = E0[j0]
            E1.fuse()
            self.remove_edge(E1)

    def has_R1(self):
        for C in self.crossings:
            for i in range(4):
                E, e = C.adjacent[i]
                D, d = E.flow(e)
                if D == C and (i + 1) % 4 == d:
                    return True
        return False

    def has_R6(self):
        for V in self.vertices:
            for i in range(V.degree):
                E, e = V.adjacent[i]
                A, a = E.flow(e)
                if isinstance(A, Crossing):
                    E, e = V.adjacent[(i + 1) % V.degree]
                    B, b = E.flow(e)
                    if A == B and (b + 1) % 4 == a:
                        return True
        return False

    def has_R2(self):
        for E in self.edges:
            A, a = E.adjacent[0]
            if isinstance(A, Crossing):
                B, b = E.adjacent[1]
                if isinstance(B, Crossing):
                    if (a + b) % 2 == 0:
                        return True
        return False

    def yamada_polynomial(self, check_pieces=False):

        A = pari('A')

        if len(self.crossings) == 0:
            return h_poly(self.projection_graph())

        C = self.crossings[0]
        c = C.label

        # S_plus
        S_plus = self.copy()
        C_plus = S_plus.data[c]
        S_plus.remove_crossing(C_plus)
        S_plus.short_cut(C_plus, 0)
        S_plus.short_cut(C_plus, 2)
        if check_pieces:
            S_plus._check()

        # S_minus
        S_minus = self.copy()
        C_minus = S_minus.data[c]
        S_minus.remove_crossing(C_minus)
        S_minus.short_cut(C_minus, 1)
        S_minus.short_cut(C_minus, 3)
        if check_pieces:
            S_minus._check()

        # S_0
        S_0 = self.copy()
        C_0 = S_0.data[c]
        S_0.remove_crossing(C_0)

        V = Vertex(4, repr(C_0) + '_smushed')
        S_0.add_vertex(V)

        for i in range(4):
            B, j = C_0.adjacent[i]
            V[i] = B[j]

        if check_pieces:
            S_0._check()

        Y_plus = S_plus.yamada_polynomial()
        Y_minus = S_minus.yamada_polynomial()
        Y_0 = S_0.yamada_polynomial()
        return A * Y_plus + (A ** -1) * Y_minus + Y_0


def get_coefficients_and_exponents(poly):

    # Assumes all denominators are only A**n with no coefficient
    coefficients = poly.numerator().Vec()
    coeff_len = len(coefficients)

    exponents = []
    degree = poly.poldegree()

    for _ in range(coeff_len):
        exponents.append(degree)
        degree -= 1

    return coefficients, exponents

def reverse_poly(poly):
    """

    """

    A = pari('A')

    coeffs, exps = get_coefficients_and_exponents(poly)

    ans = pari(0)

    for c, e in zip(coeffs, exps):
        ans += c * A ** (-e)

    return ans


def normalize_poly(poly):
    """
    The Yamada polynomial is only defined up to a power of (-A)^n.

    Also, we don't want to distinguish between a spatial graph and its
    mirror image, which corresponds to interchanging A <-> A^(-1).
    """

    A = pari('A')

    _, exps = get_coefficients_and_exponents(poly)
    a, b = min(exps), max(exps)
    ans1 = (-A) ** (-a) * poly
    ans2 = (-A) ** b * reverse_poly(poly)

    return min([ans1, ans2], key=list)