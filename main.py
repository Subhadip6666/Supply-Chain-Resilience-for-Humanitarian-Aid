from utils import integrate_algorithms, compare_costs, visualise_graph

def main():
    print("╔" + "═" * 58 + "╗")
    print("║  HUMANITARIAN AID SUPPLY CHAIN OPTIMISATION SYSTEM       ║")
    print("║  Algorithms: Bellman-Ford  ·  Hamiltonian Cycle          ║")
    print("╚" + "═" * 58 + "╝")

    # ---- Run 1: WITH subsidised (negative-cost) routes ----
    results_with = integrate_algorithms(use_subsidies=True)

    # ---- Run 2: WITHOUT subsidised routes ----
    results_without = integrate_algorithms(use_subsidies=False)

    # ---- Cost comparison ----
    compare_costs(results_with, results_without)

    # ---- Visualisation (show the subsidised scenario) ----
    print("\n  Generating visualisations …")
    visualise_graph(results_with)

    print("\n  ✓ All done. Figures saved to current directory.")

if __name__ == "__main__":
    main()
