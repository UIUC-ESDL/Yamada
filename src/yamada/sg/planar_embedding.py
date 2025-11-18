# Global imports
import numpy as np
import networkx as nx

# Local Imports
from ..sgd.diagram_elements import Vertex, Crossing, Edge
from ..sgd.spatial_graph_diagrams import SpatialGraphDiagram


class PlanarEmbedding:

    def __init__(self, orderings, pos=None):

        # Initialize underlying NetworkX graph
        self.PE = nx.PlanarEmbedding()

        # Validate the ordering
        orderings = self._validate_ordering(orderings)

        # Add the ordering to the PlanarEmbedding
        nodes = orderings.keys()
        self.add_nodes_from(nodes)

        # Add half-edges according to the ordering
        for u, nbrs in orderings.items():

            ordered_nbrs = [v for v, _ in sorted(nbrs.items(), key=lambda kv: kv[1])]

            first = ordered_nbrs[0]
            self.add_half_edge_first(u, first)
            prev = first
            for v in ordered_nbrs[1:]:
                self.add_half_edge_ccw(u, v, prev)
                prev = v

        # Check the structure
        self.check_structure()

        # Set default positions
        if pos is None: pos = nx.planar_layout(self)
        nx.set_node_attributes(self, pos, 'pos')


    def __getattr__(self, name):
        """
        Get attributes from the underlying NetworkX graph.
        """
        return getattr(self.PE, name)

    @staticmethod
    def _validate_ordering(orderings):

        assert isinstance(orderings, dict), \
               "Ordering must be a dictionary."

        assert all(isinstance(k, str) for k in orderings.keys()), \
               "Ordering keys must be strings."

        assert all(isinstance(v, dict) for v in orderings.values()), \
               "Ordering values must be dictionaries."

        assert all(all(isinstance(k, str) for k in v.keys()) for v in orderings.values()), \
               "Ordering inner keys must be strings."

        assert all(all(isinstance(i, int) for i in v.values()) for v in orderings.values()), \
               "Ordering inner values must be integers."

        # Ensure symmetric ordering
        for v, nbrs in orderings.items():
            assert v not in nbrs,               f"Node {v} cannot be a neighbor of itself."
            assert len(nbrs) == len(set(nbrs)),  "Duplicate neighbors found."
            for u in nbrs:
                assert u in orderings,    f"Neighbor {u} is not a key in ordering."
                assert v in orderings[u], f"Ordering is not symmetric: {v} not in ordering[{u}]."
                ordered_nbrs = [v for v, _ in sorted(nbrs.items(), key=lambda kv: kv[1])]
                assert min(ordered_nbrs) == 0, "Indices must start at 0"
                assert max(ordered_nbrs) == len(ordered_nbrs) - 1, "Indices must be consecutive integers."

        return orderings


    def to_spatial_graph_diagram(self):



        # FIXME cyclic not catching adjacent crossins 1 and 2
        # Create a list of all nodes and crossings
        # nodes_and_crossings = list(self.nodes) + list(self.crossings.keys())
        nodes     = [node for node in self.Projection.nodes if "crossing" not in node]
        edges     = list(self.Projection.edges)
        crossings = list(self.crossings.keys())

        node_degrees = [self.Projection.degree(node) for node in nodes]

        # Create the vertex objects
        sgd_vertices = [Vertex(degree, 'v_' + node) for node, degree in zip(nodes, node_degrees)]

        # Create the edges
        # sgd_edges = [Edge('e_' + str(i)) for i in range(len(edges))]

        # # Create the vertex and crossing objects
        # vertex_node_degrees = [len([edge for edge in self.edges if node in edge]) for node in self.nodes]
        # vertices = [Vertex(degree, 'v_' + node) for node, degree in zip(self.nodes,vertex_node_degrees)]

        # if self.crossings is not None:
        #     crossings = [Crossing('c_' + str(i)) for i in range(len(self.crossings))]
        # else:
        #     crossings = []

        # Create the crossing objects
        sgd_crossings = [Crossing('c_' + crossing.split('_')[1]) for crossing in crossings]


        # Create a dictionary that contains the cyclical ordering of every node and crossing
        # node_ordering_dict = self.cyclic_order_vertices()
        # crossing_ordering_dict = self.cyclic_order_crossings()
        # cyclic_ordering_dict = {**node_ordering_dict, **crossing_ordering_dict}

        cyclic_ordering_dict = self.node_ordering_dict






        # Assign the vertices to each other according to the cyclic orderings
        nodes_and_crossings = nodes + crossings
        vertices_and_crossings = sgd_vertices + sgd_crossings

        for edge in self.edges:
            # TODO Use more consistent lookup
            node_a, node_b = edge

            if "crossing" in node_a:
                begin, middle, end = node_a.split("_")
                node_a = begin + "_" + middle

            if "crossing" in node_b:
                begin, middle, end = node_b.split("_")
                node_b = begin + "_" + middle

            node_a_index = nodes_and_crossings.index(node_a)
            node_b_index = nodes_and_crossings.index(node_b)

            vertex_a = vertices_and_crossings[node_a_index]
            vertex_b = vertices_and_crossings[node_b_index]

            if not vertex_a.already_assigned(vertex_b) and not vertex_b.already_assigned(vertex_a):

                vertex_b_index_for_vertex_a = cyclic_ordering_dict[node_a][node_b]
                vertex_a_index_for_vertex_b = cyclic_ordering_dict[node_b][node_a]

                vertex_a[vertex_b_index_for_vertex_a] = vertex_b[vertex_a_index_for_vertex_b]

            else:
                raise ValueError('The vertices are already assigned.')


        sgd = SpatialGraphDiagram(vertices=sgd_vertices, crossings=sgd_crossings)

        return sgd
