from config import INF, NUM_NODES
from graph import build_graph
from algorithms import bellman_ford, print_bellman_ford_results, hamiltonian_cycle, print_hamiltonian_results

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
    print("\n" + "#" * 60)
    print(f"  RUNNING SYSTEM — {label} SUBSIDISED ROUTES")
    print("#" * 60)

    adj, edges = build_graph(use_subsidies=use_subsidies)
    dist, pred, has_neg_cycle = bellman_ford(adj, edges, source=0)

    if has_neg_cycle:
        print("\n  ⚠⚠⚠  WARNING: Negative cycle detected in the graph!")
        print("  Shortest paths are undefined. Aborting this run.")
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
    print("\n" + "=" * 60)
    print("  COST COMPARISON  (SDG 17 — Partnerships for the Goals)")
    print("=" * 60)

    if results_with is None or results_without is None:
        print("  ⚠ Cannot compare — one or both runs failed.")
        return

    cost_with = results_with["ham_cost"]
    cost_without = results_without["ham_cost"]

    if cost_with == INF or cost_without == INF:
        print("  ⚠ Cannot compare — Hamiltonian circuit not found in one/both runs.")
        return

    savings = cost_without - cost_with

    print(f"  Without subsidised routes : {cost_without} units")
    print(f"  With subsidised routes    : {cost_with} units")
    print(f"  Savings through partnerships : {savings} units")
    print()
    if savings > 0:
        pct = (savings / cost_without) * 100
        print(f"  → Government & NGO partnerships reduced delivery cost by {pct:.1f}%")
    elif savings == 0:
        print("  → No cost difference detected.")
    else:
        print("  → Subsidised routes actually increased cost (unusual scenario).")

    print("=" * 60)
