class EntryPoint:
    def __init__(self, vertex_like, index):
        self.vertex = vertex_like
        self.index = index

    def __eq__(self, other):
        return self.vertex == other.vertex and self.index == other.index

    def __hash__(self):
        return hash((self.vertex, self.index))

    def __repr__(self):
        return "<EP %s %d>" % (self.vertex, self.index)

    def next_corner(self):
        """
        Moves around face clockwise.
        """
        V, i = self.vertex, self.index
        j = (i + 1) % V.degree
        W, k = V.adjacent[j]
        return EntryPoint(W, k)


class BaseVertex:
    """
    A flat vertex has n inputs, labeled 0, 1, ..., n-1 in
    anticlockwise order.

    The adjacents should be edges, not other flat vertices.
    """

    def __init__(self, degree, label):
        self.label = label
        self.degree = degree
        self.adjacent = degree * [None]

    def __getitem__(self, i):
        return self, i % self.degree

    def __setitem__(self, i, other):
        o, j = other
        i = i % self.degree
        self.adjacent[i] = other
        o.adjacent[j] = (self, i)

    def __repr__(self):
        return repr(self.label)

    def entry_points(self):
        return [EntryPoint(self, i) for i in range(self.degree)]

    def already_assigned(self, node):
        """
        Returns true if the index is already assigned
        """

        already_assigned = []

        for adjacent in self.adjacent:
            if adjacent is None:
                already_assigned.append(False)
            else:
                if adjacent[0] == node:
                    already_assigned.append(True)
                else:
                    already_assigned.append(False)

        return any(already_assigned)


class Vertex(BaseVertex):
    pass


class Crossing(BaseVertex):
    """
    A crossing has four inputs, labeled 0, 1, 2, 3 in anticlockwise
    order.  Convention is 0 - 2 crosses *under* 1, 3.
    """

    def __init__(self, label):
        BaseVertex.__init__(self, 4, label)

    def flow(self, i):
        return self.adjacent[(i + 2) % 4]


class Edge(BaseVertex):
    def __init__(self, label):
        BaseVertex.__init__(self, 2, label)

    def fuse(self):
        """
        Joins the incoming and outgoing strands and removes
        self from the picture.
        """
        (A, i), (B, j) = self.adjacent
        A[i] = B[j]

    def flow(self, i):
        return self.adjacent[(i + 1) % 2]


