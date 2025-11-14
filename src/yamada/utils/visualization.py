
# Standard library imports
import numpy as np
import matplotlib.colors as mcolors
import networkx as nx
import pyvista as pv
import itertools
from networkx.algorithms.planar_drawing import triangulate_embedding


# Local imports
from ..sgd.sgd_modification import split_edges


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


        
def position_spatial_graph_in_3d(G, z_height=20):

    def normalize_label(node):
        """Normalizes the label of a node."""
        label = node.label
        return repr(label) if not isinstance(label, str) else label

    def get_end_label(edge, i):
        """Returns the label of an edge's endpoint, adjusted for crossings."""
        i = i % 2
        node, x = edge.adjacent[i]
        label = normalize_label(node)
        if node in G.crossings:
            label += '-' if x % 2 == 0 else '+'
        return label

    def position_nodes(planar_pos):
        """
        Position vertices and crossings in 3D.
        Returns dictionaries for system node positions and other node positions.
        """
        system_node_positions = {}
        other_node_positions = {}

        # Position vertices (z = 0)
        for vertex in G.vertices:
            label = normalize_label(vertex)
            x, y = planar_pos[vertex.label]
            system_node_positions[label] = (x, y, 0)

        # Position crossings (z = ±z_height)
        for crossing in G.crossings:
            label = normalize_label(crossing)
            x, y = planar_pos[crossing.label]
            other_node_positions[f"{label}+"] = (x, y, z_height)
            other_node_positions[f"{label}-"] = (x, y, -z_height)

        return system_node_positions, other_node_positions

    # def position_edges(planar_pos, node_positions):
    #     """
    #     Position edges in 3D based on the midpoint of their endpoints.
    #     Updates the other node positions dictionary.
    #     """
    #     edge_positions = {}
    #
    #     for edge in G.edges:
    #         label = normalize_label(edge)
    #         x, y = planar_pos[edge.label]
    #         start_label = get_end_label(edge, 0)
    #         end_label = get_end_label(edge, 1)
    #         z = (node_positions[start_label][2] + node_positions[end_label][2]) // 2
    #         edge_positions[label] = (x, y, z)
    #
    #     return edge_positions

    P = G.planar_embedding()
    planar_pos = tutte_embedding_positions(P)

    system_node_pos, other_node_pos = position_nodes(planar_pos)
    nodes_so_far = system_node_pos.copy()
    nodes_so_far.update(other_node_pos)

    # edge_positions = position_edges(planar_pos, {**system_node_pos, **other_node_pos})

    for E in G.edges:
        L = normalize_label(E)
        x, y = planar_pos[E.label]
        A = get_end_label(E, 0)
        B = get_end_label(E, 1)
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
                L = normalize_label(W)
                A = get_end_label(W, j)
                B = get_end_label(W, j + 1)
                one_seg += [A, L]
            W, j = W.flow(j)
        one_seg.append(normalize_label(W))
        vertex_inputs.remove((W, j))
        segments.append(one_seg)

    ###

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

    # node_positions_arr = np.array(node_positions)
    # node_positions_dict = dict(zip(nodes, node_positions_arr))


    return nodes, node_positions, segments

def plot_spatial_graph_diagram(sgd):
    """
    Plots the spatial graph diagram in 3D using PyVista.
    Labels intermediate edges with index numbers and intermediate nodes with full index assignments.
    """
    # , planar_graph, node_labels, edge_labels
    # # Check for planarity
    # is_planar, embedding = nx.check_planarity(planar_graph)
    # if not is_planar:
    #     raise ValueError("The graph is not planar!")

    # Generate 2D positions for the planar embedding
    # pos = nx.planar_layout(embedding)
    nodes, node_positions, edges = position_spatial_graph_in_3d(sgd)

    # Extend positions to 3D by adding a z-coordinate (all zero for planar layout)
    # pos_3d = {node: np.array([x, y, 0]) for node, (x, y) in pos.items()}

    # Create a PyVista plotter
    plotter = pv.Plotter()

    # Plot nodes as spheres
    for node, coords in zip(nodes, node_positions):
        sphere = pv.Sphere(radius=0.5, center=coords)
        plotter.add_mesh(sphere, color="black", opacity=0.8, label=str(node))

    # Plot edges as tubes
    pos_dict = dict(zip(nodes, node_positions))
    for edge in edges:

        # line = pv.Line(pos_dict[edge[0]], pos_dict[edge[-1]])
        # plotter.add_mesh(line.tube(radius=0.1), color="black", label=str(edge))

        line = pv.Line(pos_dict[edge[0]], pos_dict[edge[-1]])
        plotter.add_mesh(line.tube(radius=0.5), color="black", label=str(edge), line_width=6)

    # Add node labels
    for node, coords in zip(nodes, node_positions):
        label = node
        plotter.add_point_labels(
            [coords],
            [label],
            point_size=10,
            font_size=12,
            bold=True,
            text_color="black",
        )

    # # Add nodes as spheres
    # for node, coords in pos_3d.items():
    #
    #     if planar_graph.nodes[node]["type"] == "Edge":
    #         color = "black"
    #         opacity = 0.8
    #         sphere = pv.Sphere(radius=0.01, center=coords)
    #     elif planar_graph.nodes[node]["type"] == "Intermediate":
    #         color = "black"
    #         opacity = 0.8
    #         sphere = pv.Sphere(radius=0.01, center=coords)
    #     elif planar_graph.nodes[node]["type"] == "Vertex":
    #         color = "lightblue"
    #         opacity = 0.8
    #         sphere = pv.Sphere(radius=0.05, center=coords)
    #     elif planar_graph.nodes[node]["type"] == "Crossing":
    #         color = "green"
    #         opacity = 0.8
    #         sphere = pv.Sphere(radius=0.05, center=coords)
    #     else:
    #         raise ValueError("Unknown node type!")
    #         # color = "orange"
    #         # opacity = 0.5
    #         # sphere = pv.Sphere(radius=0.075, center=coords)
    #
    #     plotter.add_mesh(sphere, color=color, opacity=opacity, label=str(node))
    #
    # # Add edges as tubes
    # for edge, edge_label in zip(planar_graph.edges, edge_labels.values()):
    #     start, end = edge
    #     line = pv.Line(pos_3d[start], pos_3d[end])
    #     plotter.add_mesh(line.tube(radius=0.01), color="black", label=str(edge_label))
    #
    # # Add node labels
    # for node, coords in pos_3d.items():
    #     label = node_labels.get(node, str(node))
    #     plotter.add_point_labels(
    #         [coords],
    #         [label],
    #         point_size=10,
    #         font_size=12,
    #         bold=True,
    #         text_color="black",
    #     )
    #
    # # Add edge labels
    # for edge, edge_label in zip(planar_graph.edges, edge_labels.values()):
    #     midpoint = (pos_3d[edge[0]] + pos_3d[edge[1]]) / 2
    #     plotter.add_point_labels(
    #         [midpoint],
    #         [str(edge_label)],
    #         point_size=10,
    #         font_size=10,
    #         bold=False,
    #         text_color="blue",
    #     )
    #
    # # State all object-index assignments
    # intermediate_label_text = "Object-Index Pairs \n" + "\n".join(f"{label}" for node, label in node_labels.items())
    # text_coords = [0.8, 0.2, 0.0]  # Position the text box in normalized coordinates
    # plotter.add_text(
    #     intermediate_label_text,
    #     position="upper_right",
    #     font_size=10,
    #     color="black",
    #     viewport=True
    # )
    #
    # # Finalize the plot
    # plotter.add_axes()
    # plotter.add_legend()
    # plotter.show(title="Spatial Graph Diagram")
    return plotter


def plot_spatial_graph(nodes, edges, pos, pos2D, node_ordering_dict, node_angle_dict, sg):

    # Define a list of colors to cycle through
    color_list = list(mcolors.TABLEAU_COLORS.keys())
    color_cycle = itertools.cycle(color_list)

    # plotter = pv.Plotter()
    p = pv.Plotter(shape=(1, 2), window_size=[2000, 1000])

    p.view_xz()

    # Plot the 3D Spatial Graph in the first subplot
    p.subplot(0, 0)
    p.add_title("3D Spatial Graph")

    # Create glyphs for nodes
    nodes_nodes     = [node for node in nodes if 'crossing' not in node]
    nodes_crossings = [node for node in nodes if 'crossing' in node]
    color_node = "black"
    size_node  = 0.01
    color_crossing = "red"
    size_crossing  = 0.02
    res=12
    for node, color, size in [(nodes_nodes, color_node, size_node), (nodes_crossings, color_crossing, size_crossing)]:
        positions = np.array([pos[n] for n in node])
        sphere = pv.Sphere(radius=size, phi_resolution=res, theta_resolution=res)
        glyphs = pv.PolyData(positions).glyph(orient=False, scale=False, geom=sphere)
        p.add_mesh(glyphs, color=color, opacity=1.0)


    for edge in edges:
        start_node, end_node = edge
        start_position = pos[start_node]
        end_position = pos[end_node]
        color_i = next(color_cycle)
        line = pv.Line(start_position, end_position)
        p.add_mesh(line, color=color_i, line_width=5)

    # Configure the plot
    p.show_axes()

    # Reset the color cycle for 2D edges
    color_cycle = itertools.cycle(color_list)

    # Plot the 2D Projection in the second subplot
    p.subplot(0, 1)
    p.add_title("2D Projection")


    for edge in edges:
        start_node, end_node = edge
        start_position = pos[start_node]
        end_position = pos[end_node]
        color_i = next(color_cycle)
        line = pv.Line((start_position[0], 0, start_position[2]), (end_position[0], 0, end_position[2]))
        p.add_mesh(line, color=color_i, line_width=5)

    # Add node labels, placing each index number according to its angle
    for node in nodes:
        if "crossing" in node:
            begin, middle, end = node.split('_')
            node = begin + '_' + middle
            position = sg.crossings[node]["pos_2D"]
        else:
            position = pos2D[node]

        # p.add_point_labels(np.array([[position[0], 0, position[2]]]), f"{node}", point_size=0, font_size=12, text_color='black')
        pos_arr = np.array([[position[0], 0, position[1]]])
        p.add_point_labels(pos_arr, [f"{node}"], point_size=0, font_size=12, text_color='black')

        # Draw a faint gray line to indicate the zero-degree angle
        zero_angle_rad = np.radians(0)
        zero_x = position[0] + 0.1 * np.cos(zero_angle_rad)
        zero_z = position[1] + 0.1 * np.sin(zero_angle_rad)
        p.add_mesh(pv.Line((position[0], 0, position[1]), (zero_x, 0, zero_z)), color='gray', line_width=2, opacity=0.5)
        p.add_mesh(pv.Sphere(radius=0.002, center=(zero_x, 0, zero_z)), color='gray', opacity=0.5)

        nbrs = list(node_ordering_dict[node].keys())
        for nbr in nbrs:
            angle = node_angle_dict[node][nbr]
            radius = 0.05  # Distance from the node position to place the label
            angle_rad = np.radians(angle)
            label_x = position[0] + radius * np.cos(angle_rad)
            label_y = 0  # Since it's a 2D projection on the xz
            label_z = position[1] + radius * np.sin(angle_rad)
            p.add_point_labels((label_x, label_y, label_z), [f"{node_ordering_dict[node][nbr]}"],
                               font_size=12, text_color='black',show_points=False,background_color=None, background_opacity=0)


    # Configure the plot
    # p.view_xz()
    p.show_axes()

    # Link the two plots
    p.link_views()

    return p
