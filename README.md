# Humanitarian Aid Supply Chain Optimisation System

This project is a Semester 4 university project (Course: CS302) that models a post-disaster humanitarian aid supply chain. It calculates the most cost-effective way to deliver relief supplies from a Central Warehouse (HQ) to various regional depots and villages using two graph theory algorithms.

## Algorithms Used

1. **Bellman-Ford Algorithm**: 
   - Calculates the shortest path from the Central Warehouse to all other locations.
   - Specifically chosen because some routes are subsidized by the government and NGOs (represented as negative edge weights).
   - The algorithm is implemented manually with parent-aware relaxation to correctly handle undirected negative edges without falling into trivial negative cycles.

2. **Hamiltonian Cycle (Backtracking with Pruning)**:
   - Finds a single, continuous delivery circuit that visits every location exactly once and returns to HQ.
   - Uses the shortest paths computed by Bellman-Ford as the base costs.
   - Includes a pruning optimization: if a partial circuit's cost exceeds the current best-known circuit, it abandons that path early to save computation time.

## Project Structure

```text
SEM 4 Project/
│
├── main.py                 # The main entry point to run the program
├── config.py               # Constants, node names, and subsidised edges definitions
├── graph.py                # Graph adjacency matrix building logic
├── requirements.txt        # Python dependencies
│
├── algorithms/
│   ├── bellman_ford.py     # Shortest paths and negative cycle logic
│   └── hamiltonian.py      # Backtracking cycle solver
│
└── utils/
    ├── integration.py      # Combines algorithms and computes SDG17 savings
    └── visualisation.py    # NetworkX & Matplotlib plotting
```

## How to Run

1. **Set up a Virtual Environment (Optional but recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Program:**
   ```bash
   python3 main.py
   ```

## Output

The program will:
- Print the shortest paths and costs to all locations.
- Print the optimal delivery route (Hamiltonian circuit).
- Compare the costs of the delivery route **with** and **without** government/NGO subsidies to demonstrate the real-world financial impact (aligning with **SDG 17 - Partnerships for the Goals**).
- Generate and save two visualizations in the `Graph_Image/` folder:
  - `figure1_full_graph.png`: The complete network.
  - `figure2_results.png`: The shortest path tree and the optimal Hamiltonian circuit.

## Author
**Subhadip Patra** (Course: CS302)
