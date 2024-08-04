import itertools
import random
import networkx as nx
import pyvista as pv
from networkx.algorithms.approximation import traveling_salesman_problem

# Set the random seed for reproducibility
random.seed(0)

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

def manhattan_distance(u, v):
    return sum(abs(a - b) for a, b in zip(u, v))


def calculate_reference_paths(grid, cube_edges):
    reference_paths = {}
    for start, end in cube_edges:
        reference_path = nx.astar_path(grid, start, end, heuristic=manhattan_distance)
        reference_paths[(start, end)] = reference_path
    return reference_paths



def create_cube_paths(grid, corners, reference_paths, k, l):

    # TODO: Remove all edges from an intermediate node, and start/end nodes should not be in middle of list...

    edge_paths = []

    for (start, end), reference_path in reference_paths.items():

        # Create a copy of the grid
        grid_copy = grid.copy()

        # # Remove any waypoint nodes
        # for _, path in edge_paths:
        #     if len(path) > 2:
        #         for node in path[1:-1]:
        #             grid_copy.remove_node(node)

        # Remove the cube corners from the grid, except for the start and end nodes
        for node in corners:
            if node not in [start, end]:
                grid_copy.remove_node(node)

        # For a path with k waypoints, create k + 1 sub-paths
        n_subpaths = k + 1
        subpaths = []

        # Identify waypoints within l distance of at least one node in the reference path
        candidate_waypoints = [node for node in grid_copy.nodes if any(manhattan_distance(node, ref) <= l for ref in reference_path)]

        # Candidates should not be the start or end nodes
        candidate_waypoints = [node for node in candidate_waypoints if node not in corners]

        # Randomly select k waypoints from the candidate waypoints
        waypoints = random.sample(candidate_waypoints, k)

        # # Sort the waypoints by their distance to the start node
        # waypoints.sort(key=lambda node: manhattan_distance(node, start))

        # Create the sub-paths
        for i in range(n_subpaths):
            grid_copy_copy = grid_copy.copy()
            if i == 0:
                grid_copy_copy.remove_node(end)
                reserved_waypoints = waypoints[1:]
                grid_copy_copy.remove_nodes_from(reserved_waypoints)
                subpath = nx.astar_path(grid_copy_copy, start, waypoints[0], heuristic=manhattan_distance)
            elif i == n_subpaths - 1:
                grid_copy_copy.remove_node(start)
                reserved_waypoints = waypoints[:-1]
                grid_copy_copy.remove_nodes_from(reserved_waypoints)
                subpath = nx.astar_path(grid_copy_copy, waypoints[-1], end, heuristic=manhattan_distance)
            else:
                grid_copy_copy.remove_node(start)
                grid_copy_copy.remove_node(end)
                reserved_waypoints = waypoints[:i] + waypoints[i + 1:]
                grid_copy_copy.remove_nodes_from(reserved_waypoints)
                subpath = nx.astar_path(grid_copy_copy, waypoints[i - 1], waypoints[i], heuristic=manhattan_distance)

            subpaths += subpath

            # Remove the sub-path from the grid
            for j in range(len(subpath) - 1):
                grid_copy.remove_edge(subpath[j], subpath[j + 1])

        # Remove repeated nodes from the sub-paths
        path = [subpaths[0]]
        for node in subpaths[1:]:
            if node != path[-1]:
                path.append(node)

        edge_paths.append(((start, end), path))

    return edge_paths


def draw_graph(cube_corners, edge_paths):
    plotter = pv.Plotter()

    # Define a list of distinct colors
    color_palette = [
        "red", "green", "blue", "yellow", "purple", "cyan", "magenta", "orange", "lime", "pink", "teal", "brown"
    ]

    # Draw cube nodes larger
    for node in cube_corners:
        plotter.add_mesh(pv.Sphere(center=node, radius=0.2), color='red')  # Increase the radius

    # # Draw reference paths in wireframe
    # for ref_path, _ in edge_paths:
    #     points = []
    #     for node in ref_path:
    #         points.append(node)
    #     line = pv.lines_from_points(points)
    #     plotter.add_mesh(line, color='gray', line_width=2, style='wireframe')

    # Draw actual paths with different colors
    for path_idx, (_, path) in enumerate(edge_paths):
        color = color_palette[path_idx % len(color_palette)]
        points = []
        for node in path:
            points.append(node)
        line = pv.lines_from_points(points)
        plotter.add_mesh(line, color=color, line_width=4)

    plotter.show()

# Example usage
n = 8  # Size of the grid
m = 5  # Size of the cube
k = 1  # Number of waypoints
l = 2  # Minimum distance from the original path nodes

grid = create_grid_graph(n)
cube_corners = select_cube_corners(n, m)

cube_edges = [
    (cube_corners[0], cube_corners[1]), (cube_corners[0], cube_corners[2]), (cube_corners[0], cube_corners[4]),
    (cube_corners[1], cube_corners[3]), (cube_corners[1], cube_corners[5]), (cube_corners[2], cube_corners[3]),
    (cube_corners[2], cube_corners[6]), (cube_corners[3], cube_corners[7]), (cube_corners[4], cube_corners[5]),
    (cube_corners[4], cube_corners[6]), (cube_corners[5], cube_corners[7]), (cube_corners[6], cube_corners[7])
]

# Calculate reference paths
reference_paths = calculate_reference_paths(grid, cube_edges)

# Create paths with waypoints
edge_paths = create_cube_paths(grid, cube_corners, reference_paths, k, l)

# Draw the graph with waypoints
draw_graph(cube_corners, edge_paths)

# Define nodes, edges, and node positions of the cube nodes and paths
node_labels = {tuple(node): idx for idx, node in enumerate(set(itertools.chain(*[path for _, path in edge_paths])))}
nodes = list(node_labels.values())
edges = [(node_labels[tuple(path[i])], node_labels[tuple(path[i + 1])]) for _, path in edge_paths for i in range(len(path) - 1)]
node_positions = {idx: node for node, idx in node_labels.items()}


print("Nodes:", nodes)
print("Edges:", edges)
print("Node positions:", node_positions)


#
# from yamada import SpatialGraph
# from yamada.Reidemeister import *
#
# # Instantiate the SpatialGraph object
# sg = SpatialGraph(nodes=nodes,
#                   node_positions=node_positions,
#                   edges=edges)
#
# # # Plot the Spatial Graph in 3D and the projected 2D plane to see what's going on. Crossings will be circled in red.
# # # Note: Crossings occur when two edges that do not intersect, but appear to when they are projected onto a 2D plane.
# # # sg.plot()
#
# # Create the spatial graph diagram (necessary for calculating the Yamada polynomial)
# sgd = sg.create_spatial_graph_diagram()
#
# sgd, r1_count, r2_count, r3_count = reidemeister_simplify(sgd, n_tries=10)
#
# print(f"R1: {r1_count}, R2: {r2_count}, R3: {r3_count}, Remaining Crossings: {len(sgd.crossings)}")
# # # yp = sgd.normalized_yamada_polynomial()
# # # print(yp)




