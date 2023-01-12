# TODO Implement

# import networkx as nx
# from networkx.algorithms.planar_drawing import triangulate_embedding
# import numpy as np
# from collections import Counter
# from sage.all import sphere, line3d, polygon3d, colormaps, bezier3d

# def choose_outer_face(planar_graph):
#     G = planar_graph
#     half_edges = set(G.edges)
#     faces = []
#     while len(half_edges):
#         a, b = half_edges.pop()
#         face_edges = set()
#         face_verts = G.traverse_face(a, b, face_edges)
#         half_edges.difference_update(face_edges)        
#         faces.append(face_verts)

#     print(len(faces))
#     def score_face(face):
#         counts = Counter(G.degree[v] for v in face)
#         return counts[8]

#     # return [(score_face(face), face) for face in faces]
#     return min(faces, key=score_face)


# def tutte_system(planar_graph):
#     G, outer = triangulate_embedding(planar_graph, fully_triangulate=False)
#     #G = planar_graph
#     node_to_index = {node:index for index, node in enumerate(G.nodes())}
#     #outer = choose_outer_face(planar_graph)
#     n = G.number_of_nodes()
#     assert n == planar_graph.number_of_nodes()
#     inner_indices = np.array([node not in outer for node in G.nodes()])
#     L = nx.laplacian_matrix(G).toarray()
#     L = L[inner_indices, :]
#     M = np.zeros((len(outer), n))
#     for i, node in enumerate(outer):
#         M[i, node_to_index[node]] = 1
#     A = np.vstack([L, M])
#     Z = np.zeros(A.shape)
#     B = np.block([[A, Z], [Z, A]])
#     # set locations of boundary nodes
#     t = np.linspace(0, 2*np.pi, len(outer), endpoint=False)
#     x, y = 100*np.cos(t), 100*np.sin(t)
#     zeros = np.zeros(L.shape[0])
#     b = np.hstack([zeros, x, zeros, y])
#     return G, B, b

# def tutte_embedding_positions(planar_graph):
#     n = planar_graph.number_of_nodes()
#     G, A, b = tutte_system(planar_graph)
#     pos = np.linalg.solve(A, b)
#     pos = np.rint(pos)
#     x, y = pos[:n], pos[n:]
#     ans = dict()
#     for i, node in enumerate(G.nodes()):
#         ans[node] = (int(x[i]), int(y[i]))
#     return ans


# def position_spatial_graph_in_3D(G, z_height=20):
#     def norm_label(X):
#         L = X.label
#         return repr(L) if not isinstance(L, str) else L
        
#     P = G.underlying_planar_embedding()
#     planar_pos = tutte_embedding_positions(P)
#     system_node_pos = dict()
#     for V in G.vertices:
#         L = norm_label(V)
#         x, y = planar_pos[V.label]
#         system_node_pos[L] = (x, y, 0)

#     other_node_pos = dict()
#     for C in G.crossings:
#         L = norm_label(C)
#         x, y = planar_pos[C.label]
#         other_node_pos[L + '+'] = (x, y, z_height)
#         other_node_pos[L + '-'] = (x, y, -z_height)

#     nodes_so_far = system_node_pos.copy()
#     nodes_so_far.update(other_node_pos)

#     def end_label(edge, i):
#         i = i % 2
#         X, x = edge.adjacent[i]
#         L = norm_label(X)
#         if X in G.crossings:
#             L = L + '-' if x % 2 == 0 else L + '+'
#         return L

#     for E in G.edges:
#         L = norm_label(E)
#         x, y = planar_pos[E.label]
#         A = end_label(E, 0)
#         B = end_label(E, 1)
#         z = (nodes_so_far[A][2] + nodes_so_far[B][2]) // 2        
#         other_node_pos[L] = (x, y, z)
        
#     segments = list()
#     vertex_inputs = set()
#     for V in G.vertices:
#         vertex_inputs.update((V, i) for i in range(V.degree))
#     while len(vertex_inputs):
#         V, i = vertex_inputs.pop()
#         W, j = V.adjacent[i]
#         one_seg = []
#         while not W in G.vertices:
#             if W in G.edges:
#                 L = norm_label(W)
#                 A = end_label(W, j)
#                 B = end_label(W, j + 1)
#                 one_seg += [A, L]
#             W, j = W.flow(j)
#         one_seg.append(norm_label(W))
#         vertex_inputs.remove((W, j))
#         segments.append(one_seg)

#     return system_node_pos, other_node_pos, segments
        

    
# def draw_spatial_graph_in_3D(G, add_disks=False, z_height=20):
#     main_nodes, other_nodes, segs = position_spatial_graph_in_3D(G, z_height)
#     other_nodes.update(main_nodes)
#     nodes = other_nodes
#     scene = None
#     cmap = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
#             '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    
#     for i, (L, center) in enumerate(main_nodes.items()):
#         S = sphere(center, size=8, color=cmap[i % len(cmap)])
#         if scene is None:
#             scene = S
#         else:
#             scene += S

#         for i, one_seg in enumerate(segs):
#             scene += line3d([nodes[L] for L in one_seg],
#                         thickness=4, color=cmap[i % len(cmap)])

#     if add_disks:
#         for L, center in other_nodes.items():
#             if L.endswith('+'):
#                 x, y, z = center
#                 s = 6
#                 z = -0.5*z_height 
#                 scene += polygon3d([(x - s, y - s, z), (x + s, y - s, z),
#                                     (x + s, y + s, z), (x - s, y + s, z)], color='white')
    
#     return scene

  
        
                

# G = nx.check_planarity(nx.complete_graph(4))[1]
    
