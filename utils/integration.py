from config import INF, NUM_NODES
from graph import build_graph
from algorithms import bellman_ford, print_bellman_ford_results, hamiltonian_cycle, print_hamiltonian_results
from .ui import print_color, Colors, print_slow, animate_typing_human

def build_complete_cost_matrix(adj, edges):
    cost_matrix = [[INF] * NUM_NODES for _ in range(NUM_NODES)]
    all_preds = []

    for src in range(NUM_NODES):
        dist, pred, neg = bellman_ford(adj, edges, source=src)
        cost_matrix[src] = dist
        all_preds.append(pred)

    return cost_matrix, all_preds

def integrate_algorithms(use_subsidies=True):
    label = "WITH" if use_subsidies else "WITHOUT"
    print_color("\n" + "#" * 60, Colors.LIGHT_BLUE)
    print_color(f"  RUNNING SYSTEM — {label} SUBSIDISED ROUTES", Colors.BOLD + Colors.LIGHT_BLUE)
    print_color("#" * 60, Colors.LIGHT_BLUE)

    adj, edges = build_graph(use_subsidies=use_subsidies)
    dist, pred, has_neg_cycle = bellman_ford(adj, edges, source=0)

    if has_neg_cycle:
        print_color("\n  ⚠⚠⚠  WARNING: Negative cycle detected in the graph!", Colors.LIGHT_RED + Colors.BOLD)
        print_color("  Shortest paths are undefined. Aborting this run.", Colors.LIGHT_RED)
        return None

    print_bellman_ford_results(dist, pred)
    cost_matrix, all_preds = build_complete_cost_matrix(adj, edges)
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

def compare_costs(results_with, results_without):
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
