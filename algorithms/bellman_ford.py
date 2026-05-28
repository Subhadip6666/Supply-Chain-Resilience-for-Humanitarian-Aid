from config import INF, NUM_NODES, SUBSIDISED_EDGES, SHORT_NAMES, NODE_NAMES

def bellman_ford(adj, edges, source=0):
    V = NUM_NODES
    dist = [INF] * V
    pred = [-1] * V
    dist[source] = 0

    for iteration in range(V - 1):
        for u, v, w in edges:
            if pred[u] == v:
                continue

            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u

                if (u, v) in SUBSIDISED_EDGES:
                    pass

    has_negative_cycle = False
    for u, v, w in edges:
        if pred[u] == v:
            continue
        if dist[u] != INF and dist[u] + w < dist[v]:
            has_negative_cycle = True
            break

    return dist, pred, has_negative_cycle

def reconstruct_path(pred, target):
    path = []
    node = target
    while node != -1:
        path.append(node)
        node = pred[node]
    path.reverse()
    return path

def path_uses_subsidy(path):
    for i in range(len(path) - 1):
        if (path[i], path[i + 1]) in SUBSIDISED_EDGES:
            return True
    return False

def print_bellman_ford_results(dist, pred):
    print("\n" + "=" * 60)
    print("  BELLMAN-FORD RESULTS  (Source: Central Warehouse / HQ)")
    print("=" * 60)

    for node in range(1, NUM_NODES):
        path = reconstruct_path(pred, node)
        path_str = " → ".join(SHORT_NAMES[n] for n in path)
        subsidy_tag = "  [uses subsidised route]" if path_uses_subsidy(path) else ""
        name = NODE_NAMES[node]
        print(f"  Node {node:>2} ({name:<16}) | Cost: {dist[node]:>4} | Path: {path_str}{subsidy_tag}")

    print("=" * 60)
