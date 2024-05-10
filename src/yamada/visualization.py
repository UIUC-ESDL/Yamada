import networkx as nx
from networkx.algorithms.planar_drawing import triangulate_embedding
import numpy as np
from .enumeration import split_edges


def tutte_system(planar_graph):
    G, outer = triangulate_embedding(planar_graph, fully_triangulate=False)
    node_to_index = {node: index for index, node in enumerate(G.nodes())}
    n = G.number_of_nodes()
    assert n == planar_graph.number_of_nodes()
    inner_indices = np.array([node not in outer for node in G.nodes()])
    L = nx.laplacian_matrix(G).toarray()
    L = L[inner_indices, :]
    M = np.zeros((len(outer), n))
    for i, node in enumerate(outer):
        M[i, node_to_index[node]] = 1
    A = np.vstack([L, M])
    Z = np.zeros(A.shape)
    B = np.block([[A, Z], [Z, A]])
    # set locations of boundary nodes
    t = np.linspace(0, 2*np.pi, len(outer), endpoint=False)
    x, y = 100*np.cos(t), 100*np.sin(t)
    zeros = np.zeros(L.shape[0])
    b = np.hstack([zeros, x, zeros, y])
    return G, B, b


def tutte_embedding_positions(planar_graph):
    n = planar_graph.number_of_nodes()
    G, A, b = tutte_system(planar_graph)
    pos = np.linalg.solve(A, b)
    pos = np.rint(pos)
    x, y = pos[:n], pos[n:]
    ans = dict()
    for i, node in enumerate(G.nodes()):
        ans[node] = (int(x[i]), int(y[i]))
    return ans


def _position_spatial_graph_in_3d(G, z_height=20):
    def norm_label(X):
        L = X.label
        return repr(L) if not isinstance(L, str) else L
        
    P = G.underlying_planar_embedding()
    planar_pos = tutte_embedding_positions(P)
    system_node_pos = dict()
    for V in G.vertices:
        L = norm_label(V)
        x, y = planar_pos[V.label]
        system_node_pos[L] = (x, y, 0)

    other_node_pos = dict()
    for C in G.crossings:
        L = norm_label(C)
        x, y = planar_pos[C.label]
        other_node_pos[L + '+'] = (x, y, z_height)
        other_node_pos[L + '-'] = (x, y, -z_height)

    nodes_so_far = system_node_pos.copy()
    nodes_so_far.update(other_node_pos)

    def end_label(edge, i):
        i = i % 2
        X, x = edge.adjacent[i]
        L = norm_label(X)
        if X in G.crossings:
            L = L + '-' if x % 2 == 0 else L + '+'
        return L

    for E in G.edges:
        L = norm_label(E)
        x, y = planar_pos[E.label]
        A = end_label(E, 0)
        B = end_label(E, 1)
        z = (nodes_so_far[A][2] + nodes_so_far[B][2]) // 2
        other_node_pos[L] = (x, y, z)
        
    segments = list()
    vertex_inputs = set()
    for V in G.vertices:
        vertex_inputs.update((V, i) for i in range(V.degree))
    while len(vertex_inputs):
        V, i = vertex_inputs.pop()
        W, j = V.adjacent[i]
        one_seg = []
        while not W in G.vertices:
            if W in G.edges:
                L = norm_label(W)
                A = end_label(W, j)
                B = end_label(W, j + 1)
                one_seg += [A, L]
            W, j = W.flow(j)
        one_seg.append(norm_label(W))
        vertex_inputs.remove((W, j))
        segments.append(one_seg)

    return system_node_pos, other_node_pos, segments
        
def position_spatial_graph_in_3d(G, z_height=20):

    system_node_pos, other_node_pos, segments = _position_spatial_graph_in_3d(G, z_height)

    nodes = list(system_node_pos.keys())
    node_positions = list(system_node_pos.values())

    crossings = list(other_node_pos.keys())
    crossing_positions = list(other_node_pos.values())


    # Extract non crossings from crossings
    noncrossings, noncrossing_positions = zip(*[(crossing, crossing_position) for crossing, crossing_position in zip(crossings, crossing_positions) if "C" not in crossing])

    # Only extract non crossings
    # Merge nodes and crossings
    nodes.extend(noncrossings)
    node_positions.extend(noncrossing_positions)

    segments = split_edges(segments)

    # Convert segments from lists to tuples

    return nodes, node_positions, segments


def position_spatial_graphs_in_3d(ust_dict, z_height=20):

    sg_inputs = []

    for ust in list(ust_dict.values()):

        nodes, node_positions, edges = position_spatial_graph_in_3d(ust, z_height)
        sg_inputs.append((nodes, node_positions, edges))

    return sg_inputs


