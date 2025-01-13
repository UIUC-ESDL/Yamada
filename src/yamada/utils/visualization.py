import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.planar_drawing import triangulate_embedding
import numpy as np
from yamada.sgd.sgd_analysis import split_edges


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
        
    P = G.planar_embedding()
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
        node_positions = {node: position for node, position in zip(nodes, node_positions)}
        sg_inputs.append((nodes, node_positions, edges))

    return sg_inputs

def plot_spatial_graph(nodes, node_positions, edges):

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot nodes
    for node, position in node_positions.items():
        ax.scatter(*position, label=node)

    # Plot edges
    for edge in edges:
        edge_positions = [node_positions[node] for node in edge]
        edge_positions = np.array(edge_positions)
        ax.plot(edge_positions[:, 0], edge_positions[:, 1], edge_positions[:, 2])

    plt.show()



# def add_curved_edge(ax, pos, n1, n2, over=True):
#     """Add a curved edge between two nodes."""
#     x1, y1 = pos[n1]
#     x2, y2 = pos[n2]
#     mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
#     curve_factor = 0.2
#     control_x = mid_x + curve_factor * (y2 - y1)
#     control_y = mid_y - curve_factor * (x2 - x1)
#
#     path = Path([(x1, y1), (control_x, control_y), (x2, y2)],
#                 [Path.MOVETO, Path.CURVE3, Path.CURVE3])
#     patch = PathPatch(path, edgecolor='blue' if over else 'orange', lw=2, zorder=2 if over else 1)
#     ax.add_patch(patch)

# def plot_spatial_graph(graph, pos):
#     """Plot the graph with crossings visualized."""
#     fig, ax = plt.subplots(figsize=(8, 8))
#     ax.set_aspect('equal')
#
#     # Draw nodes
#     for node, (x, y) in pos.items():
#         ax.plot(x, y, 'o', color='black', zorder=3)
#         ax.text(x, y, str(node), fontsize=12, ha='center', va='center')
#
#     # Draw edges
#     for edge in graph.edges:
#         n1, n2 = edge
#         # Example: Assume alternating "over" and "under" crossings
#         over = graph.edges[edge].get('over', True)
#         add_curved_edge(ax, pos, n1, n2, over)
#
#     plt.axis('off')
#     plt.show()
#
# # Create a sample graph
# G = nx.Graph()
# G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])  # A square graph
#
# # Add "over/under" attributes to crossings
# for i, edge in enumerate(G.edges):
#     G.edges[edge]['over'] = (i % 2 == 0)
#
# # Compute positions
# pos = nx.planar_layout(G)  # Use planar layout for simplicity
# plot_spatial_graph(G, pos)


# def plot(self, highlight_nodes=None, highlight_labels=None):
#     """
#     Plots the spatial graph diagram, labeling intermediate edges with index numbers
#     and intermediate nodes with full index assignments.
#     """
#
#     # Step 1: Create the planar-friendly graph
#     planar_graph, node_labels, edge_labels = self.planar_embedding()
#
#     # Step 2: Generate the planar embedding
#     is_planar, embedding = nx.check_planarity(planar_graph)
#     if not is_planar:
#         raise ValueError("The graph is not planar!")
#     pos = nx.planar_layout(embedding)
#
#     # Step 3: Separate node types
#     edges = [n for n, d in planar_graph.nodes(data=True) if d["type"] == "Edge"]
#     vertices = [n for n, d in planar_graph.nodes(data=True) if d["type"] == "Vertex"]
#     crossings = [n for n, d in planar_graph.nodes(data=True) if d["type"] == "Crossing"]
#     regular_nodes = [n for n, d in planar_graph.nodes(data=True) if d["type"] != "Intermediate"]
#     intermediate_nodes = [n for n, d in planar_graph.nodes(data=True) if d["type"] == "Intermediate"]
#
#     # Initialize the plot
#     plt.figure(figsize=(12, 12))
#
#     # Draw the edges
#     nx.draw_networkx_edges(planar_graph, pos)
#
#     # Label the edges
#     nx.draw_networkx_edge_labels(
#         planar_graph,
#         pos,
#         edge_labels=edge_labels,
#         font_size=8,
#         font_color="black",
#         rotate=False,
#     )
#
#     # Draw the nodes
#     nx.draw_networkx_nodes(
#         planar_graph,
#         pos,
#         nodelist=edges,
#         node_color="gray",
#         node_size=300,
#         alpha=0.7
#     )
#
#     nx.draw_networkx_nodes(
#         planar_graph,
#         pos,
#         nodelist=vertices,
#         node_color="lightgreen",
#         node_size=300,
#         alpha=0.7
#     )
#
#     nx.draw_networkx_nodes(
#         planar_graph,
#         pos,
#         nodelist=crossings,
#         node_color="lightblue",
#         node_size=300,
#         alpha=0.7
#     )
#
#     # Label the nodes
#     nx.draw_networkx_labels(
#         planar_graph,
#         pos,
#         labels={n: n for n in regular_nodes},
#         font_size=10,
#     )
#
#     if highlight_nodes:
#         nx.draw_networkx_nodes(
#             planar_graph,
#             pos,
#             nodelist=highlight_nodes,
#             node_color="yellow",
#             node_size=2000,
#             label="Highlighted Nodes",
#             alpha=0.4,
#             edgecolors="orange"
#         )
#
#     # State all object-index assignments
#     intermediate_label_text = "Object-Index Pairs \n" + "\n".join(f"{label}" for node, label in node_labels.items())
#     plt.gcf().text(
#         0.85, 0.5,  # Position the text box to the right of the plot
#         intermediate_label_text,
#         fontsize=10,
#         va="center",
#         bbox=dict(boxstyle="round,pad=0.5", edgecolor="black", facecolor="white", alpha=0.9),
#     )
#
#     # Step 10: Remove axis and spines
#     plt.axis("off")  # Turn off axes, ticks, and labels
#     ax = plt.gca()  # Get the current axis
#     for spine in ax.spines.values():
#         spine.set_visible(False)  # Hide all spines
#
#     # Show the plot
#     plt.title("Planar Embedding of the Spatial Graph Diagram")
#     plt.show()