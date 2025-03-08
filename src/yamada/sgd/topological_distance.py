from collections import deque, defaultdict
import time
from yamada.sgd.sgd_modification import apply_crossing_swap
from yamada.sgd.reidemeister import reidemeister_simplify


def expand_single_bfs(queue, polynomials, other_polynomials, network, max_depth):
    """
    Expand a single step in the BFS for the current diagram.

    Args:
        queue: The BFS queue for the current side.
        polynomials: The visited set for the current side.
        other_polynomials: The visited set for the opposite side.
        network: The topological network being constructed.
        max_depth: The maximum depth for BFS expansion.

    Returns:
        The distance if an early exit is found, or None if expansion continues.
    """
    current_diagram, depth = queue.popleft()
    if depth >= max_depth:
        return None

    # Expand neighbors
    yamada_poly_current = current_diagram.yamada_polynomial()
    for crossing in current_diagram.crossings:
        new_diagram = apply_crossing_swap(current_diagram, crossing.label)

        # Simplify the diagram
        new_diagram, _, _, _ = reidemeister_simplify(new_diagram)

        yamada_poly_new = new_diagram.yamada_polynomial()


        if yamada_poly_new not in polynomials:

            # Add to network
            network[yamada_poly_current].append(yamada_poly_new)

            # Update BFS structures
            polynomials[yamada_poly_new] = depth + 1
            queue.append((new_diagram, depth + 1))

            # Early exit if the polynomial matches one from the other BFS
            if yamada_poly_new in other_polynomials:
                return depth + 1 + other_polynomials[yamada_poly_new]

    return None


def compute_min_distance(diagram1, diagram2, max_depth=3, max_runtime=10):
    """
    Perform a bidirectional BFS to compute the minimum number of topological changes.
    """
    start_time = time.time()

    # Initialize BFS queues and visited sets
    queue1 = deque([(diagram1, 0)])
    queue2 = deque([(diagram2, 0)])
    polynomials1 = {diagram1.yamada_polynomial(): 0}
    polynomials2 = {diagram2.yamada_polynomial(): 0}
    network = defaultdict(list)

    # Quick check if diagrams already match
    if diagram1.yamada_polynomial() == diagram2.yamada_polynomial():
        return 0, network

    # BFS search loop with dynamic alternation
    while queue1 or queue2:

        # Time check
        if time.time() - start_time > max_runtime:
            raise TimeoutError("Time limit reached")

        # Expand one step from the first queue if available
        if queue1:
            result = expand_single_bfs(queue1, polynomials1, polynomials2, network, max_depth)
            if result is not None:
                return result, network

        # Expand one step from the second queue if available
        if queue2:
            result = expand_single_bfs(queue2, polynomials2, polynomials1, network, max_depth)
            if result is not None:
                return result, network

    # No match found
    return None, network



###

def bfs_expansion(diagram, max_depth=5, max_runtime=10):
    """
    Perform a full unidirectional BFS expansion from a single diagram.
    At each node, for every crossing in the diagram:
      1. Create a copy,
      2. Apply a crossing swap,
      3. Simplify the new diagram.
    The BFS recurses until max_depth is reached.

    Each node is stored as a dict with:
      - 'diagram': the resulting spatial graph diagram,
      - 'depth': the number of crossing swaps (BFS level),
      - 'parent': the parent node's ID (None for the root),
      - 'swap': the crossing label used to generate the node.

    Returns:
        nodes: dict mapping node_id -> node data.
        tree: dict mapping a parent node_id -> list of child node_ids.
    """
    start_time = time.time()
    nodes = {}  # node_id -> { 'diagram', 'depth', 'parent', 'swap' }
    tree = defaultdict(list)  # parent node_id -> list of child node_ids
    queue = deque()

    # Assign ID 0 to the root node.
    node_counter = 0
    root_id = node_counter
    nodes[root_id] = {'diagram': diagram, 'depth': 0, 'parent': None, 'swap': None}
    queue.append(root_id)
    node_counter += 1

    while queue:
        if time.time() - start_time > max_runtime:
            raise TimeoutError("Time limit reached")
        current_id = queue.popleft()
        current_node = nodes[current_id]
        current_depth = current_node['depth']
        if current_depth >= max_depth:
            continue

        current_diagram = current_node['diagram']
        # For every crossing, create a copy and perform a crossing swap.
        for crossing in current_diagram.crossings:
            new_diagram = apply_crossing_swap(current_diagram, crossing.label)
            # TODO Fix
            # new_diagram, _, _, _ = reidemeister_simplify(new_diagram)
            new_depth = current_depth + 1
            new_id = node_counter
            node_counter += 1
            nodes[new_id] = {
                'diagram': new_diagram,
                'depth': new_depth,
                'parent': current_id,
                'swap': crossing.label
            }
            tree[current_id].append(new_id)
            queue.append(new_id)
    return nodes, tree


def compute_network(diagrams, max_depth=3, max_runtime=10):
    """
    For a list of starting diagrams, run a full BFS expansion on each one
    (using bfs_expansion) and then compile the results into a single network.

    After all BFS trees are built, we compute the Yamada polynomial for every node.
    Then we collapse nodes that have identical Yamada polynomials by keeping,
    for each unique topology, the minimal BFS depth at which it was encountered.

    We also construct a network mapping from one unique topology to its neighbors,
    using the minimal distance (i.e. BFS depth) if an edge appears multiple times.

    Returns:
        combined_graph: A dict mapping each unique Yamada polynomial to a dict:
            {
              'min_depth': minimal number of crossing swaps to reach this topology,
              'neighbors': { neighbor_yamada_poly: min_edge_distance, ... }
            }
    """
    combined_nodes = {}  # Combined node_id -> node data
    combined_tree = defaultdict(list)  # Combined tree: parent_id -> list of child_ids
    id_offset = 0
    bfs_results = []  # List of (shifted_nodes, shifted_tree) for each starting diagram

    # Run a BFS for each starting diagram, shifting node IDs to avoid collisions.
    for diagram in diagrams:
        nodes, tree = bfs_expansion(diagram, max_depth, max_runtime)
        shifted_nodes = {}
        shifted_tree = defaultdict(list)
        for node_id, data in nodes.items():
            new_id = node_id + id_offset
            shifted_nodes[new_id] = data
        for parent, children in tree.items():
            parent_shifted = parent + id_offset
            shifted_tree[parent_shifted] = [child + id_offset for child in children]
        bfs_results.append((shifted_nodes, shifted_tree))
        id_offset += len(nodes)

    # Merge all nodes and trees.
    for nodes, tree in bfs_results:
        combined_nodes.update(nodes)
        for parent, children in tree.items():
            combined_tree[parent].extend(children)

    # Compute the Yamada polynomial for each node.
    node_poly = {}
    for node_id, data in combined_nodes.items():
        poly = data['diagram'].yamada_polynomial()
        node_poly[node_id] = poly

    # Build a mapping from each unique Yamada polynomial to its minimal depth.
    poly_min_depth = {}
    for node_id, data in combined_nodes.items():
        poly = node_poly[node_id]
        depth = data['depth']
        if poly in poly_min_depth:
            poly_min_depth[poly] = min(poly_min_depth[poly], depth)
        else:
            poly_min_depth[poly] = depth

    # Build the network: for each edge in the combined BFS tree,
    # map the parent's Yamada polynomial to the child's Yamada polynomial.
    # The edge weight is taken as the child's depth.
    combined_network = defaultdict(dict)
    for parent_id, children in combined_tree.items():
        parent_poly = node_poly[parent_id]
        for child_id in children:
            child_poly = node_poly[child_id]
            child_depth = combined_nodes[child_id]['depth']
            if child_poly in combined_network[parent_poly]:
                combined_network[parent_poly][child_poly] = min(
                    combined_network[parent_poly][child_poly], child_depth)
            else:
                combined_network[parent_poly][child_poly] = child_depth

    # Create the final combined graph structure.
    combined_graph = {}
    for poly, depth in poly_min_depth.items():
        combined_graph[poly] = {
            'min_depth': depth,
            'neighbors': combined_network.get(poly, {})
        }

    return combined_graph

