"""EXAMPLE

Enumerate all spatial graphs for a given system architecture.

This example is not implemented yet since the source code is still under development.

"""

import networkx as nx
import multiprocessing
import time
import glob
import pickle
import pandas as pd
import numpy as np
import collections
import os
import json

from yamada import (spatial_graph_diagrams_fixed_crossings,
                    pickle_yamada, to_poly)
from tutte import position_spatial_graph_in_3D

def one_graph(nodes):
    while True:
        G = nx.random_regular_graph(3, nodes)
        if nx.edge_connectivity(G) < 3:
            continue
        if nx.check_planarity(G)[0]:
            continue
        return G



def large_spectral_gap(nodes, tries=100):
    graphs = [one_graph(nodes) for _ in range(tries)]
    poss = [(-num_automorphisms(G), nx.laplacian_spectrum(G)[1], G)
            for G in graphs]
    return max(poss, key=lambda x:x[:2])


# num automorphisms: [24, 72, 12, 2, 1, 1, 1, 1, 1]

graph_data = {
    4: [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)],
    6: [(0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 0), (2, 5), (3, 5), (4, 5)],
    8: [(0, 1), (0, 2), (0, 7), (1, 3), (1, 5), (3, 2), (3, 4), (4, 6), (5, 2),
        (5, 6), (7, 4), (7, 6)],
    10: [(0, 1), (0, 3), (0, 8), (1, 8), (1, 9), (2, 6), (2, 9), (3, 2), (3, 4),
         (4, 5), (4, 7), (5, 6), (5, 9), (7, 6), (8, 7)],
    12: [(1, 5), (2, 4), (2, 6), (3, 0), (3, 8), (4, 7), (5, 7), (6, 5), (6, 11),
         (8, 0), (8, 4), (9, 2), (9, 7), (9, 10), (10, 1), (10, 3), (11, 0), (11, 1)],
    14: [(0, 9), (0, 10), (1, 7), (2, 3), (2, 11), (3, 0), (4, 2), (4, 6),
         (4, 10), (5, 11), (5, 12), (5, 13), (6, 9), (6, 13), (7, 9), (8, 1),
         (8, 12), (10, 1), (11, 7), (12, 3), (13, 8)],
    16: [(0, 2), (0, 8), (1, 10), (2, 5), (2, 14), (3, 7), (3, 8), (4, 5), (4, 8),
         (4, 15), (6, 0), (6, 10), (6, 12), (7, 10), (7, 13), (9, 1), (9, 5),
         (9, 11), (11, 14), (12, 3), (12, 11), (14, 13), (15, 1), (15, 13)],
    18: [(0, 4), (0, 14), (1, 13), (2, 1), (3, 5), (3, 7), (3, 15), (4, 13),
         (5, 10), (5, 16), (6, 9), (6, 12), (6, 16), (7, 4), (8, 2), (8, 14),
         (9, 2), (9, 11), (10, 0), (10, 1), (11, 13), (11, 15), (12, 7), (12, 8),
         (14, 17), (15, 17), (16, 17)],
    20: [(0, 8), (0, 11), (0, 14), (1, 9), (3, 9), (3, 10), (4, 1), (4, 13),
         (4, 15), (5, 14), (5, 17), (6, 11), (6, 17), (6, 18), (7, 16), (8, 7),
         (8, 13), (10, 2), (10, 11), (12, 9), (12, 15), (12, 19), (14, 1),
         (15, 7), (16, 2), (16, 17), (18, 3), (18, 13), (19, 2), (19, 5)],
}

def graph(nodes):
    G = nx.MultiGraph()
    G.add_edges_from(graph_data[nodes])
    return G

def summarize_timings():
    nodes = [6, 8, 10, 12, 14]
    cross = [0, 1, 2, 3, 4, 5, 6]
    df = pd.DataFrame(index=nodes, columns=cross)
    for n in nodes:
        pick = read_pickle(n)
        for c, v in pick[1].items():
            df.loc[n, c] = v
    return df

def summarize_num_distinct_topologies():
    nodes = [6, 8, 10, 12, 14]
    cross = [0, 1, 2, 3, 4, 5, 6]
    df = pd.DataFrame(index=nodes, columns=cross)
    for n in nodes:
        pick = read_pickle(n)
        cross_counts = collections.Counter(
            [len(SGD.crossings) for SGD in pick[0].values()])
        print(cross_counts)
        for c, v in cross_counts.items():
            df.loc[n, c] = v
    return df


def export_topologies():
    nodes = [6, 8, 10, 12, 14]
    cross = [0, 1, 2, 3, 4, 5, 6]
    for n in nodes:
        by_cross = collections.defaultdict(list)
        for poly, SGD in read_pickle(n)[0].items():
            cross = len(SGD.crossings)
            index = len(by_cross[cross])
            datum = {'nodes':n,
                     'crossings':cross,
                     'index':index,
                     'name':f'G{n}C{cross}I{index}',
                     'yamada':repr(poly),
                     '3D_positions':position_spatial_graph_in_3D(SGD)}
            by_cross[cross].append(datum)
            target_dir = f'distinct_topos/G{n}/C{cross}'
            os.makedirs(target_dir, exist_ok=True)
            with open(target_dir + '/' + datum['name'] + '.json', 'w') as file:
                json.dump(datum, file)
            
        
