from collections import deque
import time
from .diagram_elements import Edge, Crossing, Vertex
from .spatial_graph_diagrams import SpatialGraphDiagram
from .Reidemeister import reidemeister_simplify
from .Anti_Reidemeister import apply_anti_reidemeister_move


def compute_min_distance(diagram1, diagram2, max_depth, max_runtime):
    start_time = time.time()
    queue1 = deque([(diagram1, 0)])
    queue2 = deque([(diagram2, 0)])
    visited1 = set()
    visited2 = set()
    polynomials1 = {diagram1.normalized_yamada_polynomial(): 0}
    polynomials2 = {diagram2.normalized_yamada_polynomial(): 0}

    if diagram1.normalized_yamada_polynomial() == diagram2.normalized_yamada_polynomial():
        return 0

    while queue1 and queue2:
        # Time and depth checks
        if time.time() - start_time > max_runtime:
            break

        # Expand from queue1
        current_diagram1, depth1 = queue1.popleft()
        if depth1 >= max_depth:
            continue
        for crossing in current_diagram1.crossings:
            new_diagram = apply_anti_reidemeister_move(current_diagram1, crossing.label)
            diag_hash = hash(new_diagram)
            if diag_hash not in visited1:
                visited1.add(diag_hash)
                yamada_poly = new_diagram.normalized_yamada_polynomial()
                polynomials1[yamada_poly] = depth1 + 1
                queue1.append((new_diagram, depth1 + 1))
                if yamada_poly in polynomials2:
                    return depth1 + 1 + polynomials2[yamada_poly]

        # Expand from queue2
        current_diagram2, depth2 = queue2.popleft()
        if depth2 >= max_depth:
            continue
        for crossing in current_diagram2.crossings:
            new_diagram = apply_anti_reidemeister_move(current_diagram2, crossing.label)
            diag_hash = hash(new_diagram)
            if diag_hash not in visited2:
                visited2.add(diag_hash)
                yamada_poly = new_diagram.normalized_yamada_polynomial()
                polynomials2[yamada_poly] = depth2 + 1
                queue2.append((new_diagram, depth2 + 1))
                if yamada_poly in polynomials1:
                    return depth2 + 1 + polynomials1[yamada_poly]

    return None  # No match found within constraints