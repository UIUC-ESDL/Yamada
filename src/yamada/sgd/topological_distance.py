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


# def unidirectional_bfs(diagram, max_depth=3, max_runtime=10):
#     """
#     Perform a uni-directional BFS starting from a single diagram.
#     Uses the provided expand_single_bfs function to expand the BFS.
#
#     Args:
#         diagram: The starting diagram.
#         max_depth: Maximum BFS depth.
#         max_runtime: Maximum allowed runtime in seconds.
#
#     Returns:
#         visited: A dict mapping each discovered Yamada polynomial to its BFS distance.
#         network: A defaultdict(list) where keys are source Yamada polynomials and
#                  values are lists of target Yamada polynomials reached by one crossing swap.
#     """
#     start_time = time.time()
#     queue = deque([(diagram, 0)])
#     visited = {diagram.yamada_polynomial(): 0}
#     network = defaultdict(list)
#     # For uni-directional BFS, we pass a persistent empty dictionary to avoid triggering early exit.
#     dummy_other_polynomials = {}
#
#     while queue:
#         if time.time() - start_time > max_runtime:
#             raise TimeoutError("Time limit reached")
#         # Expand one node using your provided expand_single_bfs.
#         # We ignore the return value since the early exit (which is meant for bidirectional searches)
#         # should never fire with an empty dummy dictionary.
#         expand_single_bfs(queue, visited, dummy_other_polynomials, network, max_depth)
#
#     return visited, network
#
#
# def compute_network(diagrams, max_depth=4, max_runtime=10):
#     """
#     For a list of diagrams, perform a BFS search on each one (using unidirectional_bfs),
#     and then combine the results. In the combined network, if two BFS searches both identify
#     a relationship (i.e. an edge from one Yamada polynomial to another), the minimal distance
#     between them (as given by the BFS 'visited' dictionaries) is used.
#
#     Returns:
#         combined_visited: A dict mapping each discovered Yamada polynomial to the minimum BFS distance
#                           from any starting diagram.
#         combined_network: A dict mapping a source Yamada polynomial to a dict whose keys are target
#                           Yamada polynomials and values are the minimal number of crossing swaps (distance)
#                           required to reach that topology.
#     """
#     combined_visited = {}  # Mapping polynomial -> minimal distance (from any BFS)
#     combined_network = defaultdict(dict)  # Mapping: source poly -> {target poly: min distance}
#
#     # Run each BFS in parallel.
#     with ThreadPoolExecutor() as executor:
#         futures = {executor.submit(unidirectional_bfs, diagram, max_depth, max_runtime): diagram
#                    for diagram in diagrams}
#         for future in as_completed(futures):
#             try:
#                 visited, network = future.result()
#             except Exception as e:
#                 print(f"BFS search failed for one diagram: {e}")
#                 continue
#
#             # Combine the visited dictionaries: for each discovered polynomial,
#             # keep the minimum distance (i.e. the fewer crossing swaps needed).
#             for poly, d in visited.items():
#                 if poly in combined_visited:
#                     combined_visited[poly] = min(combined_visited[poly], d)
#                 else:
#                     combined_visited[poly] = d
#
#             # Combine the network edges.
#             # The network from unidirectional_bfs is a defaultdict(list) mapping a source polynomial
#             # to a list of neighbor polynomials. The "distance" to a neighbor is given by visited[neighbor]
#             # (which, by construction, equals visited[source] + 1).
#             for src, neighbor_list in network.items():
#                 for tgt in neighbor_list:
#                     # Use the BFS's visited dictionary to get the distance to the neighbor.
#                     if tgt in visited:
#                         edge_distance = visited[tgt]
#                         if tgt in combined_network[src]:
#                             combined_network[src][tgt] = min(combined_network[src][tgt], edge_distance)
#                         else:
#                             combined_network[src][tgt] = edge_distance
#     return combined_visited, combined_network


def bfs(queue, polynomials, network, max_depth):
    """
    Expand a single step in the BFS for the current diagram.

    Args:
        queue: The BFS queue for the current side.
        polynomials: The visited set for the current side.
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


    return network


def compute_network(diagram, max_depth=5, max_runtime=10):
    """
    Perform a unidirectional BFS starting from a single diagram.
    Returns the visited dictionary (mapping Yamada polynomials to BFS depths)
    and the network (mapping each polynomial to a list of neighbor polynomials).
    """
    start_time = time.time()

    # Initialize BFS queues and visited sets
    queue = deque([(diagram, 0)])
    polynomials = {diagram.yamada_polynomial(): 0}
    network = defaultdict(list)

    # BFS search loop with dynamic alternation
    while queue:

        # Time check
        if time.time() - start_time > max_runtime:
            raise TimeoutError("Time limit reached")

        # Expand one step from the first queue if available
        if queue:
            result = expand_single_bfs(queue, polynomials, network, max_depth)
            if result is not None:
                return result, network


    # No match found
    return None, network
