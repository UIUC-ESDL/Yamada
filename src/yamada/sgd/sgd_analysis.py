from yamada import Edge, Crossing, Vertex


def face_has_exactly_3_crossings_and_3_edges(face):
    edges = [entrypoint.vertex for entrypoint in face if isinstance(entrypoint.vertex, Edge)]
    crossings = [entrypoint.vertex for entrypoint in face if isinstance(entrypoint.vertex, Crossing)]
    vertices = [entrypoint.vertex for entrypoint in face if isinstance(entrypoint.vertex, Vertex)]

    has_3_edges = len(edges) == 3
    has_3_crossings = len(crossings) == 3
    has_no_vertices = len(vertices) == 0
    has_exactly_3_crossings_and_3_edges = has_3_edges and has_3_crossings and has_no_vertices
    return has_exactly_3_crossings_and_3_edges


def edges_that_are_fully_under_or_over(face):
    edges = [entrypoint.vertex for entrypoint in face if isinstance(entrypoint.vertex, Edge)]
    candidate_edges = []
    for edge in edges:
        if edge_is_double_over_or_under(edge):
            candidate_edges.append(edge)
    return candidate_edges


def edge_is_double_over_or_under(edge):
    edge_adjacent_1 = edge.adjacent[0][0]
    edge_adjacent_2 = edge.adjacent[1][0]

    if not isinstance(edge_adjacent_1, Crossing) or not isinstance(edge_adjacent_2, Crossing):
        return False

    crossing_1 = edge_adjacent_1
    crossing_2 = edge_adjacent_2

    edge_over_crossing_1 = edge_is_over(edge, crossing_1)
    edge_over_crossing_2 = edge_is_over(edge, crossing_2)

    # Double over
    if edge_over_crossing_1 and edge_over_crossing_2:
        return True

    # Double under
    elif not edge_over_crossing_1 and not edge_over_crossing_2:
        return True

    # One over, one under
    else:
        return False


def edge_is_over(edge, crossing):
    """
    Crossing indices 1 and 3 indicate the over edge. Indices 0 and 2 indicate the under edge.
    If an edge is not over, then it must be under. Therefore, we only check for
    one of these two conditions.
    """
    if crossing.adjacent[1][0] == edge or crossing.adjacent[3][0] == edge:
        return True
    else:
        return False


def find_opposite_crossing(face, edge):
    for entrypoint in face:
        if isinstance(entrypoint.vertex, Crossing):
            edge_adjacent = [adjacent[0] for adjacent in edge.adjacent]
            if entrypoint.vertex not in edge_adjacent:
                return entrypoint.vertex


def find_common_edge(crossing1, crossing2):
    for adjacent1 in crossing1.adjacent:
        for adjacent2 in crossing2.adjacent:
            if adjacent1[0] == adjacent2[0]:
                return adjacent1[0]
    raise Exception('Common edge not found in crossings')


def get_index_of_crossing_corner(crossing, corner, opposite_side=False):
    for i in range(4):
        if crossing.adjacent[i][0] == corner:
            if not opposite_side:
                return i
            else:
                return (i + 2) % 4
    raise Exception('Corner not found in crossing')


def edges_form_a_strand_along_a_direction(e1, e2, direction_index):

    # TODO Ensure that both edges are Edge objects

    # Initialize the current object and the index of the next object
    current_object = e1
    index_of_next_object = direction_index

    # Loop through the strand until the second edge is reached or the strand ends
    strand = [current_object.label]
    max_iter = 1000
    for i in range(max_iter):

        # If the current object is the second edge, then the edges form a strand
        if current_object == e2:
            return True, strand

        # Identify the next object and the index it assigns to the current object
        next_object, next_object_index = current_object.adjacent[index_of_next_object]
        strand.append(next_object.label)

        # If the next object is the second edge, then the edges form a strand
        if next_object == e2:
            return True, strand

        # If the next object is not the second edge and is also not 2-valent,
        # then the strand ends and the edges do not form a strand.
        elif next_object.degree != 2:
            return False, strand

        # If not the next object is admissible, then continue moving along the strand
        else:
            # Set the next object as the current object
            current_object = next_object

            # Set the index of the next object
            # Since this is a 2-valent vertex, the index of the next object is the opposite of the current index
            index_of_next_object = (next_object_index + 1) % 2

    return False, strand


def edges_form_a_strand(e1, e2):
    """
    Check whether two edges are form part, or a whole, of a strand.
    A strand is a series of edges and 2-valent vertices that are connected in a line.
    """

    # Check if the edges form a strand in either direction
    cond_1, strand_dir1 = edges_form_a_strand_along_a_direction(e1, e2, 0)
    cond_2, strand_dir2 = edges_form_a_strand_along_a_direction(e1, e2, 1)
    does_form_strand = cond_1 or cond_2
    strands_checked = [strand_dir1, strand_dir2]  # For Debugging
    return does_form_strand


def available_crossing_swaps(sgd):
    crossing_labels = [c.label for c in sgd.crossings]
    return crossing_labels
