"""A module to computer to H polynomial of an Abstract Graph

Computation of the H polynomial is based on the following paper:

SYSTEMATIC ENUMERATION AND IDENTIFICATION OF UNIQUE SPATIAL TOPOLOGIES OF 3D SYSTEMS USING SPATIAL GRAPH REPRESENTATIONS
Peddada et al.
DOI: 10.1115/DETC2021-66900

P1. H(empty graph) = 1 and H(simple loop) = A + 1 + A^(-1)
P2. H(G_1 disjoint union G_2)      =  H(G_1) * H(G_2)
P3. H(G_1 union G_2)               = -H(G_1) * H(G_2)
P4. If G has a cut edge, then H(G) =  0
P5. Let e be a non-loop edge of graph G. Then H(G) = H(G/e) + H(G-e) where G/e is the graph obtained from G by
    contracting e to a point and G-e is G with e deleted.

"""

import networkx as nx
import collections
from cypari import pari


def has_cut_edge(abstract_graph):

    """
    Determines if the abstract graph has a cut edge. A cut edge is an edge that, if removed, would increase the number
    of disconnected sub-graphs in the graph.
    """

    g = nx.Graph(abstract_graph)

    for u, v in nx.bridges(g):
        if abstract_graph.number_of_edges(u, v) == 1:
            return True

    return False


def an_edge(graph):

    """
    A generator that returns the next edge in the graph.
    """

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

    """
    Returns a hash of the graph.

    The graph hash is used to cache the results of the H polynomial computation and avoid recomputing the H polynomial.
    """

    return nx.weisfeiler_lehman_graph_hash(graph, iterations=3)


H_poly_cache = collections.defaultdict(list)


def h_poly(abstract_graph):

    """

    """

    A = pari('A')
    G = abstract_graph

    # Validate the input format
    if not isinstance(G, nx.MultiGraph):
        G = nx.MultiGraph(G)

    # H Polynomial property P1: H(empty graph) = 1
    if G.number_of_nodes() == 0:
        return pari(1)


    if nx.is_connected(G):

        # Check if the graph has already been computed
        its_hash = graph_hash(G)
        for H, poly in H_poly_cache[its_hash]:
            if nx.is_isomorphic(G, H):
                return poly
        G_for_cache = G.copy()

        # H Polynomial property P4. If G has a cut edge, then H(G) =  0
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

            # H Polynomial property P5. H(G) = H(G/e) + H(G-e)
            else:
                e = an_edge(G)
                G_mod_e = nx.contracted_edge(G, e, self_loops=True)
                G_mod_e.remove_edge(e[0], e[0])
                G.remove_edge(*e)
                ans = (h_poly(G_mod_e) + h_poly(G)) * loop_factor

        H_poly_cache[its_hash].append((G_for_cache, ans))
        return ans

    # If the graph is not connected, then apply the H polynomial property P2
    # H(G_1 disjoint union G_2) = H(G_1) * H(G_2)
    else:

        ans = pari(1)

        for vertices in nx.connected_components(G):
            S = G.subgraph(vertices).copy()
            h = h_poly(S)
            if h == 0:
                return pari(0)

            ans = ans * h
        return ans