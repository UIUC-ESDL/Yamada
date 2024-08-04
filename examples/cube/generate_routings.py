import itertools
import networkx as nx
import matplotlib.pyplot as plt


def create_grid_graph(size):
    # Create a 3D grid graph with the specified size
    return nx.grid_graph(dim=[size, size, size])


def select_cube_corners(n, m):
    # Select 8 cube corners centered within the grid
    offset = (n - m) // 2
    corners = [
        (offset, offset, offset),
        (offset, offset, offset + m - 1),
        (offset, offset + m - 1, offset),
        (offset, offset + m - 1, offset + m - 1),
        (offset + m - 1, offset, offset),
        (offset + m - 1, offset, offset + m - 1),
        (offset + m - 1, offset + m - 1, offset),
        (offset + m - 1, offset + m - 1, offset + m - 1)
    ]
    return corners


def create_cube_paths(grid, corners, complexity_cutoff):
    # Create paths corresponding to cube edges without reusing edges or intermediate nodes
    edge_paths = []
    used_nodes = set(corners)  # Start with the corners being used
    cube_edges = [
        (corners[0], corners[1]), (corners[0], corners[2]), (corners[0], corners[4]),
        (corners[1], corners[3]), (corners[1], corners[5]), (corners[2], corners[3]),
        (corners[2], corners[6]), (corners[3], corners[7]), (corners[4], corners[5]),
        (corners[4], corners[6]), (corners[5], corners[7]), (corners[6], corners[7])
    ]

    for start, end in cube_edges:
        try:
            paths = list(nx.all_simple_paths(grid, source=start, target=end, cutoff=complexity_cutoff))
            if not paths:
                raise nx.NetworkXNoPath("No path found within the complexity cutoff.")
            # Select the path closest to the cutoff and not reusing intermediate nodes
            best_path = None
            for path in paths:
                if all(node in corners or node not in used_nodes for node in path):
                    if best_path is None or len(path) > len(best_path):
                        best_path = path
            if best_path is None:
                raise nx.NetworkXNoPath("No valid path found without reusing nodes.")
            edge_paths.append(best_path)
            used_nodes.update(node for node in best_path if node not in corners)
            # Remove used edges from the grid
            for i in range(len(best_path) - 1):
                grid.remove_edge(best_path[i], best_path[i + 1])
        except nx.NetworkXNoPath:
            raise nx.NetworkXNoPath(f"No path found from {start} to {end} within the complexity cutoff.")

    return edge_paths


def draw_graph(cube_corners, edge_paths):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Draw straight cube edges
    for start, end in cube_edges:
        x = [start[0], end[0]]
        y = [start[1], end[1]]
        z = [start[2], end[2]]
        ax.plot(x, y, z, 'r--', alpha=0.5)

    # Draw cube nodes
    for node in cube_corners:
        ax.scatter(*node, color='red', s=100)

    # Draw waypoint nodes and complex edges
    for path in edge_paths:
        x, y, z = zip(*path)
        ax.plot(x, y, z, 'b')
        for node in path:
            if node not in cube_corners:
                ax.scatter(*node, color='blue', s=50)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


# Example usage
n = 10  # Size of the grid
m = 4  # Size of the cube
# complexity_cutoff = 5
complexity_cutoff = 4

grid = create_grid_graph(n)
cube_corners = select_cube_corners(n, m)
cube_edges = [
    (cube_corners[0], cube_corners[1]), (cube_corners[0], cube_corners[2]), (cube_corners[0], cube_corners[4]),
    (cube_corners[1], cube_corners[3]), (cube_corners[1], cube_corners[5]), (cube_corners[2], cube_corners[3]),
    (cube_corners[2], cube_corners[6]), (cube_corners[3], cube_corners[7]), (cube_corners[4], cube_corners[5]),
    (cube_corners[4], cube_corners[6]), (cube_corners[5], cube_corners[7]), (cube_corners[6], cube_corners[7])
]

# Create paths with waypoints
edge_paths = create_cube_paths(grid, cube_corners, complexity_cutoff)

# Draw the graph with waypoints
draw_graph(cube_corners, edge_paths)

# Define nodes, edges, and node positions of the cube nodes and paths
node_labels = {node: str(idx) for idx, node in enumerate(set(itertools.chain(*edge_paths)))}
nodes = list(node_labels.values())
edges = [(node_labels[path[i]], node_labels[path[i + 1]]) for path in edge_paths for i in range(len(path) - 1)]
node_positions = {idx: node for node, idx in node_labels.items()}

print("Nodes:", nodes)
print("Edges:", edges)
print("Node positions:", node_positions)


from yamada import SpatialGraph

# Instantiate the SpatialGraph object
sg = SpatialGraph(nodes=nodes,
                  node_positions=node_positions,
                  edges=edges)

# Plot the Spatial Graph in 3D and the projected 2D plane to see what's going on. Crossings will be circled in red.
# Note: Crossings occur when two edges that do not intersect, but appear to when they are projected onto a 2D plane.
# sg.plot()

# Create the spatial graph diagram (necessary for calculating the Yamada polynomial)
sgd = sg.create_spatial_graph_diagram()

# # Calculate the Yamada polynomial
# # We use the normalized version because it is more useful for comparing polynomials
yamada_polynomial = sgd.normalized_yamada_polynomial()
print("Yamada Polynomial: ", yamada_polynomial)



