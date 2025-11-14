"""Spatial Graphs

This module contains classes and functions for working with spatial graphs.
"""


import numpy as np
import networkx as nx
from itertools import combinations
from scipy.stats import qmc

from ..sg.geometry import (rotate,
                                compute_line_segment_intersection,
                                compute_intermediate_y_position,
                                compute_3D_intersection,
                                compute_counter_clockwise_angle)

from ..sgd.diagram_elements import Vertex, Crossing, Edge
from ..sgd.spatial_graph_diagrams import SpatialGraphDiagram
from ..utils.visualization import plot_spatial_graph


class SpatialGraph:
    """
    A class to represent a spatial graph.

    TODO Add an input checker
    TODO Fundamentally switch from rotating positions to defining rotating plane
    """



    def __init__(self,
                 nodes: list[str],
                 pos: dict,
                 edges: list[tuple[str, str]],
                 rotation=None):

        # Initialize the underlying NetworkX graph
        self.SG = nx.Graph()

        # Validate the inputs
        nodes = self._validate_nodes(nodes)
        edges = self._validate_edges(edges)
        pos   = self._validate_positions(nodes, pos)

        # Add the inputs to the SpatialGraph
        self.SG.add_nodes_from(nodes)
        self.SG.add_edges_from(edges)
        nx.set_node_attributes(self.SG, pos, 'pos')
        nx.set_node_attributes(self.SG, 'vertex','type')

        # self.nodes = nodes
        # self.edges = edges
        self.edge_pairs = list(combinations(self.edges, 2))

        self.adjacent_edge_pairs = self.get_adjacent_edge_pairs()
        self.nonadjacent_edge_pairs = [edge_pair for edge_pair in self.edge_pairs if
                                       edge_pair not in self.adjacent_edge_pairs]

        # Project the spatial graph onto a random the xz-plane
        # TODO Stop rotating everything, just define the rotation plane and show it; plane as object?
        pos, crossings = self.project(forced_rotation=rotation)
        nx.set_node_attributes(self.SG, pos, 'pos')

        # TODO Delete...
        self.crossings = crossings

        # Subdivide edges to add crossings
        self.subdivide_edges()

        self.node_ordering_dict, self.node_angle_dict = self.cyclic_orderings()




    def __getattr__(self, name):
        """
        Get attributes from the underlying NetworkX graph.
        """
        return getattr(self.SG, name)


    @staticmethod
    def _validate_nodes(nodes):
        assert isinstance(nodes, list),                      "Nodes must be a list."
        assert all(isinstance(node, str) for node in nodes), "All nodes must be strings."
        assert len(nodes) == len(set(nodes)),                "All nodes must be unique."
        return nodes

    @staticmethod
    def _validate_edges(edges):
        assert isinstance(edges, list),                                          "Edges must be a list."
        assert all(isinstance(s, str) and isinstance(t, str) for s, t in edges), "All edge nodes must be strings."
        assert all(isinstance(edge, tuple) for edge in edges),                   "All edges must be tuples."
        assert all(len(edge) == 2 for edge in edges),                            "All edges must have two nodes."
        assert len(edges) == len(set(edges)),                                    "All edges must be unique."
        return edges

    @staticmethod
    def _validate_positions(nodes, pos):
        assert isinstance(pos, dict),                                         "Positions must be a dictionary."
        assert all(isinstance(node, str) for node in pos.keys()),             "All position keys must be strings."
        assert all(isinstance(position, tuple) for position in pos.values()), "All position values must be lists, tuples, or numpy arrays."
        assert all(len(pos) == 3 for pos in pos.values()),                    "All position tuples must have three values."
        assert all(isinstance(coord, (int, float)) for position in pos.values() for coord in position), "All position coordinates must be numbers."
        assert set(nodes) == set(pos.keys()),                                 "All nodes must have a position and vice versa."
        return pos

    @property
    def pos2D(self):
        pos = nx.get_node_attributes(self.SG, 'pos')
        pos_2d = {node: (position[0], position[2]) for node, position in pos.items()}
        return pos_2d

    @property
    def pos3D(self):
        pos = nx.get_node_attributes(self.SG, 'pos')
        return pos

    @property
    def pos_2D_proj(self):
        pass

    @property
    def pos_3D_proj(self):
        pass


    def get_adjacent_edge_pairs(self):
        # TODO Replace with nx functions?
        adjacent_edge_pairs = set()  # Using a set to avoid duplicates

        # Create a dictionary that maps each node to the edges that contain it
        node_to_edges = {}

        for edge in self.edges:
            a, b = edge
            if a not in node_to_edges:
                node_to_edges[a] = []
            if b not in node_to_edges:
                node_to_edges[b] = []
            node_to_edges[a].append(edge)
            node_to_edges[b].append(edge)

        # Loop through each node and find pairs of edges connected to that node
        for node, edges in node_to_edges.items():
            for i in range(len(edges)):
                for j in range(i + 1, len(edges)):
                    # Add the pair of edges to the set (unordered pair)
                    adjacent_edge_pairs.add((edges[i], edges[j]))

        return list(adjacent_edge_pairs)  # Convert set to list for the result


    def get_edge_vertices_and_or_crossings(self, edge):
        """
        Returns a list of the vertices and crossings along a give edge, specifically ordered from -x to +x.
        FIXME What if the edge is perfectly vertical?
        """

        # Get edge's two nodes and their positions
        edge_nodes             = [node for node in edge]
        edge_node_positions_2D = [self.pos2D[node] for node in edge_nodes]
        edge_node_positions_3D = [self.pos3D[node] for node in edge_nodes]

        # Get crossing and positions (if applicable)
        edge_crossings = []
        edge_crossing_positions_2D = []
        edge_crossing_positions_3D = []
        for crossing, crossing_values in self.crossings.items():
            edge_pair = crossing_values['edges']
            if edge in edge_pair:
                idx       = edge_pair.index(edge)
                orientation = crossing_values['orientation'][idx]
                pos2D     = crossing_values['pos_2D']
                pos3D     = crossing_values['pos_3D'][idx]
                label     = f"{crossing}_{orientation}"

                edge_crossings.append(label)
                edge_crossing_positions_2D.append(pos2D)
                edge_crossing_positions_3D.append(pos3D)

        if len(edge_crossings) > 0:
            # Merge the vertices and crossings
            adjacent_nodes        = edge_nodes + edge_crossings
            adjacent_positions_2D = np.vstack((edge_node_positions_2D, edge_crossing_positions_2D))
            adjacent_positions_3D = np.vstack((edge_node_positions_3D, edge_crossing_positions_3D))

        else:
            adjacent_nodes        = edge_nodes
            adjacent_positions_2D = edge_node_positions_2D
            adjacent_positions_3D = edge_node_positions_3D

        # Order vertices and crossings from left to right by x position (i.e., ascending position index 0)
        x_positions = np.array(adjacent_positions_2D)[:, 0]
        idx_sorted  = np.argsort(x_positions)

        ordered_nodes = [adjacent_nodes[i] for i in idx_sorted]
        ordered_positions_2D = [adjacent_positions_2D[i] for i in idx_sorted]
        ordered_positions_3D = [adjacent_positions_3D[i] for i in idx_sorted]

        # Attributes
        edge_labels     = [str(edge)] * len(ordered_nodes)
        sub_edge_labels = [str(i) for i in range(len(ordered_nodes) - 1)]


        return ordered_nodes, ordered_positions_2D, ordered_positions_3D, edge_labels, sub_edge_labels

    def cyclic_ordering(self, ref_node, ref_node_type, node_ordering_dict=None, node_angle_dict=None):

        # If no node ordering dictionary is provided, use the default node ordering dictionary
        if node_ordering_dict is None:
            node_ordering_dict = {}
        if node_angle_dict is None:
            node_angle_dict = {}


        # Initialize lists to store the adjacent node and edge information
        # Crossings are not relevant for this calculation since they exist along edges
        if ref_node_type == 'vertex':
            pos_x = np.array(self.pos2D[ref_node])
            nbrs     = list(self.neighbors(ref_node))
            pos_nbrs = np.array([self.pos2D[node] for node in nbrs])
        else:
            edge_1, edge_2 = self.crossings[ref_node]['edges']
            ori_ab, ori_cd = self.crossings[ref_node]['orientation']
            oris = [ori_ab, ori_ab, ori_cd, ori_cd]
            pos_x = self.crossings[ref_node]['pos_2D']
            (a, b), (c, d) = edge_1, edge_2
            nbrs     = [a, b, c, d]
            pos_nbrs = np.array([self.pos2D[node] for node in nbrs])

        # Shift nodes to the origin
        pos_nbrs -= pos_x

        # Horizontal line (reference for angles)
        ref_vector = np.array([1, 0])

        angles = []
        for pos_nbr in pos_nbrs:
            angle = compute_counter_clockwise_angle(ref_vector, pos_nbr)
            angles.append(angle)

        ordered_nodes     = [node     for _, node     in sorted(zip(angles, nbrs))]
        ordered_angles    = [angle    for angle, _ in sorted(zip(angles, nbrs))]

        if ref_node_type == 'vertex':
            ordered_indices = [i for i in range(len(ordered_nodes))]
        else:
            ordered_ori     = [ori for _, ori in sorted(zip(angles, oris))]
            ordered_indices = [0, 1, 2, 3] if ordered_ori[0] == 'under' else [1, 2, 3, 0]

        ccw_node_ordering = {}
        ccw_angle_ordering = {}
        for node, idx, angle in zip(ordered_nodes, ordered_indices, ordered_angles):

            # FIXME Strip _over/_under from crossing labels
            if 'crossing' in node:
                begin, middle, end = node.split("_")
                node = begin + "_" + middle

            ccw_node_ordering[node]  = idx
            ccw_angle_ordering[node] = angle

        # Make sure _over/_under stripped crossings are stored correctly
        # if ref_node_type == 'crossing':
        #     begin, middle, end = ref_node.split("_")
        #     ref_node = begin + "_" + middle

        node_ordering_dict[ref_node] = ccw_node_ordering
        node_angle_dict[ref_node]    = ccw_angle_ordering

        return node_ordering_dict, node_angle_dict

    def cyclic_orderings(self):
        node_ordering_dict = {}
        node_angle_dict    = {}

        # Crossings should only be visited once, but in 3D they are defined twice
        crossing_visited = set()

        for node in self.nodes:
            node_type = self.SG.nodes[node]['type']
            assert node_type == "vertex" or node_type == "crossing"

            if node_type == "crossing":
                # strip over/under from crossing label from crossing_0_over
                begin, middle, end = node.split("_")
                node = begin + "_" + middle

            if node not in crossing_visited:
                node_ordering_dict, node_angle_dict = self.cyclic_ordering(node, node_type, node_ordering_dict, node_angle_dict)
                crossing_visited.add(node)

        return node_ordering_dict, node_angle_dict


    def subdivide_edge(self, edge):

        edge_nodes_and_or_crossings, positions_2D, positions_3D, edge_labels, sub_edge_labels = self.get_edge_vertices_and_or_crossings(edge)

        # If there are no crossings, return empty lists
        if len(edge_nodes_and_or_crossings) == 2:
            return [], [], [], [], [], []

        else:
            # Sanity check nodes are only first and last
            old_edges = [edge]
            new_nodes = [node for node in edge_nodes_and_or_crossings[1:-1]]
            new_edges = [(edge_nodes_and_or_crossings[i], edge_nodes_and_or_crossings[i + 1]) for i in
                            range(len(edge_nodes_and_or_crossings) - 1)]
            new_positions_3D = [tuple(positions_3D[i]) for i in range(1, len(positions_3D) - 1)]

            return old_edges, new_nodes, new_edges, new_positions_3D, edge_labels, sub_edge_labels


    def subdivide_edges(self):

        all_edges_to_remove = []
        all_nodes_to_add    = []
        all_edges_to_add    = []
        all_pos_to_add      = []
        all_edge_labels = []
        all_sub_edge_labels = []
        for edge in self.edges:
            edges_to_remove, nodes_to_add, edges_to_add, pos_to_add, edge_labels, sub_edge_labels = self.subdivide_edge(edge)
            all_edges_to_remove += edges_to_remove
            all_nodes_to_add    += nodes_to_add
            all_edges_to_add    += edges_to_add
            all_pos_to_add      += pos_to_add
            all_edge_labels     += edge_labels
            all_sub_edge_labels += sub_edge_labels

        # Update the Spatial Graph (remove old edges, add crossing nodes, add new edges)
        self.SG.remove_edges_from(all_edges_to_remove)
        self.SG.add_nodes_from(all_nodes_to_add)
        self.SG.add_edges_from(all_edges_to_add)
        nx.set_node_attributes(self.SG, {node: pos for node, pos in zip(all_nodes_to_add, all_pos_to_add)}, 'pos')
        nx.set_node_attributes(self.SG, {node: 'crossing' for node in all_nodes_to_add}, 'type')
        nx.set_edge_attributes(self.SG, {edge: edge_label for edge, edge_label in zip(all_edges_to_add, all_edge_labels)}, 'edge_label')
        nx.set_edge_attributes(self.SG, {edge: sub_edge_label for edge, sub_edge_label in zip(all_edges_to_add, all_sub_edge_labels)}, 'sub_edge_label')
        print("Done")



    def project(self, max_iter=10, forced_rotation=None):
        """
        Project the spatial graph onto a random 2D plane.

        The projection is done by applying a random 3D rotation to the graph and then projecting it onto a 2D plane.
        For simplicity, we use the transformed XZ plane. When the rotation is complete, the program checks that the
        projected graph for several things.

        First, it checks to make sure that no combinations of edges and/or nodes are overlapping.

        Second, it checks to make sure that no edges are perfectly vertical or perfectly horizontal. While neither of
        these cases technically incorrect, it's easier to implement looping through rotations rather than add edge cases
        in for these cases.

        """


        # Convert the node positions to a numpy array
        pos_arr = np.array([self.pos3D[node] for node in self.nodes])

        # Either use the forced rotation or generate a random sequence of candidate rotations.
        if forced_rotation is not None:
            rotations = [forced_rotation]
        else:
            # Define the random rotations (in a deterministic manner w/ a Halton sequence)
            sampler        = qmc.Halton(d=3, scramble=False)
            halton_samples = sampler.random(n=max_iter)
            rotations      = 2 * np.pi * halton_samples

        for rotation in rotations:

            # Initialize the bad rotation flag
            bad_rotation = False

            # Rotate the node positions
            pos_arr_rot   = rotate(pos_arr, rotation)

            # First, check that no edges are perfectly vertical or perfectly horizontal.
            # While neither of these cases is technically incorrect, it's easier to implement looping through rotations
            # rather than add edge cases for each 2D and 3D line equation.

            for edge in self.edges:
                a, b      = edge
                x1, _, z1 = pos_arr_rot[list(self.nodes).index(a)]
                x2, _, z2 = pos_arr_rot[list(self.nodes).index(b)]

                if np.isclose(x1, x2) or np.isclose(z1, z2):
                    print('An edge is vertical or horizontal. This is not a valid spatial graph.')
                    bad_rotation = True
                    break

            if bad_rotation:
                continue

            # Second, check adjacent edge pairs for validity.
            # Since adjacent segments are straight lines, they should only intersect at a single endpoint.
            # The only other possibility is for them to infinitely overlap, which is not a valid spatial graph.

            crossings = {}

            for edge_1, edge_2 in self.nonadjacent_edge_pairs:

                # Get the crossing in 2D and 3D
                a, b = edge_1
                c, d = edge_2
                pos_a_3D = pos_arr_rot[list(self.nodes).index(a)]
                pos_b_3D = pos_arr_rot[list(self.nodes).index(b)]
                pos_c_3D = pos_arr_rot[list(self.nodes).index(c)]
                pos_d_3D = pos_arr_rot[list(self.nodes).index(d)]

                pos_a_2D = pos_a_3D[[0, 2]]
                pos_b_2D = pos_b_3D[[0, 2]]
                pos_c_2D = pos_c_3D[[0, 2]]
                pos_d_2D = pos_d_3D[[0, 2]]

                # First, in 2D
                min_dist, min_dist_pos, _ = compute_line_segment_intersection(pos_a_2D, pos_b_2D, pos_c_2D, pos_d_2D)
                y_ab = compute_intermediate_y_position(pos_a_3D, pos_b_3D, x_int=min_dist_pos[0], z_int=min_dist_pos[1])
                y_cd = compute_intermediate_y_position(pos_c_3D, pos_d_3D, x_int=min_dist_pos[0], z_int=min_dist_pos[1])
                pos_x_ab = np.array([min_dist_pos[0], y_ab, min_dist_pos[1]])
                pos_x_cd = np.array([min_dist_pos[0], y_cd, min_dist_pos[1]])

                if np.isclose(min_dist, 0., atol=1e-4):

                    # Ensure that the crossing does not occur at an endpoint
                    assert_1 = np.allclose(min_dist_pos, pos_a_2D, atol=1e-4)
                    assert_2 = np.allclose(min_dist_pos, pos_b_2D, atol=1e-4)
                    assert_3 = np.allclose(min_dist_pos, pos_c_2D, atol=1e-4)
                    assert_4 = np.allclose(min_dist_pos, pos_d_2D, atol=1e-4)
                    if any([assert_1, assert_2, assert_3, assert_4]):
                        bad_rotation = True
                        print('These crossings should not intersect at endpoints.')

                    # elif crossing_position is np.inf:
                    #     raise ValueError('The edges are overlapping. This is not a valid spatial graph.')


                    edges = (edge_1, edge_2)
                    label = f"crossing_{len(crossings)}"

                    # Define the over and under strands, based on y position
                    idx_over = np.argmax([pos_x_ab[1], pos_x_cd[1]])
                    idx_under = np.argmin([pos_x_ab[1], pos_x_cd[1]])
                    assert idx_over != idx_under, "Error in determining over and under strands."

                    # FIXME, reverse logic? Plotting y pointing away
                    orientation = ['over', 'under'] if pos_x_ab[1] < pos_x_cd[1] else ['under', 'over']
                    # FIXME This information gets stale, maybe store % along edge instead?
                    crossings[label] = {'edges': edges,
                                        'pos_3D': [pos_x_ab, pos_x_cd],
                                        'orientation': orientation,
                                        'pos_2D': np.array([min_dist_pos[0], min_dist_pos[1]])}

            if bad_rotation:
                continue


            # If all are satisfied
            break


        else:
            # No rotation succeeded
            raise RuntimeError("Failed to find a valid projection (all rotations invalid).")

        # Convert back to dictionary
        pos_rot = {node: pos_arr_rot[i] for i, node in enumerate(self.nodes)}

        return pos_rot, crossings

    def to_spatial_graph_diagram(self):
        #FIXME cyclic not catching adjacent crossins 1 and 2
        # # Create a list of all nodes and crossings
        # nodes_and_crossings = list(self.nodes) + list(self.crossings.keys())
        nodes     = [node for node in self.nodes if "crossing" not in node]
        edges     = list(self.edges)
        crossings = list(self.crossings.keys())

        node_degrees = [self.degree(node) for node in nodes]

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


        # for sub_edge in self.edges:
        #     node_a, node_b = sub_edge
        #
        #     node_a_index = nodes_and_crossings.index(node_a)
        #     node_b_index = nodes_and_crossings.index(node_b)
        #
        #     vertex_a = vertices_and_crossings[node_a_index]
        #     vertex_b = vertices_and_crossings[node_b_index]
        #
        #     if not vertex_a.already_assigned(vertex_b) and not vertex_b.already_assigned(vertex_a):
        #
        #         vertex_b_index_for_vertex_a = cyclic_ordering_dict[node_a][node_b]
        #         vertex_a_index_for_vertex_b = cyclic_ordering_dict[node_b][node_a]
        #
        #         vertex_a[vertex_b_index_for_vertex_a] = vertex_b[vertex_a_index_for_vertex_b]
        #
        #     else:
        #         raise ValueError('The vertices are already assigned.')


        sgd = SpatialGraphDiagram(vertices=sgd_vertices, crossings=sgd_crossings)

        return sgd

    def plot(self):

        plotter = plot_spatial_graph(self.nodes, self.edges, self.pos3D,self.pos2D,
                                     self.node_ordering_dict, self.node_angle_dict, self)
        plotter.show()

