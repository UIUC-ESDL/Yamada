"""
Enumerating spatial graph diagrams
==================================

Current code is limited to trivalent system architectures.

The basic approach differs somewhat from the one in the paper.
Namely, I use "plantri" to enumerate possible diagram shadows with the
specified number of crossings::

  http://users.cecs.anu.edu.au/~bdm/plantri/

You need to compile plantri and have it in the same directory as this
file (or somewhere in your path) for the enumeration to work.

Due to a limitation of plantri, this restricts us to shadows which are
"diagrammatically prime" in that there is not a circle meeting the
shadow in two points that has vertices of the shadow on both sides.
Equivalently, the dual planar graph is simple.

If the system architecture graph cannot be disconnected by removing
two edges, this only excludes shadows all of whose spatial diagrams
are the connect sum of a spatial graph diagram with the desired system
architecture and a knot.  Presumably, we would want to exclude such in
any event.  However, the example in Case Study 1 can be so
disconnected...

Validation
==========

Compared to Dobrynin and Vesnin:

1. For the theta graph, the list of Yamada polynomials through 5
   crossings matches after removing the non-prime examples from their
   list (theta_3, theta_5, theta_10, theta_14).

2. For the tetrahedral graph, the list of Yamada polynomials through 4
   crossings matches after removing the non-prime Omega_5.

Note: The way this script is written w/ pickling you must import this script into another script
rather than directly calculate Yamada polynomials in this script (you'll get error messages)

"""

import networkx as nx
import pickle
from cypari import pari
import matplotlib
matplotlib.use('TkAgg')   # Use a non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

from yamada.poly.H_polynomial import h_poly
from yamada.poly.utilities import get_coefficients_and_exponents, normalize_poly
from yamada.sgd.diagram_elements import Vertex, Edge, Crossing


class SpatialGraphDiagram:
    """
    TODO: Fix labels. Normalize them, and make sure they are unique (both currently, and going forward)
    """

    def __init__(self, *, edges=None, vertices=None, crossings=None, check=True):

        # Ensure inputs are lists (avoid mutable default arguments)
        edges = edges or []
        vertices = vertices or []
        crossings = crossings or []

        # Combine all elements into a single list
        data = edges + vertices + crossings

        # Ensure labels are unique by creating a dictionary
        self.data = {d.label: d for d in data}

        # Validate label uniqueness
        if len(data) != len(self.data):
            raise ValueError("Labels must be unique across all diagram elements.")

        # Categorize elements by type
        self.edges = [d for d in data if isinstance(d, Edge)]
        self.vertices = [d for d in data if isinstance(d, Vertex)]
        self.crossings = [d for d in data if isinstance(d, Crossing)]

        # Optional: Validate categorization
        if len(self.edges) != len(edges):
            raise ValueError("Some edges are incorrectly classified.")
        if len(self.vertices) != len(vertices):
            raise ValueError("Some vertices are incorrectly classified.")
        if len(self.crossings) != len(crossings):
            raise ValueError("Some crossings are incorrectly classified.")

        # Normalize labels
        self._normalize_labels()

        # TODO Update to make sure each object is connected by edges... preprocess
        if len(self.edges) == 0 and len(data) > 0:
            self._inflate_edges()
        # self._inflate_edges()

        # Optionally run additional checks
        if check:
            self._check()

    def _normalize_labels(self):
        """
        Renumbers labels for edges, vertices, and crossings sequentially.
        """
        # Renumber edges
        for i, edge in enumerate(self.edges, start=1):
            old_label = edge.label
            new_label = f"e{i}"
            edge.label = new_label
            self.data.pop(old_label)
            self.data[new_label] = edge

        # Renumber vertices
        for i, vertex in enumerate(self.vertices, start=1):
            old_label = vertex.label
            new_label = f"v{i}"
            vertex.label = new_label
            self.data.pop(old_label)
            self.data[new_label] = vertex

        # Renumber crossings
        for i, crossing in enumerate(self.crossings, start=1):
            old_label = crossing.label
            new_label = f"c{i}"
            crossing.label = new_label
            self.data.pop(old_label)
            self.data[new_label] = crossing

        # Update counters
        self.edge_counter = len(self.edges)
        self.vertex_counter = len(self.vertices)
        self.crossing_counter = len(self.crossings)

    def faces(self):
        """
        The faces are the complementary regions of the diagram. Each
        face is given as a list of corners of BaseVertices as one goes
        around *clockwise*. These corners are recorded as
        EntryPoints, where EntryPoints(c, j) denotes the corner of the
        face abutting crossing c between strand j and j + 1.

        Alternatively, the sequence of EntryPoints can be regarded as
        the *heads* of the oriented edges of the face.
        """

        entry_points = []

        for V in self.data.values():
            entry_points += V.entry_points()

        corners = set(entry_points)
        faces = []

        while len(corners):
            face = [corners.pop()]
            while True:
                next_ep = face[-1].next_corner()
                if next_ep == face[0]:
                    faces.append(face)
                    break
                else:
                    corners.remove(next_ep)
                    face.append(next_ep)

        return faces

    def euler(self):
        """
        Returns the Euler characteristic of the diagram.
        """
        v = len(self.crossings) + len(self.vertices)
        e = len(self.edges)
        f = len(self.faces())
        return v - e + f

    def is_planar(self):
        """
        Returns True if the diagram is planar.
        """
        return self.euler() == 2 * len(list(nx.connected_components(self.projection_graph())))


    def _check(self):
        """
        Checks that the diagram is valid.
        """

        assert 2 * len(self.edges) == sum(d.degree for d in self.crossings + self.vertices)

        for C in self.crossings:
            assert all(isinstance(v, Edge) for v, j in C.adjacent)
        for V in self.vertices:
            assert all(isinstance(v, Edge) for v, j in V.adjacent)
        for E in self.edges:
            assert all(not isinstance(v, Edge) for v, j in E.adjacent)
        assert self.is_planar()


    def _create_edge(self, A, i, B, j):
        """Creates and adds an edge to the diagram."""

        # Create a new edge
        self.edge_counter += 1
        edge_label = f'e{self.edge_counter}'
        edge = Edge(edge_label)

        # Add the edge to the diagram
        self._add_edge(edge)

        # Connect the edge to the diagram elements
        self.connect(A, i, edge, 0)
        self.connect(B, j, edge, 1)

    def _create_vertex(self, *args):
        """Creates and adds an n-valent vertex to the diagram. Each argument is a tuple (A,i), (B, j), etc."""

        # Create a new vertex
        self.vertex_counter += 1
        vertex_label = f'v{self.vertex_counter}'
        vertex = Vertex(len(args), vertex_label)

        # Add the vertex to the diagram
        self._add_vertex(vertex)

        # Connect the vertex to the diagram elements
        for i, (obj, idx) in enumerate(args):
            self.connect(obj, idx, vertex, i)

    def _create_crossing(self, A, i, B, j, C, k, D, l):
        """Creates and adds a crossing to the diagram."""

        # Create a new crossing
        self.crossing_counter += 1
        crossing_label = f'c{self.crossing_counter}'
        crossing = Crossing(crossing_label)

        # Add the crossing to the diagram
        self._add_crossing(crossing)

        # Connect the crossing to the diagram elements
        self.connect(A, i, crossing, 0)
        self.connect(B, j, crossing, 1)
        self.connect(C, k, crossing, 2)
        self.connect(D, l, crossing, 3)

    def _add_edge(self, edge):
        """Adds an edge to the diagram."""
        self.edges.append(edge)
        self.data[edge.label] = edge

    def _add_vertex(self, vertex):
        """Adds a vertex to the diagram."""
        self.vertices.append(vertex)
        self.data[vertex.label] = vertex

    def _add_crossing(self, crossing):
        """Adds a crossing to the diagram."""
        self.crossings.append(crossing)
        self.data[crossing.label] = crossing

    def _remove_edge(self, edge):
        """Removes an edge from the diagram."""
        self.edges.remove(edge)
        self.data.pop(edge.label)

    def _remove_vertex(self, vertex):
        """Removes a vertex from the diagram."""
        self.vertices.remove(vertex)
        self.data.pop(vertex.label)

    def _remove_crossing(self, crossing):
        """Removes a crossing from the diagram."""
        self.crossings.remove(crossing)
        self.data.pop(crossing.label)

    def _inflate_edges(self):
        """
        Creates and inserts an edge for each pair of crossings and/or vertices.
        """

        curr_index = 0
        edges = []

        for A in self.crossings + self.vertices:
            for i in range(A.degree):
                B, j = A.adjacent[i]
                if not isinstance(B, Edge):
                    E = Edge(curr_index)
                    curr_index += 1
                    edges.append(E)
                    self.data[E.label] = E
                    E[0] = (A, i)
                    E[1] = (B, j)

        self.edges = edges

    def _merge_edges(self, E0, E1):
        """
        Merges two edges into a single edge. Keeps the label with the lowest value.
        """

        if E0.label < E1.label:
            keep_edge = E0
            remove_edge = E1
        elif E0.label > E1.label:
            keep_edge = E1
            remove_edge = E0
        else:
            raise ValueError('Edges must have distinct labels.')

    def get_object(self, label):
        return self.data[label]

    def connect(self, A, i, B, j):

        A_is_edge = isinstance(A, Edge)
        B_is_edge = isinstance(B, Edge)

        # If both diagram elements are edges, then connect them with a vertex.
        if A_is_edge and B_is_edge:
            self._create_vertex((A, i), (B, j))

        # If only one diagram element is an edge, then connect them directly.
        elif (A_is_edge and not B_is_edge) or (not A_is_edge and B_is_edge):
            A[i] = B[j]

        # If neither diagram element is an edge, then connect them with an edge.
        else:
            self._create_edge(A, i, B, j)


    def short_cut(self, crossing, i0):
        """
        Short-cuts a crossing by removing the edge between them.
        """

        i1 = (i0 + 1) % 4
        E0, j0 = crossing.adjacent[i0]
        E1, j1 = crossing.adjacent[i1]
        if E0 == E1:
            self._create_vertex((E0, j0), (E1, j1))
        else:
            self.connect(E0, j0, E1, j1)


    def copy(self):
        """
        Returns a serialized copy of the diagram.
        """
        return pickle.loads(pickle.dumps(self))

    def projection_graph(self):
        """
        TODO Add documentation
        """

        G = nx.MultiGraph()

        for e in self.edges:
            v = e.adjacent[0][0].label
            w = e.adjacent[1][0].label
            G.add_edge(v, w)
        return G

    def underlying_graph(self):
        """
        TODO Add documentation
        """

        G = nx.MultiGraph()
        vertex_inputs = set()

        for V in self.vertices:
            vertex_inputs.update((V, i) for i in range(V.degree))

        edges_used = 0

        while len(vertex_inputs):
            V, i = vertex_inputs.pop()
            W, j = V.adjacent[i]
            while not isinstance(W, Vertex):
                if isinstance(W, Edge):
                    edges_used += 1
                W, j = W.flow(j)
            vertex_inputs.remove((W, j))
            v, w = V.label, W.label
            G.add_edge(v, w)

        if edges_used == len(self.edges):
            return G

    def underlying_planar_embedding(self):
        """
        Returns the underlying planar embedding of an abstract graph.
        """

        G = nx.PlanarEmbedding()
        parts = self.vertices + self.crossings + self.edges

        for A in parts:
            for i in range(A.degree):
                B, j = A.adjacent[i]
                ref_nbr = None if i == 0 else A.adjacent[i - 1][0].label
                G.add_half_edge_ccw(A.label, B.label, ref_nbr)

        G.check_structure()
        return G

    # def underlying_planar_embedding(self):
    #     """
    #     Returns the underlying planar embedding of an abstract graph.
    #     """
    #
    #     G = nx.PlanarEmbedding()
    #     parts = self.vertices + self.crossings
    #
    #     for A in parts:
    #         for i in range(A.degree):
    #             B, j = A.adjacent[i]
    #             ref_nbr = None if i == 0 else A.adjacent[i - 1][0].label
    #             G.add_half_edge_ccw(A.label, B.label, ref_nbr)
    #
    #             ref_nbr_reverse = None if j == 0 else B.adjacent[j - 1][0].label
    #             G.add_half_edge_ccw(B.label, A.label, ref_nbr_reverse)
    #
    #     G.check_structure()
    #     return G


    def calculate_yamada_polynomial(self, check_pieces=False):

        A = pari('A')

        if len(self.crossings) == 0:
            return h_poly(self.projection_graph())

        C = self.crossings[0]
        c = C.label

        # S_plus
        S_plus = self.copy()
        C_plus = S_plus.data[c]
        S_plus._remove_crossing(C_plus)
        S_plus.short_cut(C_plus, 0)
        S_plus.short_cut(C_plus, 2)
        if check_pieces:
            S_plus._check()

        # S_minus
        S_minus = self.copy()
        C_minus = S_minus.data[c]
        S_minus._remove_crossing(C_minus)
        S_minus.short_cut(C_minus, 1)
        S_minus.short_cut(C_minus, 3)
        if check_pieces:
            S_minus._check()

        # S_0
        S_0 = self.copy()
        C_0 = S_0.data[c]
        S_0._remove_crossing(C_0)

        V = Vertex(4, repr(C_0) + '_smushed')
        S_0._add_vertex(V)

        # (A, i), (B, j), (C, k), (D, l) = C_0.adjacent
        # S_0._create_vertex((A, i), (B, j), (C, k), (D, l))

        # for i, (B, j) in enumerate(C_0.adjacent):
        #     V[i] = B[j]

        for i in range(4):
            B, j = C_0.adjacent[i]
            V[i] = B[j]

        if check_pieces:
            S_0._check()

        Y_plus  = S_plus.calculate_yamada_polynomial()
        Y_minus = S_minus.calculate_yamada_polynomial()
        Y_0     = S_0.calculate_yamada_polynomial()
        Y_new   = A * Y_plus + (A ** -1) * Y_minus + Y_0

        return Y_new

    def yamada_polynomial(self, normalize=True):
        """normalized_yamada_polynomial"""

        yamada_polynomial = self.calculate_yamada_polynomial()

        if normalize:
            yamada_polynomial =  normalize_poly(yamada_polynomial)

        return yamada_polynomial

    def plot(self):

        G = self.underlying_planar_embedding()
        layout = nx.planar_layout(G)


        # Draw the base graph
        plt.figure(figsize=(12, 10))
        nx.draw(
            G,
            layout,
            with_labels=True,
            node_color="lightblue",
            edge_color="gray",
            node_size=3000,
            font_size=10,
        )

        # Add assignment labels at connections
        for edge in self.edges:
            # Each edge has two connections (start and end)
            for idx, (connected_obj, jdx) in enumerate(edge.adjacent):
                # Calculate label position
                edge_pos = layout[edge.label]
                obj_pos = layout[connected_obj.label]
                label_pos = (
                    (edge_pos[0] + obj_pos[0]) / 2,
                    (edge_pos[1] + obj_pos[1]) / 2,
                )

                # Create assignment label
                assignment_label = f"{edge.label}[{idx}]={connected_obj.label}[{jdx}]"

                # Annotate the graph
                plt.text(
                    label_pos[0],
                    label_pos[1],
                    assignment_label,
                    fontsize=8,
                    color="red",
                    ha="center",
                )

        # Final adjustments
        plt.title("Spatial Graph Diagram with Assignments")
        plt.axis("off")
        plt.show()


