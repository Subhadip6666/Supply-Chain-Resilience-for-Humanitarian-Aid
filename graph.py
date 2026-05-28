from config import INF, NUM_NODES

def build_graph(use_subsidies=True):
    adj = [[INF] * NUM_NODES for _ in range(NUM_NODES)]

    for i in range(NUM_NODES):
        adj[i][i] = 0

    raw_edges = [
        (0, 1, 4),   (0, 2, 8),   (0, 4, 2),
        (1, 0, 4),   (1, 2, 3),   (1, 3, 5),   (1, 5, 7),
        (2, 0, 8),   (2, 1, 3),   (2, 3, 2),   (2, 6, 6),
        (3, 1, 5),   (3, 2, 2),   (3, 6, 4),   (3, 7, 8),
        (4, 0, 2),   (4, 5, 3),   (4, 8, 5),
        (5, 1, 7),   (5, 4, 3),   (5, 6, -2),  (5, 9, 4),
        (6, 2, 6),   (6, 3, 4),   (6, 5, -2),  (6, 7, 3),  (6, 10, 5),
        (7, 3, 8),   (7, 6, 3),   (7, 11, 6),
        (8, 4, 5),   (8, 9, -3),  (8, 10, 4),
        (9, 5, 4),   (9, 8, -3),  (9, 10, 2),  (9, 11, 5),
        (10, 6, 5),  (10, 8, 4),  (10, 9, 2),  (10, 11, 3),
        (11, 7, 6),  (11, 9, 5),  (11, 10, 3),
    ]

    edges = []
    for u, v, w in raw_edges:
        if not use_subsidies and w < 0:
            w = abs(w)
        adj[u][v] = w
        edges.append((u, v, w))

    return adj, edges
