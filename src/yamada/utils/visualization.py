
# Standard library imports
import numpy as np
import matplotlib.pyplot as plt
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

def plot_spatial_graph_diagram(sgd, label_map=None, color_map=None, off_screen=False):
    """
    Plots the spatial graph diagram in 3D using PyVista.
    Labels intermediate edges with index numbers and intermediate nodes with full index assignments.
    """

    # Initialize the PyVista plotter
    plotter = pv.Plotter(window_size=[1000, 750], off_screen=off_screen)
    plotter.camera.SetClippingRange(1e-6, 1e6)
    plotter.view_isometric()

    # Get node positions
    nodes, node_positions, edges = position_spatial_graph_in_3d(sgd)

    node_sizes  = {}
    node_colors = {}
    node_types  = {}
    for node in sgd.data.values():
        node_label = node.label
        if node in sgd.vertices:
            node_sizes[node_label]  = 7
            node_colors[node_label] = "blue"
            node_types[node_label]  = "Vertex"
        elif node in sgd.crossings:
            node_sizes[node_label + "+"]  = 7
            node_sizes[node_label + "-"]  = 7
            # node_colors[node_label + "+"] = "lightgreen"
            # node_colors[node_label + "-"] = "lightgreen"
            node_colors[node_label + "+"] = "gray"
            node_colors[node_label + "-"] = "gray"
            node_types[node_label + "+"]  = "Crossing"
            node_types[node_label + "-"]  = "Crossing"
        elif node in sgd.edges:
            node_sizes[node_label]  = 1
            node_colors[node_label] = "black"
            node_types[node_label]  = "Edge"
        else:
            raise ValueError("Unknown node type")

        if color_map is not None and node_label in color_map:
            cur_color = node_colors[node_label]
            node_colors[node_label] = color_map.get(node_label, cur_color)


    # Plot nodes as spheres
    for node, coords in zip(nodes, node_positions):

        size  = node_sizes[node]
        color = node_colors[node]

        sphere = pv.Sphere(radius=size, center=coords)
        plotter.add_mesh(sphere, color=color, edge_color="black",opacity=1.0, label=str(node))

    # Plot edges as tubes
    pos_dict = dict(zip(nodes, node_positions))

    for edge in edges:
        line = pv.Line(pos_dict[edge[0]], pos_dict[edge[-1]])
        plotter.add_mesh(line.tube(radius=1.0), color="black", line_width=6)

    # Add node labels
    LABEL_OFFSET = np.array([1.3, 1.3, 1.3])
    for node, coords in zip(nodes, node_positions):

        if node_types[node] == "Edge":
            continue  # Skip labeling edges here

        label     = node
        label_pos = coords + LABEL_OFFSET

        if label_map is not None:
            label = label_map.get(label, label)

        plotter.add_point_labels(
            [label_pos],
            [label],
            point_size=22,
            font_size=24,
            bold=True,
            text_color="black",
            # shape_color="white",
            # shape_opacity=0.5,
            background_color=None,
            background_opacity=0.0,
            always_visible=True,
            shape=None,
        )

    return plotter

def draw_spatial_graph_2d(plotter, nodes_2d, edges_2d, pos_2d, ccw_orderings, ccw_angles, show_index_labels):

    # Reset the color cycle for 2D edges
    color_list = list(mcolors.TABLEAU_COLORS.keys())
    color_cycle = itertools.cycle(color_list)

    res=6

    for node in nodes_2d:
        positions = np.array([pos_2d[node]])
        positions = np.array([[positions[0][0], 0, positions[0][1]]])
        sphere = pv.Sphere(radius=0.01, phi_resolution=res, theta_resolution=res)
        glyphs = pv.PolyData(positions).glyph(orient=False, scale=False, geom=sphere)
        plotter.add_mesh(glyphs, color="black", opacity=1.0)

    for edge in edges_2d:
        start_node, end_node, _ = edge
        start_position = pos_2d[start_node]
        end_position = pos_2d[end_node]
        # Insert y=0 for 2D projection
        start_position = np.array([start_position[0], 0, start_position[1]])
        end_position   = np.array([end_position[0], 0, end_position[1]])
        color_i = next(color_cycle)
        line = pv.Line(start_position, end_position)
        plotter.add_mesh(line, color=color_i, line_width=5)

    # Add node labels, placing each index number according to its angle
    # node_labels          = [f"{node}" for node in nodes_2d]
    # node_label_positions = np.array([[pos_2d[node][0], 0, pos_2d[node][1]] for node in nodes_2d])
    # plotter.add_point_labels(node_label_positions, node_labels, point_size=0, font_size=12, text_color='black')
    node_labels = [f"{node}".replace("crossing_", "X") for node in nodes_2d]
    node_label_positions = np.array([[pos_2d[node][0], 0, pos_2d[node][1]] for node in nodes_2d])
    plotter.add_point_labels(node_label_positions, node_labels,
                             point_size=0,
                             font_size=62,
                             text_color='black',background_color=None,shape=None,
            background_opacity=0.0, always_visible=True)


    # Add neighbor index labels
    if show_index_labels:

        # Draw zero-angles as a glyph
        a0 = np.array([0, 0, 0])
        b0 = np.array([0.1, 0, 0])
        offsets = [np.array([pos_2d[node][0], 0, pos_2d[node][1]]) for node in nodes_2d]
        points = []
        endpoints = []
        lines = []
        for i, offset in enumerate(offsets):
            a = a0 + offset
            b = b0 + offset

            idx0 = len(points)
            idx1 = idx0 + 1
            points.append(a)
            points.append(b)
            endpoints.append(b)
            lines.extend([2, idx0, idx1])

        # Draw a faint gray line at each node to indicate the zero-degree angle
        polyLines = pv.PolyData(np.array(points), lines=np.array(lines))
        polyEndpoints = pv.PolyData(np.array(endpoints))
        sphere = pv.Sphere(radius=0.005, phi_resolution=8, theta_resolution=8)
        sphereGlyph = polyEndpoints.glyph(orient=False, scale=False, geom=sphere)
        plotter.add_mesh(polyLines, color="gray", line_width=2, opacity=0.5)
        plotter.add_mesh(sphereGlyph, color="gray", opacity=0.5)

        node_labels = []
        node_positions = []
        for node in nodes_2d:
            for nbr in list(ccw_orderings[node].keys()):
                angle   = ccw_angles[node][nbr]
                radius  = 0.1
                label_x = pos_2d[node][0] + radius * np.cos(angle)
                label_y = 0
                label_z = pos_2d[node][1] + radius * np.sin(angle)

                node_labels.append(f"{ccw_orderings[node][nbr]}")
                node_positions.append([label_x, label_y, label_z])

        # plotter.add_point_labels(node_positions, node_labels,
        #                    font_size=12, text_color='black', show_points=False,background_color=None, background_opacity=0)
        plotter.add_point_labels(node_positions, node_labels,
                                 font_size=42,
                                 text_color='black',
                                 show_points=False,
                                 background_color=None,
                                 background_opacity=0,
                                 shape=None)

    # Configure the plot
    plotter.view_xz()
    # plotter.show_axes()


def draw_spatial_graph_3d(plotter, nodes_3d, edges_3d, pos_3d,
                          projection_plane_normal):

    # Define a list of colors to cycle through
    color_list = list(mcolors.TABLEAU_COLORS.keys())
    color_cycle = itertools.cycle(color_list)

    # Create a PyVista plotter
    plotter.view_isometric()

    # Plot the projection plane
    center = np.mean(np.array(list(pos_3d.values())), axis=0)
    projected_plane = pv.Plane(center=center, direction=projection_plane_normal,
                               i_size=2, j_size=2)
    plotter.add_mesh(projected_plane, color='lightgray', opacity=0.1)

    # Create glyphs for nodes
    nodes_nodes     = [node for node in nodes_3d if 'crossing' not in node]
    nodes_crossings = [node for node in nodes_3d if 'crossing' in node]
    color_node = "black"
    size_node  = 0.01
    color_crossing = "red"
    size_crossing  = 0.02
    res=6

    if nodes_nodes:
        nodeVertex = pv.Sphere(radius=size_node, phi_resolution=res, theta_resolution=res)
        nodeVertexGlyphs = pv.PolyData(np.array([pos_3d[n] for n in nodes_nodes])).glyph(orient=False, scale=False,
                                                                                         geom=nodeVertex)
        plotter.add_mesh(nodeVertexGlyphs, color=color_node, opacity=1.0)

    if nodes_crossings:
        nodeCrossing = pv.Sphere(radius=size_crossing, phi_resolution=res, theta_resolution=res)
        nodeCrossingGlyphs = pv.PolyData(np.array([pos_3d[n] for n in nodes_crossings])).glyph(orient=False, scale=False, geom=nodeCrossing)
        plotter.add_mesh(nodeCrossingGlyphs, color=color_crossing, opacity=1.0)


    for edge in edges_3d:
        start_node, end_node, _ = edge
        start_position       = pos_3d[start_node]
        end_position         = pos_3d[end_node]
        color_i              = next(color_cycle)
        line                 = pv.Line(start_position, end_position)
        plotter.add_mesh(line, color=color_i, line_width=5)

    # Add node labels
    node_labels          = [f"{node}" for node in nodes_3d]
    node_label_positions = np.array([pos_3d[node] for node in nodes_3d])
    plotter.add_point_labels(node_label_positions, node_labels , point_size=0, font_size=42, text_color='black', always_visible=True,background_color=None, shape=None,
            background_opacity=0.0,)



    # Configure the plot
    plotter.show_axes()



def plot_projection():
    pass




def add_labels(p, nodes_2d, pos_2d, ccw_orderings, ccw_angles):
    # Collect all node label positions and texts
    node_label_points = []
    node_label_texts  = []

    # Collect all neighbor-index label positions and texts
    angle_label_points = []
    angle_label_texts  = []

    for node in nodes_2d:
        # ----- Node label (name) -----
        position = pos_2d[node]  # (x, z) in your convention
        x, z = position
        node_label_points.append([x, 0.0, z])
        node_label_texts.append(f"{node}")

        # ----- Optional: zero-angle guide line + marker -----
        zero_angle_rad = np.radians(0.0)  # or just 0.0
        zero_x = x + 0.1 * np.cos(zero_angle_rad)
        zero_z = z + 0.1 * np.sin(zero_angle_rad)
        p.add_mesh(
            pv.Line((x, 0.0, z), (zero_x, 0.0, zero_z)),
            line_width=2, opacity=0.5
        )
        p.add_mesh(
            pv.Sphere(radius=0.002, center=(zero_x, 0.0, zero_z)),
            opacity=0.5
        )

        # ----- Neighbor index labels -----
        if node not in ccw_orderings:
            continue

        nbrs = list(ccw_orderings[node].keys())
        for nbr in nbrs:
            angle = ccw_angles[node][nbr]  # assuming degrees; if radians, drop np.radians
            # radius = 0.05
            radius = 0.3
            angle_rad = np.radians(angle)

            label_x = x + radius * np.cos(angle_rad)
            label_y = 0.0
            label_z = z + radius * np.sin(angle_rad)

            angle_label_points.append([label_x, label_y, label_z])
            angle_label_texts.append(f"{ccw_orderings[node][nbr]}")

    # ----- Batch-add node labels -----
    if node_label_points:
        node_label_points = np.asarray(node_label_points)
        p.add_point_labels(
            node_label_points,
            node_label_texts,
            point_size=0,
            font_size=42,
            text_color="black",
            show_points=False,
            background_color=None,
            background_opacity=0.0,
            shape = None,
        )

    # ----- Batch-add neighbor index labels -----
    if angle_label_points:
        angle_label_points = np.asarray(angle_label_points)
        p.add_point_labels(
            angle_label_points,
            angle_label_texts,
            point_size=0,
            font_size=24,
            text_color="black",
            show_points=False,
            background_color=None,
            background_opacity=0.0,
            shape=None,
        )

    return p

def draw_sgd(G, pos, ccw_orderings, ccw_angles, save_filepath=None):

    fig, ax = plt.subplots(figsize=(10, 10))

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color='lightblue', ax=ax)
    # Draw edges
    nx.draw_networkx_edges(G, pos, width=2, edge_color='gray', ax=ax)
    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=36, font_color='black', ax=ax)

    # Add a faint gray line to indicate the zero-degree angle for each node
    for node in G.nodes():
        angle_rad = 0  # 0 degrees in radians
        radius = 0.2  # Length of the guide line
        start_x = pos[node][0]
        start_y = pos[node][1]
        end_x = start_x + radius * np.cos(angle_rad)
        end_y = start_y + radius * np.sin(angle_rad)
        ax.plot([start_x, end_x], [start_y, end_y], color='gray', linewidth=1, linestyle='--', alpha=0.5)
        ax.plot(end_x, end_y, marker='o', color='gray', markersize=5, alpha=0.5)

    # Add neighbor index labels
    for node in G.nodes():
        nbrs = list(ccw_orderings[node].keys())
        for nbr in nbrs:
            angle = ccw_angles[node][nbr]
            # radius = 0.05  # Distance from the node position to place the label
            radius = 0.3
            angle_rad = angle
            label_x = pos[node][0] + radius * np.cos(angle_rad)
            label_y = pos[node][1] + radius * np.sin(angle_rad)
            ax.text(label_x, label_y, f"{ccw_orderings[node][nbr]}", fontsize=10, color='darkgreen')

    if save_filepath is None:
        plt.show(block=True)
    else:
        plt.savefig(save_filepath, dpi=300)
        plt.close()


