from config import INF, NUM_NODES, SUBSIDISED_EDGES, SHORT_NAMES, NODE_NAMES
import sys
import os

# Add parent directory to sys.path so we can import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ui import print_color, Colors, print_slow, animate_typing_human

def bellman_ford(adj, edges, source=0):
    V = NUM_NODES
    dist = [INF] * V
    pred = [-1] * V
    dist[source] = 0

    dist_history = []

    for iteration in range(V - 1):
        for u, v, w in edges:
            if pred[u] == v:
                continue

            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u

                if (u, v) in SUBSIDISED_EDGES:
                    pass
        dist_history.append(list(dist))

    has_negative_cycle = False
    for u, v, w in edges:
        if pred[u] == v:
            continue
        if dist[u] != INF and dist[u] + w < dist[v]:
            has_negative_cycle = True
            break

    return dist, pred, has_negative_cycle, dist_history

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
    print_color("\n" + "=" * 60, Colors.LIGHT_BLUE)
    print_color("  BELLMAN-FORD RESULTS  (Source: Central Warehouse / HQ)", Colors.BOLD + Colors.LIGHT_BLUE)
    print_color("=" * 60, Colors.LIGHT_BLUE)

    for node in range(1, NUM_NODES):
        path = reconstruct_path(pred, node)
        path_str = " → ".join(SHORT_NAMES[n] for n in path)
        subsidy_tag = f"  {Colors.LIGHT_GREEN}[uses subsidised route]{Colors.ENDC}" if path_uses_subsidy(path) else ""
        name = NODE_NAMES[node]
        animate_typing_human(f"  Node {node:>2} ({name:<16}) | Cost: {dist[node]:>4} | Path: {path_str}{subsidy_tag}\n", delay_base=0.01)

    print_color("=" * 60, Colors.LIGHT_BLUE)

def print_bf_iterations(edges, dist_history):
    """
    Prints a table showing the distance array after each of the first 3
    relaxation rounds of Bellman-Ford (first 3 iterations only).
    """
    cols = ["Iteration"] + [SHORT_NAMES[i] for i in range(12)]
    widths = [len(c) for c in cols]
    
    header_str = " | ".join(f"{cols[i]:^{widths[i]}}" for i in range(len(cols)))
    print_color("\n" + header_str, Colors.LIGHT_BLUE)
    
    for it in range(3):
        if it < len(dist_history):
            row_vals = [f"{it + 1}"]
            for node in range(12):
                d = dist_history[it][node]
                val_str = "INF" if d == INF else f"{int(d) if d == int(d) else d}"
                row_vals.append(val_str)
            row_str = " | ".join(f"{row_vals[i]:^{widths[i]}}" for i in range(len(cols)))
            print(row_str)
