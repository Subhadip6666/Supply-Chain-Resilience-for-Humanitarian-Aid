import sys
from utils import integrate_algorithms, compare_costs, visualise_graph
from utils import print_slow, print_color, animate_spinner, animate_progress_bar, animate_typing_human, Colors

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

    animate_progress_bar("Booting Up Subsystems", duration=1.2, length=25, color=Colors.LIGHT_BLUE)
    print()

    # ---- Run 1: WITH subsidised (negative-cost) routes ----
    results_with = integrate_algorithms(use_subsidies=True)

    # ---- Run 2: WITHOUT subsidised routes ----
    results_without = integrate_algorithms(use_subsidies=False)

    # ---- Cost comparison ----
    compare_costs(results_with, results_without)

    # ---- Visualisation (show the subsidised scenario) ----
    animate_spinner("Generating visualisations …", duration=2.0)
    visualise_graph(results_with)

    animate_typing_human("\n  ✓ All done. Figures saved to current directory.", delay_base=0.03, color=Colors.LIGHT_GREEN + Colors.BOLD)

if __name__ == "__main__":
    main()
