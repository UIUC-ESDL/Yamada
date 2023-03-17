import networkx as nx
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