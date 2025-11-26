# Global imports
import networkx as nx

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



