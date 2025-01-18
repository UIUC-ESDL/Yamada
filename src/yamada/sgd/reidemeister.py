from yamada.sgd.diagram_elements import Edge, Crossing
from yamada.sgd.sgd_analysis import face_has_exactly_3_crossings_and_3_edges, edges_that_are_fully_under_or_over, \
    edge_is_double_over_or_under, find_opposite_crossing, find_common_edge, get_index_of_crossing_corner, \
    edges_form_a_strand


# %% Reidemeister 1

def available_r1_moves(sgd):
    """
    Criteria:
    1. The diagram must have a crossing.
    2. Two adjacent corners of the crossing must share the same exact edge OR strand of edges.
       (i.e., the edge forms a loop and nothing is over-laying, under-laying, or poking through that loop).

    Note: Applying the R1 move monotonically simplifies the diagram. Further, since applying the R1 move will change
    the diagram, it might invalidate other identified R1 moves. Therefore, we will only provide the first identified R1.
    This function may be called multiple times to simplify the diagram.

    TODO Decouple SGD Object from Reidemeister Moves. Rely on static data structures.
    """


    r1_crossing_labels = []
    for crossing in sgd.crossings:
        (A, i), (B, j), (C, k), (D, l) = crossing.adjacent
        cond_1 = edges_form_a_strand(A, B)
        cond_2 = edges_form_a_strand(B, C)
        cond_3 = edges_form_a_strand(C, D)
        cond_4 = edges_form_a_strand(D, A)
        if cond_1 or cond_2 or cond_3 or cond_4:
            r1_crossing_labels.append(crossing.label)

    return r1_crossing_labels


def apply_r1_move(sgd, crossing_label, simplify=True):
    """
    1. Remove the crossing.
    2. Remove the edge that two adjacent crossing corners share.
    3. Connect the edges from the other two crossing corners.
    """

    # Make a copy of the sgd object to avoid modifying the original
    sgd = sgd.copy()

    # Find the crossing object given the label
    crossing = sgd.get_object(crossing_label)

    # Connect the opposing crossing corners and remove the crossing
    A, i = crossing.adjacent[0]
    B, j = crossing.adjacent[1]
    C, k = crossing.adjacent[2]
    D, l = crossing.adjacent[3]
    sgd.connect(A, i, C, k)
    sgd.connect(B, j, D, l)
    sgd._remove_crossing(crossing)

    # Simplify and Check the diagram
    if simplify:
        sgd.simplify_diagram()

    return sgd


# %% Reidemeister 2

def available_r2_moves(sgd):
    """
    Criteria:
    1. There must exist a pair of crossings that share two common edges.
       (again, the edges form uninterrupted arcs and nothing is over-laying, under-laying, or poking through them).
    2. One of these edges must pass over both crossings, and the other edge must pass under both crossings.

    Note: Applying the R2 move monotonically simplifies the diagram. Further, since applying the R2 move will change
    the diagram, it might invalidate other identified R1 moves. Therefore, we will only provide the first identified R2.
    This function may be called multiple times to simplify the diagram.

    TODO Decouple SGD Object from Reidemeister Moves. Rely on static data structures.
    """

    r2_crossing_labels = []

    for face in sgd.faces():
        crossings = [entrypoint.vertex for entrypoint in face if isinstance(entrypoint.vertex, Crossing)]
        edges = [entrypoint.vertex for entrypoint in face if isinstance(entrypoint.vertex, Edge)]

        if len(crossings) == 2 and len(edges) == 2:
            crossing1, crossing2 = crossings
            edge1, edge2 = edges
            if edge_is_double_over_or_under(edge1) and edge_is_double_over_or_under(edge2):
                r2_crossing_labels.append((crossing1.label, crossing2.label))

    return r2_crossing_labels


def apply_r2_move(sgd, crossing_labels, simplify=True):
    """
    0. Get the indices
    1. Remove the two crossings
    2. Connect edges on opposite sides of the crossings
    # 2. Remove the two common edges
    # 3. Connect the continuations of the common edges

    """

    # Make a copy of the sgd object to avoid modifying the original
    sgd = sgd.copy()

    # Get the inputs
    crossing_1_label, crossing_2_label = crossing_labels

    # Find the objects given the labels
    crossing_1 = sgd.get_object(crossing_1_label)
    crossing_2 = sgd.get_object(crossing_2_label)

    # Remove crossing 1
    c1_a0, c1_a0_i = crossing_1.adjacent[0]
    c1_a1, c1_a1_i = crossing_1.adjacent[1]
    c1_a2, c1_a2_i = crossing_1.adjacent[2]
    c1_a3, c1_a3_i = crossing_1.adjacent[3]
    sgd.connect(c1_a0, c1_a0_i, c1_a2, c1_a2_i)
    sgd.connect(c1_a1, c1_a1_i, c1_a3, c1_a3_i)
    sgd._remove_crossing(crossing_1)

    # Remove crossing 2
    c2_a0, c2_a0_i = crossing_2.adjacent[0]
    c2_a1, c2_a1_i = crossing_2.adjacent[1]
    c2_a2, c2_a2_i = crossing_2.adjacent[2]
    c2_a3, c2_a3_i = crossing_2.adjacent[3]
    sgd.connect(c2_a0, c2_a0_i, c2_a2, c2_a2_i)
    sgd.connect(c2_a1, c2_a1_i, c2_a3, c2_a3_i)
    sgd._remove_crossing(crossing_2)

    # Simplify and Check the diagram
    if simplify:
        sgd.simplify_diagram()

    return sgd


# %% Reidemeister 3

def available_r3_moves(sgd):
    """
    Criteria:
    1. The face must have exactly 3 crossings and 3 edges.
    2. At least one of the edges of the face must pass either fully under or fully over its two crossings.

    Note: A face can have more than one possible R3 move.

    Terminology:
    - stationary_crossing: The crossing that is not being moved by R3.
    - moving_edge: The edge that is moving across the stationary crossing
    - moving_crossings (1 & 2): The two crossings connected to the moving_edge and therefore move with it.
    - stationary_edges (1 & 2): The two edges that form the stationary_crossing.
    """

    # Initialize the lists
    r3_inputs = []

    # Criteria 1: There must be a face with exactly three crossings (i.e., no vertices).
    candidate_faces = []
    for face in sgd.faces():
        if face_has_exactly_3_crossings_and_3_edges(face):
            candidate_faces.append(face)

    # Criteria 2: At least one of the edges of the face must pass either fully under or fully over two crossings.
    for face in candidate_faces:
        candidate_edges = edges_that_are_fully_under_or_over(face)
        for candidate_edge in candidate_edges:
            r3_input = {}

            # In a triangular face (3 crossings, 3 edges), the stationary crossing is opposite of the moving edge.
            stationary_crossing = find_opposite_crossing(face, candidate_edge)

            face_entry_points = [ep.vertex for ep in face]

            # Determine the starting point (stationary crossing)
            start_index = face_entry_points.index(stationary_crossing)

            # Reorder the face to start from the stationary crossing
            ordered_face = face_entry_points[start_index:] + face_entry_points[:start_index]

            # Identify the two moving crossings (next clockwise crossings after the stationary crossing)
            moving_crossings = [ep for ep in ordered_face if isinstance(ep, Crossing) and ep != stationary_crossing]

            stationary_edge_1 = find_common_edge(stationary_crossing, moving_crossings[0])
            stationary_edge_2 = find_common_edge(stationary_crossing, moving_crossings[1])

            r3_input['stationary_crossing'] = stationary_crossing.label
            r3_input['stationary_edge_1'] = stationary_edge_1.label
            r3_input['stationary_edge_2'] = stationary_edge_2.label
            r3_input['moving_crossing_1'] = moving_crossings[0].label
            r3_input['moving_crossing_2'] = moving_crossings[1].label
            r3_input['moving_edge'] = candidate_edge.label
            r3_inputs.append(r3_input)

    return r3_inputs


def apply_r3_move(sgd, r3_input, simplify=True):
    """
    We apply the R3 move by:
    TBD...
    """

    # Make a copy of the sgd object to avoid modifying the original
    sgd = sgd.copy()

    # Unpack the inputs
    sc_label = r3_input['stationary_crossing']
    mc1_label = r3_input['moving_crossing_1']
    mc2_label = r3_input['moving_crossing_2']
    se1_label = r3_input['stationary_edge_1']
    se2_label = r3_input['stationary_edge_2']

    # Find the SGD objects given their labels
    sc = [crossing for crossing in sgd.crossings if crossing.label == sc_label][0]
    se1 = [edge for edge in sgd.edges if edge.label == se1_label][0]
    se2 = [edge for edge in sgd.edges if edge.label == se2_label][0]
    mc1 = [crossing for crossing in sgd.crossings if crossing.label == mc1_label][0]
    mc2 = [crossing for crossing in sgd.crossings if crossing.label == mc2_label][0]

    # Stationary crossing edge assignments
    index_sc_to_se1 = get_index_of_crossing_corner(sc, se1)
    index_sc_to_se2 = get_index_of_crossing_corner(sc, se2)
    index_sc_to_opposite_of_se1 = get_index_of_crossing_corner(sc, se1, opposite_side=True)
    index_sc_to_opposite_of_se2 = get_index_of_crossing_corner(sc, se2, opposite_side=True)

    # Moving crossing 1 edge assignments
    index_mc1_to_se1 = get_index_of_crossing_corner(mc1, se1)
    index_mc1_to_opposite_of_se1 = get_index_of_crossing_corner(mc1, se1, opposite_side=True)

    # Moving crossing 2 edge assignments
    index_mc2_to_se2 = get_index_of_crossing_corner(mc2, se2)
    index_mc2_to_opposite_of_se2 = get_index_of_crossing_corner(mc2, se2, opposite_side=True)

    # Find the objects adjacent to one crossing on the side opposing another crossing
    sc_adj_opposite_of_se1 = sc.adjacent[index_sc_to_opposite_of_se1][0]
    sc_adj_opposite_of_se2 = sc.adjacent[index_sc_to_opposite_of_se2][0]
    mc1_adj_opposite_of_se1 = mc1.adjacent[index_mc1_to_opposite_of_se1][0]
    mc2_adj_opposite_of_se2 = mc2.adjacent[index_mc2_to_opposite_of_se2][0]

    # Also find their relevant indices
    index_sc_adj_opposite_of_se1_to_sc = get_index_of_crossing_corner(sc_adj_opposite_of_se1, sc)
    index_sc_adj_opposite_of_se2_to_sc = get_index_of_crossing_corner(sc_adj_opposite_of_se2, sc)
    index_mc1_adj_opposite_of_se1_to_mc1 = get_index_of_crossing_corner(mc1_adj_opposite_of_se1, mc1)
    index_mc2_adj_opposite_of_se2_to_mc2 = get_index_of_crossing_corner(mc2_adj_opposite_of_se2, mc2)

    se1_mc1_index = [i for (edge, i) in mc1.adjacent if edge == se1][0]
    se1_sc_index = [i for (edge, i) in sc.adjacent if edge == se1][0]
    se2_mc2_index = [i for (edge, i) in mc2.adjacent if edge == se2][0]
    se2_sc_index = [i for (edge, i) in sc.adjacent if edge == se2][0]

    # Update the stationary crossing connections
    sgd.connect(sc, index_sc_to_se1, mc1_adj_opposite_of_se1, index_mc1_adj_opposite_of_se1_to_mc1)
    sgd.connect(sc, index_sc_to_se2, mc2_adj_opposite_of_se2, index_mc2_adj_opposite_of_se2_to_mc2)
    sgd.connect(sc, index_sc_to_opposite_of_se1, se2, se2_sc_index)
    sgd.connect(sc, index_sc_to_opposite_of_se2, se1, se1_sc_index)

    # Update the moving-crossing-1 connections
    sgd.connect(mc1, index_mc1_to_opposite_of_se1, se1, se1_mc1_index)
    sgd.connect(mc1, index_mc1_to_se1, sc_adj_opposite_of_se2, index_sc_adj_opposite_of_se2_to_sc)

    # Update the moving-crossing-2 connections
    sgd.connect(mc2, index_mc2_to_opposite_of_se2, se2, se2_mc2_index)
    sgd.connect(mc2, index_mc2_to_se2, sc_adj_opposite_of_se1, index_sc_adj_opposite_of_se1_to_sc)

    # Check the diagram
    if simplify:
        sgd.simplify_diagram()

    return sgd


# %% Reidemeister 4


# NOT IMPLEMENTED


# %% Reidemeister 5


# NOT IMPLEMENTED


# %% Reidemeister 6


# NOT FULLY IMPLEMENTED


def has_r6(sgd):
    for V in sgd.vertices:
        for i in range(V.degree):
            E, e = V.adjacent[i]
            A, a = E.flow(e)
            if isinstance(A, Crossing):
                E, e = V.adjacent[(i + 1) % V.degree]
                B, b = E.flow(e)
                if A == B and (b + 1) % 4 == a:
                    return True
    return False


# %% Reidemeister Simplification


def r1_and_r2_simplify(sgd):
    max_iter = 1000
    i = 0
    r1_count = 0
    r2_count = 0
    sgd_has_r1 = True
    sgd_has_r2 = True
    while sgd_has_r1 and sgd_has_r2:

        r1_crossing_labels = available_r1_moves(sgd)
        if len(r1_crossing_labels) > 0:
            sgd = apply_r1_move(sgd, r1_crossing_labels[0])
            r1_count += 1
        else:
            sgd_has_r1 = False

        r2_crossing_labels = available_r2_moves(sgd)
        if len(r2_crossing_labels) > 0:
            sgd = apply_r2_move(sgd, r2_crossing_labels[0])
            r2_count += 1
        else:
            sgd_has_r2 = False

        if i > max_iter:
            raise ValueError(f"R1 and R2 simplification has been looping for {i} times. This is likely an error.")

        i += 1

    return sgd, r1_count, r2_count


def reidemeister_simplify(sgd, n_tries=10):

    # Make a copy of the sgd object
    sgd = sgd.copy()

    # Initialize the counts
    total_r1_count = 0
    total_r2_count = 0
    total_r3_count = 0

    # Check for any initial moves that will monotonically simplify the diagram
    sgd, r1_count, r2_count = r1_and_r2_simplify(sgd)
    total_r1_count += r1_count
    total_r2_count += r2_count

    # Perform Reidemeister 3 moves to see if they set up any R1 or R2 moves
    for i in range(n_tries):
        r3_inputs = available_r3_moves(sgd)
        if len(r3_inputs) > 0:
            # Pick a semi-random R3 move
            r3_input = r3_inputs[i % len(r3_inputs)]
            sgd = apply_r3_move(sgd, r3_input)
            total_r3_count += 1

            # Check for any R1 or R2 moves that will monotonically simplify the diagram
            sgd, r1_count, r2_count = r1_and_r2_simplify(sgd)
            total_r1_count += r1_count
            total_r2_count += r2_count
        else:
            break

    return sgd, total_r1_count, total_r2_count, total_r3_count
