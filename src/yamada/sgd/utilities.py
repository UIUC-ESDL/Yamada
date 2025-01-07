def split_edge(edge):
    """
    Splits an edge with more than two nodes into a series of edges which each have two nodes.
    """

    edges = []
    for i in range(len(edge)-1):
        edges.append((edge[i], edge[i+1]))
    return edges


def split_edges(edges):
    """
    Splits a list of edges with more than two nodes into a series of edges which each have two nodes.
    """

    # Strip crossings from edges
    edges_without_crossings = []
    for edge in edges:
        edge_without_crossings = [node for node in edge if "C" not in node]
        edges_without_crossings.append(edge_without_crossings)

    new_edges = []
    for edge in edges_without_crossings:
        new_edges.extend(split_edge(edge))
    return new_edges


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


def apply_crossing_swap(sgd, crossing_label):

    sgd = sgd.copy()

    X = sgd.get_object(crossing_label)

    (A, i), (B, j), (C, k), (D, l) = X.adjacent

    # Swap the under-crossing strand and over-crossing strand
    X[0] = D[l]
    X[1] = A[i]
    X[2] = B[j]
    X[3] = C[k]

    return sgd
