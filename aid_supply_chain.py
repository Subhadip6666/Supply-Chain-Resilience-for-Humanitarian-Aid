"""
Humanitarian Aid Supply Chain Optimisation System
==================================================
Uses Bellman-Ford (shortest paths with negative edges) and
Hamiltonian Cycle (backtracking with pruning) to plan optimal
delivery routes after a cyclone disaster.

Authors : Subhadip Patra
Course  : CS302
"""

import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import copy
import time
import random

class Colors:
    LIGHT_RED = '\033[91m'      # Bright Red
    LIGHT_VIOLET = '\033[95m'   # Bright Magenta / Violet
    LIGHT_PURPLE = '\033[38;5;141m' # Light Purple (256 color)
    LIGHT_GREEN = '\033[92m'    # Bright Green
    LIGHT_BLUE = '\033[96m'     # Bright Cyan / Light Blue
    
    HEADER = '\033[38;5;141m'   # Light Purple
    OKBLUE = '\033[96m'         # Light Blue
    OKCYAN = '\033[96m'         # Light Blue
    OKGREEN = '\033[92m'        # Light Green
    WARNING = '\033[93m'        # Bright Yellow
    FAIL = '\033[91m'           # Light Red
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_slow(text, delay=0.01, color=Colors.ENDC, end='\n'):
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(Colors.ENDC)
    sys.stdout.write(end)
    sys.stdout.flush()

def animate_typing_human(text, delay_base=0.015, color=Colors.ENDC, end='\n'):
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(max(0.002, delay_base + random.uniform(-0.005, 0.02)))
    sys.stdout.write(Colors.ENDC)
    sys.stdout.write(end)
    sys.stdout.flush()

def print_color(text, color=Colors.ENDC, end='\n'):
    sys.stdout.write(color + text + Colors.ENDC + end)
    sys.stdout.flush()

def animate_spinner(message, duration=0.8):
    spinner_chars = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    sys.stdout.write(Colors.OKCYAN + message + " ")
    i = 0
    while time.time() < end_time:
        sys.stdout.write(spinner_chars[i % len(spinner_chars)])
        sys.stdout.flush()
        time.sleep(0.05)
        sys.stdout.write('\b')
        i += 1
    sys.stdout.write(Colors.OKGREEN + "Done!" + Colors.ENDC + "\n")
    sys.stdout.flush()

def animate_progress_bar(message, duration=0.8, length=30, color=Colors.OKCYAN):
    sys.stdout.write(color + message + " [" + Colors.ENDC)
    steps = length
    sleep_time = duration / steps
    for i in range(steps):
        sys.stdout.write(color + "█" + Colors.ENDC)
        sys.stdout.flush()
        time.sleep(sleep_time)
    sys.stdout.write(color + "] " + Colors.OKGREEN + "Complete!\n" + Colors.ENDC)
    sys.stdout.flush()
# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
INF = float('inf')
NUM_NODES = 12

# Human-readable names for each node
NODE_NAMES = {
    0:  "Central Warehouse (HQ)",
    1:  "Depot A",
    2:  "Depot B",
    3:  "Depot C",
    4:  "Village 1",
    5:  "Village 2",
    6:  "Village 3",
    7:  "Village 4",
    8:  "Village 5",
    9:  "Village 6",
    10: "Village 7",
    11: "Village 8",
}

# Short names for compact printing
SHORT_NAMES = {
    0: "HQ", 1: "Depot A", 2: "Depot B", 3: "Depot C",
    4: "Village 1", 5: "Village 2", 6: "Village 3", 7: "Village 4",
    8: "Village 5", 9: "Village 6", 10: "Village 7", 11: "Village 8",
}

# Negative (subsidised) edges and their real-world explanation
SUBSIDISED_EDGES = {
    (5, 6): "State government subsidises this coastal road (cost -2)",
    (6, 5): "State government subsidises this coastal road (cost -2)",
    (8, 9): "NGO covers fuel cost on this relief corridor (cost -3)",
    (9, 8): "NGO covers fuel cost on this relief corridor (cost -3)",
}


# ======================================================================
# FUNCTION: build_graph
# ======================================================================
def build_graph(use_subsidies=True):
    """
    Build and return the 12×12 adjacency matrix.

    Parameters
    ----------
    use_subsidies : bool
        If True, negative edges are kept (subsidised routes active).
        If False, negative edges are replaced with their absolute values.

    Returns
    -------
    adj : list[list[float]]
        12×12 adjacency matrix.
    edges : list[tuple]
        List of (u, v, weight) for every finite edge.
    """
    adj = [[INF] * NUM_NODES for _ in range(NUM_NODES)]

    # Set diagonal to 0 (distance from a node to itself)
    for i in range(NUM_NODES):
        adj[i][i] = 0

    # Define all edges as (u, v, weight)
    raw_edges = [
        (0, 1, 4),   (0, 2, 8),   (0, 4, 2),
        (1, 0, 4),   (1, 2, 3),   (1, 3, 5),   (1, 5, 7),
        (2, 0, 8),   (2, 1, 3),   (2, 3, 2),   (2, 6, 6),
        (3, 1, 5),   (3, 2, 2),   (3, 6, 4),   (3, 7, 8),
        (4, 0, 2),   (4, 5, 3),   (4, 8, 5),
        # Edge 5↔6: cost -2 — state government subsidises this coastal road
        (5, 1, 7),   (5, 4, 3),   (5, 6, -2),  (5, 9, 4),
        # Edge 6↔5: cost -2 — state government subsidises this coastal road
        (6, 2, 6),   (6, 3, 4),   (6, 5, -2),  (6, 7, 3),  (6, 10, 5),
        (7, 3, 8),   (7, 6, 3),   (7, 11, 6),
        # Edge 8↔9: cost -3 — NGO covers fuel cost on this relief corridor
        (8, 4, 5),   (8, 9, -3),  (8, 10, 4),
        # Edge 9↔8: cost -3 — NGO covers fuel cost on this relief corridor
        (9, 5, 4),   (9, 8, -3),  (9, 10, 2),  (9, 11, 5),
        (10, 6, 5),  (10, 8, 4),  (10, 9, 2),  (10, 11, 3),
        (11, 7, 6),  (11, 9, 5),  (11, 10, 3),
    ]

    edges = []
    for u, v, w in raw_edges:
        if not use_subsidies and w < 0:
            # Replace negative cost with absolute value (no subsidy scenario)
            w = abs(w)
        adj[u][v] = w
        edges.append((u, v, w))

    return adj, edges


# ======================================================================
# FUNCTION: bellman_ford
# ======================================================================
def bellman_ford(adj, edges, source=0):
    """
    Manually implemented Bellman-Ford algorithm.

    Performs V-1 = 11 relaxation rounds, then one extra round for
    negative-cycle detection.

    NOTE ON UNDIRECTED NEGATIVE EDGES:
    In this graph, subsidised routes (edges 5↔6 and 8↔9) have
    negative costs in both directions. In an undirected graph,
    this would normally create a trivial 2-node negative cycle
    (e.g. 5→6→5 = -2 + -2 = -4). To handle this correctly,
    we use parent-aware relaxation: when relaxing edge u→v,
    we skip it if v is already the predecessor of u (i.e. we
    just came from v). This prevents the algorithm from
    bouncing back and forth on the same edge.

    Parameters
    ----------
    adj   : adjacency matrix (unused directly, kept for interface consistency)
    edges : list of (u, v, w) tuples
    source: starting node (default 0 = HQ)

    Returns
    -------
    dist : list[float]   — shortest cost from source to every node
    pred : list[int]     — predecessor array for path reconstruction
    has_negative_cycle : bool
    """
    V = NUM_NODES

    # Initialise distances and predecessors
    dist = [INF] * V
    pred = [-1] * V
    dist[source] = 0

    # ---- V-1 relaxation rounds ----
    for iteration in range(V - 1):  # exactly 11 rounds
        for u, v, w in edges:
            # Parent-aware relaxation: skip if v is already the parent of u.
            # This prevents trivial 2-node negative cycles on undirected
            # negative-weight edges (e.g. subsidised routes 5↔6 and 8↔9).
            if pred[u] == v:
                continue

            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u

                # Log when a subsidised (negative) edge causes relaxation
                if (u, v) in SUBSIDISED_EDGES:
                    pass  # negative edge processed: subsidy applied

    # ---- Negative cycle detection (one extra round) ----
    # If any distance can still be reduced (respecting parent-awareness),
    # then a genuine negative cycle exists in the graph.
    has_negative_cycle = False
    for u, v, w in edges:
        if pred[u] == v:
            continue
        if dist[u] != INF and dist[u] + w < dist[v]:
            has_negative_cycle = True
            break

    return dist, pred, has_negative_cycle


def reconstruct_path(pred, target):
    """Trace back the predecessor array to build the full path."""
    path = []
    node = target
    while node != -1:
        path.append(node)
        node = pred[node]
    path.reverse()
    return path


def path_uses_subsidy(path):
    """Check whether any consecutive pair in the path is a subsidised edge."""
    for i in range(len(path) - 1):
        if (path[i], path[i + 1]) in SUBSIDISED_EDGES:
            return True
    return False


def print_bellman_ford_results(dist, pred):
    """Pretty-print Bellman-Ford shortest path results."""
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


# ======================================================================
# FUNCTION: build_complete_cost_matrix (integration helper)
# ======================================================================
def build_complete_cost_matrix(adj, edges):
    """
    Run Bellman-Ford from every node to build a complete
    shortest-cost matrix for all pairs.

    Returns
    -------
    cost_matrix : list[list[float]]
        cost_matrix[i][j] = shortest cost from i to j.
    all_preds : list[list[int]]
        Predecessor arrays for every source.
    """
    cost_matrix = [[INF] * NUM_NODES for _ in range(NUM_NODES)]
    all_preds = []

    for src in range(NUM_NODES):
        dist, pred, neg = bellman_ford(adj, edges, source=src)
        cost_matrix[src] = dist
        all_preds.append(pred)

    return cost_matrix, all_preds


# ======================================================================
# FUNCTION: hamiltonian_cycle
# ======================================================================
def hamiltonian_cycle(cost_matrix):
    """
    Find the minimum-cost Hamiltonian Cycle starting and ending at node 0
    using backtracking with pruning.

    Parameters
    ----------
    cost_matrix : list[list[float]]
        Complete cost matrix (shortest costs between all pairs).

    Returns
    -------
    best_path : list[int] or None
        The optimal circuit (list of node indices), or None if none exists.
    best_cost : float
        Total cost of the circuit (INF if none found).
    """
    V = NUM_NODES
    best_cost = INF
    best_path = None

    # Current path starts at HQ (node 0)
    current_path = [0]
    visited = [False] * V
    visited[0] = True

    def backtrack(current_node, current_cost, depth):
        nonlocal best_cost, best_path

        # Base case: all nodes visited — try to return to HQ
        if depth == V:
            return_cost = cost_matrix[current_node][0]
            if return_cost < INF:
                total = current_cost + return_cost
                if total < best_cost:
                    best_cost = total
                    best_path = current_path[:] + [0]  # complete the circuit
            return

        # Try every unvisited node
        for next_node in range(V):
            if visited[next_node]:
                continue
            edge_cost = cost_matrix[current_node][next_node]
            if edge_cost >= INF:
                continue  # no connection

            new_cost = current_cost + edge_cost

            # ---- Pruning: abandon if partial cost already exceeds best ----
            if new_cost >= best_cost:
                continue

            # Recurse
            visited[next_node] = True
            current_path.append(next_node)
            backtrack(next_node, new_cost, depth + 1)
            current_path.pop()
            visited[next_node] = False

    backtrack(0, 0, 1)
    return best_path, best_cost


def print_hamiltonian_results(best_path, best_cost):
    """Pretty-print the Hamiltonian circuit results."""
    print_color("\n" + "=" * 60, Colors.LIGHT_PURPLE)
    print_color("  HAMILTONIAN CIRCUIT  (Delivery Route)", Colors.BOLD + Colors.LIGHT_PURPLE)
    print_color("=" * 60, Colors.LIGHT_PURPLE)

    if best_path is None:
        print_color("  ⚠  No valid Hamiltonian circuit exists for this graph.", Colors.LIGHT_RED)
    else:
        circuit_str = " → ".join(SHORT_NAMES[n] for n in best_path)
        animate_typing_human(f"  Circuit : {circuit_str}\n", delay_base=0.015, color=Colors.LIGHT_GREEN)
        animate_typing_human(f"  Total Cost : {best_cost} units\n", delay_base=0.015, color=Colors.LIGHT_GREEN)

    print_color("=" * 60, Colors.LIGHT_PURPLE)


# ======================================================================
# FUNCTION: integrate_algorithms
# ======================================================================
def integrate_algorithms(use_subsidies=True):
    """
    Integration pipeline:
    1. Build graph
    2. Run Bellman-Ford from HQ (node 0) — print results
    3. Run Bellman-Ford from ALL nodes to get complete cost matrix
    4. Run Hamiltonian Cycle on the complete cost matrix
    5. Return results for visualisation and comparison

    Parameters
    ----------
    use_subsidies : bool
        Whether to use negative (subsidised) edges.

    Returns
    -------
    dict with keys: adj, edges, dist, pred, cost_matrix,
                    ham_path, ham_cost, use_subsidies
    """
    label = "WITH" if use_subsidies else "WITHOUT"
    print_color("\n" + "#" * 60, Colors.LIGHT_BLUE)
    print_color(f"  RUNNING SYSTEM — {label} SUBSIDISED ROUTES", Colors.BOLD + Colors.LIGHT_BLUE)
    print_color("#" * 60, Colors.LIGHT_BLUE)

    # Step 1: Build the graph
    adj, edges = build_graph(use_subsidies=use_subsidies)

    # Step 2: Bellman-Ford from HQ
    dist, pred, has_neg_cycle = bellman_ford(adj, edges, source=0)

    if has_neg_cycle:
        print_color("\n  ⚠⚠⚠  WARNING: Negative cycle detected in the graph!", Colors.LIGHT_RED + Colors.BOLD)
        print_color("  Shortest paths are undefined. Aborting this run.", Colors.LIGHT_RED)
        return None

    print_bellman_ford_results(dist, pred)

    # Step 3: Build complete cost matrix (all-pairs shortest paths)
    cost_matrix, all_preds = build_complete_cost_matrix(adj, edges)

    # Step 4: Hamiltonian Cycle on the complete cost matrix
    ham_path, ham_cost = hamiltonian_cycle(cost_matrix)
    print_hamiltonian_results(ham_path, ham_cost)

    return {
        "adj": adj,
        "edges": edges,
        "dist": dist,
        "pred": pred,
        "cost_matrix": cost_matrix,
        "ham_path": ham_path,
        "ham_cost": ham_cost,
        "use_subsidies": use_subsidies,
    }


# ======================================================================
# FUNCTION: visualise_graph
# ======================================================================
def visualise_graph(results):
    """
    Create two matplotlib figures:
      Figure 1 — Full graph with colour-coded nodes and edges
      Figure 2 — Bellman-Ford tree + Hamiltonian circuit overlay
    """
    if results is None:
        print("  Skipping visualisation (no valid results).")
        return

    adj = results["adj"]
    edges = results["edges"]
    pred = results["pred"]
    ham_path = results["ham_path"]
    ham_cost = results["ham_cost"]

    # --- Build NetworkX graph ---
    G = nx.Graph()
    for i in range(NUM_NODES):
        G.add_node(i, label=SHORT_NAMES[i])

    added = set()
    for u, v, w in edges:
        key = (min(u, v), max(u, v))
        if key not in added:
            G.add_edge(u, v, weight=w)
            added.add(key)

    # Use spring layout for consistent positioning
    pos = nx.spring_layout(G, seed=42, k=2.5)

    # --- Node colours ---
    node_colors = []
    for n in G.nodes():
        if n == 0:
            node_colors.append("#2ecc71")       # HQ — green
        elif n in (1, 2, 3):
            node_colors.append("#f39c12")       # Depots — orange
        else:
            node_colors.append("#85c1e9")       # Villages — light blue

    labels = {n: SHORT_NAMES[n] for n in G.nodes()}

    # ================================================================
    # FIGURE 1 — Full Graph
    # ================================================================
    fig1, ax1 = plt.subplots(1, 1, figsize=(14, 10))
    ax1.set_title("Figure 1 — Humanitarian Aid Supply Chain Network",
                  fontsize=15, fontweight='bold')

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, ax=ax1, node_color=node_colors,
                           node_size=700, edgecolors='black', linewidths=1.2)
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax1, font_size=7,
                            font_weight='bold')

    # Separate normal and subsidised edges for colouring
    normal_edges = []
    subsidy_edges = []
    for u, v, d in G.edges(data=True):
        key = (min(u, v), max(u, v))
        if key in {(5, 6), (8, 9)}:
            subsidy_edges.append((u, v))
        else:
            normal_edges.append((u, v))

    nx.draw_networkx_edges(G, pos, edgelist=normal_edges, ax=ax1,
                           edge_color='#3498db', width=2)
    nx.draw_networkx_edges(G, pos, edgelist=subsidy_edges, ax=ax1,
                           edge_color='red', width=3, style='dashed')

    # Edge labels
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax1,
                                 font_size=8)

    # Legend
    legend_handles = [
        mpatches.Patch(color='#2ecc71', label='HQ (Central Warehouse)'),
        mpatches.Patch(color='#f39c12', label='Regional Depots'),
        mpatches.Patch(color='#85c1e9', label='Villages'),
        mpatches.Patch(color='#3498db', label='Normal Route'),
        mpatches.Patch(color='red', label='Subsidised Route'),
    ]
    ax1.legend(handles=legend_handles, loc='lower left', fontsize=9)
    ax1.axis('off')
    fig1.tight_layout()
    fig1.savefig("figure1_full_graph.png", dpi=150, bbox_inches='tight')
    print("  ✓ Saved figure1_full_graph.png")

    # ================================================================
    # FIGURE 2 — Results (BF tree + Hamiltonian circuit)
    # ================================================================
    fig2, ax2 = plt.subplots(1, 1, figsize=(14, 10))
    ax2.set_title("Figure 2 — Shortest Path Tree & Hamiltonian Circuit",
                  fontsize=15, fontweight='bold')

    # Draw base graph lightly
    nx.draw_networkx_nodes(G, pos, ax=ax2, node_color=node_colors,
                           node_size=700, edgecolors='black', linewidths=1.2)
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax2, font_size=7,
                            font_weight='bold')
    nx.draw_networkx_edges(G, pos, ax=ax2, edge_color='#d5dbdb', width=1,
                           alpha=0.5)

    # Bellman-Ford shortest path tree edges (yellow)
    bf_tree_edges = []
    for node in range(1, NUM_NODES):
        p = pred[node]
        if p != -1:
            bf_tree_edges.append((p, node))

    nx.draw_networkx_edges(G, pos, edgelist=bf_tree_edges, ax=ax2,
                           edge_color='#f1c40f', width=4, alpha=0.8)

    # Hamiltonian Circuit (red arrows)
    if ham_path is not None:
        DG = nx.DiGraph()
        ham_edges = []
        for i in range(len(ham_path) - 1):
            ham_edges.append((ham_path[i], ham_path[i + 1]))
            DG.add_edge(ham_path[i], ham_path[i + 1])

        nx.draw_networkx_edges(DG, pos, edgelist=ham_edges, ax=ax2,
                               edge_color='red', width=2.5, arrows=True,
                               arrowsize=20, arrowstyle='-|>',
                               connectionstyle='arc3,rad=0.1')

        # Text box with total cost
        textstr = f"Hamiltonian Circuit Cost: {ham_cost} units"
        props = dict(boxstyle='round,pad=0.5', facecolor='lightyellow',
                     edgecolor='red', alpha=0.9)
        ax2.text(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=11,
                 verticalalignment='top', bbox=props)

    # Legend
    legend_handles2 = [
        mpatches.Patch(color='#f1c40f', label='Bellman-Ford Shortest Path Tree'),
        mpatches.Patch(color='red', label='Hamiltonian Circuit'),
    ]
    ax2.legend(handles=legend_handles2, loc='lower left', fontsize=9)
    ax2.axis('off')
    fig2.tight_layout()
    fig2.savefig("figure2_results.png", dpi=150, bbox_inches='tight')
    print("  ✓ Saved figure2_results.png")

    plt.show()


# ======================================================================
# FUNCTION: compare_costs
# ======================================================================
def compare_costs(results_with, results_without):
    """
    Print a comparison table showing the impact of subsidised routes
    on total delivery circuit cost (aligned with SDG 17 — Partnerships).
    """
    print_color("\n" + "=" * 60, Colors.LIGHT_PURPLE)
    print_color("  COST COMPARISON  (SDG 17 — Partnerships for the Goals)", Colors.BOLD + Colors.LIGHT_PURPLE)
    print_color("=" * 60, Colors.LIGHT_PURPLE)

    if results_with is None or results_without is None:
        print_color("  ⚠ Cannot compare — one or both runs failed.", Colors.LIGHT_RED)
        return

    cost_with = results_with["ham_cost"]
    cost_without = results_without["ham_cost"]

    if cost_with == INF or cost_without == INF:
        print_color("  ⚠ Cannot compare — Hamiltonian circuit not found in one/both runs.", Colors.LIGHT_RED)
        return

    savings = cost_without - cost_with

    animate_typing_human(f"  Without subsidised routes : {cost_without} units\n", delay_base=0.015)
    animate_typing_human(f"  With subsidised routes    : {cost_with} units\n", delay_base=0.015)
    animate_typing_human(f"  Savings through partnerships : {savings} units\n\n", delay_base=0.02)

    if savings > 0:
        pct = (savings / cost_without) * 100
        print_color(f"  → Government & NGO partnerships reduced delivery cost by {pct:.1f}%", Colors.LIGHT_GREEN + Colors.BOLD)
    elif savings == 0:
        print_color("  → No cost difference detected.", Colors.LIGHT_VIOLET)
    else:
        print_color("  → Subsidised routes actually increased cost (unusual scenario).", Colors.LIGHT_RED)

    print_color("=" * 60, Colors.LIGHT_PURPLE)


# ======================================================================
# FUNCTION: main
# ======================================================================
def main():
    # Ensure stdout handles UTF-8 characters correctly on all platforms, including Windows console
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    width = 58
    print_color("╔" + "═" * width + "╗", Colors.LIGHT_PURPLE)
    print_color("║" + "HUMANITARIAN AID SUPPLY CHAIN OPTIMISATION SYSTEM".center(width) + "║", Colors.BOLD + Colors.LIGHT_PURPLE)
    print_color("╠" + "═" * width + "╣", Colors.LIGHT_PURPLE)
    
    info_lines = [
        ("Author      : Subhadip Patra (Course: CS302)", Colors.LIGHT_RED),
        ("Semester    : 4th Semester University Project", Colors.LIGHT_RED),
        ("Algorithms  : Bellman-Ford & Hamiltonian Cycle", Colors.LIGHT_VIOLET),
        ("", Colors.LIGHT_VIOLET),
        ("Description :", Colors.LIGHT_VIOLET),
        ("A post-disaster humanitarian aid supply chain system", Colors.LIGHT_VIOLET),
        ("modelling relief supply delivery routes under SDG 17", Colors.LIGHT_VIOLET),
        ("(Partnerships for the Goals). Solves shortest paths", Colors.LIGHT_VIOLET),
        ("with government/NGO subsidies and plans optimal", Colors.LIGHT_VIOLET),
        ("circuits using backtracking with pruning.", Colors.LIGHT_VIOLET)
    ]
    for line_text, color in info_lines:
        print_color(f"║ {line_text.ljust(width - 2)} ║", color)
    print_color("╚" + "═" * width + "╝\n", Colors.LIGHT_PURPLE)

    animate_progress_bar("Booting Up Subsystems", duration=0.8, length=25, color=Colors.LIGHT_BLUE)
    print()

    # ---- Run 1: WITH subsidised (negative-cost) routes ----
    results_with = integrate_algorithms(use_subsidies=True)

    # ---- Run 2: WITHOUT subsidised routes ----
    results_without = integrate_algorithms(use_subsidies=False)

    # ---- Cost comparison ----
    compare_costs(results_with, results_without)

    # ---- Visualisation (show the subsidised scenario) ----
    animate_spinner("Generating visualisations …", duration=1.0)
    visualise_graph(results_with)

    animate_typing_human("\n  ✓ All done. Figures saved to current directory.", delay_base=0.03, color=Colors.LIGHT_GREEN + Colors.BOLD)


# ======================================================================
# Entry point
# ======================================================================
if __name__ == "__main__":
    main()
