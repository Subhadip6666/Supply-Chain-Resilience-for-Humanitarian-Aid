from config import INF, NUM_NODES, SHORT_NAMES
import sys
import os

# Add parent directory to sys.path so we can import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ui import print_color, Colors, print_slow, animate_typing_human

def hamiltonian_cycle(cost_matrix):
    V = NUM_NODES
    best_cost = INF
    best_path = None

    current_path = [0]
    visited = [False] * V
    visited[0] = True

    def backtrack(current_node, current_cost, depth):
        nonlocal best_cost, best_path

        if depth == V:
            return_cost = cost_matrix[current_node][0]
            if return_cost < INF:
                total = current_cost + return_cost
                if total < best_cost:
                    best_cost = total
                    best_path = current_path[:] + [0]
            return

        for next_node in range(V):
            if visited[next_node]:
                continue
            edge_cost = cost_matrix[current_node][next_node]
            if edge_cost >= INF:
                continue

            new_cost = current_cost + edge_cost

            if new_cost >= best_cost:
                continue

            visited[next_node] = True
            current_path.append(next_node)
            backtrack(next_node, new_cost, depth + 1)
            current_path.pop()
            visited[next_node] = False

    backtrack(0, 0, 1)
    return best_path, best_cost

def print_hamiltonian_results(best_path, best_cost):
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
