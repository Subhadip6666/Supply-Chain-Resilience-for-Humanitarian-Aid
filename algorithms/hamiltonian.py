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

    # ---- Hamiltonian Result Verification ----
    verification_status = "FAILED"
    verification_reason = "No Hamiltonian circuit found"

    if best_path is not None:
        if len(best_path) != 13:
            verification_status = "FAILED"
            verification_reason = f"Circuit path length is {len(best_path)}, expected 13"
        elif best_path[0] != 0 or best_path[-1] != 0:
            verification_status = "FAILED"
            verification_reason = f"Circuit must start and end at node 0 (starts with {best_path[0]}, ends with {best_path[-1]})"
        else:
            unique_nodes = set(best_path[:-1])
            if len(unique_nodes) != 12 or any(n < 0 or n >= 12 for n in unique_nodes):
                verification_status = "FAILED"
                verification_reason = "Not all 12 nodes are visited exactly once"
            else:
                calculated_cost = 0
                cost_mismatch = False
                for i in range(len(best_path) - 1):
                    u, v = best_path[i], best_path[i + 1]
                    c = cost_matrix[u][v]
                    if c == INF:
                        cost_mismatch = True
                        verification_reason = f"Infinite cost step found between node {u} and {v}"
                        break
                    calculated_cost += c
                
                if cost_mismatch:
                    verification_status = "FAILED"
                elif abs(calculated_cost - best_cost) > 1e-6:
                    verification_status = "FAILED"
                    verification_reason = f"Calculated path cost ({calculated_cost}) does not match reported best_cost ({best_cost})"
                else:
                    verification_status = "VERIFIED"
                    verification_reason = "All 12 nodes visited exactly once; starts and ends at node 0; cost matches sum along path"

    hamiltonian_cycle.verification_status = verification_status
    hamiltonian_cycle.verification_reason = verification_reason

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
        
        status = getattr(hamiltonian_cycle, 'verification_status', None)
        reason = getattr(hamiltonian_cycle, 'verification_reason', None)
        if status == "VERIFIED":
            animate_typing_human(f"  Verification: VERIFIED ({reason})\n", delay_base=0.015, color=Colors.LIGHT_GREEN)
        else:
            animate_typing_human(f"  Verification: FAILED ({reason if reason else 'Unknown issue'})\n", delay_base=0.015, color=Colors.LIGHT_RED)

    print_color("=" * 60, Colors.LIGHT_PURPLE)
