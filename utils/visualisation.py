import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from config import NUM_NODES, SHORT_NAMES

def visualise_graph(results):
    if results is None:
        print("  Skipping visualisation (no valid results).")
        return

    adj = results["adj"]
    edges = results["edges"]
    pred = results["pred"]
    ham_path = results["ham_path"]
    ham_cost = results["ham_cost"]

    G = nx.Graph()
    for i in range(NUM_NODES):
        G.add_node(i, label=SHORT_NAMES[i])

    added = set()
    for u, v, w in edges:
        key = (min(u, v), max(u, v))
        if key not in added:
            G.add_edge(u, v, weight=w)
            added.add(key)

    pos = nx.spring_layout(G, seed=42, k=2.5)

    node_colors = []
    for n in G.nodes():
        if n == 0:
            node_colors.append("#2ecc71")
        elif n in (1, 2, 3):
            node_colors.append("#f39c12")
        else:
            node_colors.append("#85c1e9")

    labels = {n: SHORT_NAMES[n] for n in G.nodes()}

    fig1, ax1 = plt.subplots(1, 1, figsize=(14, 10))
    ax1.set_title("Figure 1 — Humanitarian Aid Supply Chain Network", fontsize=15, fontweight='bold')

    nx.draw_networkx_nodes(G, pos, ax=ax1, node_color=node_colors, node_size=700, edgecolors='black', linewidths=1.2)
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax1, font_size=7, font_weight='bold')

    normal_edges = []
    subsidy_edges = []
    for u, v, d in G.edges(data=True):
        key = (min(u, v), max(u, v))
        if key in {(5, 6), (8, 9)}:
            subsidy_edges.append((u, v))
        else:
            normal_edges.append((u, v))

    nx.draw_networkx_edges(G, pos, edgelist=normal_edges, ax=ax1, edge_color='#3498db', width=2)
    nx.draw_networkx_edges(G, pos, edgelist=subsidy_edges, ax=ax1, edge_color='red', width=3, style='dashed')

    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax1, font_size=8)

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
    fig1.savefig("Graph_Image/figure1_full_graph.png", dpi=150, bbox_inches='tight')
    print("  ✓ Saved Graph_Image/figure1_full_graph.png")

    fig2, ax2 = plt.subplots(1, 1, figsize=(14, 10))
    ax2.set_title("Figure 2 — Shortest Path Tree & Hamiltonian Circuit", fontsize=15, fontweight='bold')

    nx.draw_networkx_nodes(G, pos, ax=ax2, node_color=node_colors, node_size=700, edgecolors='black', linewidths=1.2)
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax2, font_size=7, font_weight='bold')
    nx.draw_networkx_edges(G, pos, ax=ax2, edge_color='#d5dbdb', width=1, alpha=0.5)

    bf_tree_edges = []
    for node in range(1, NUM_NODES):
        p = pred[node]
        if p != -1:
            bf_tree_edges.append((p, node))

    nx.draw_networkx_edges(G, pos, edgelist=bf_tree_edges, ax=ax2, edge_color='#f1c40f', width=4, alpha=0.8)

    if ham_path is not None:
        DG = nx.DiGraph()
        direct_ham_edges = []
        indirect_ham_edges = []
        for i in range(len(ham_path) - 1):
            u, v = ham_path[i], ham_path[i + 1]
            DG.add_edge(u, v)
            if G.has_edge(u, v):
                direct_ham_edges.append((u, v))
            else:
                indirect_ham_edges.append((u, v))

        if direct_ham_edges:
            nx.draw_networkx_edges(DG, pos, edgelist=direct_ham_edges, ax=ax2,
                                   edge_color='red', width=2.5, arrows=True,
                                   arrowsize=20, arrowstyle='-|>', style='solid',
                                   connectionstyle='arc3,rad=0.1')
        if indirect_ham_edges:
            nx.draw_networkx_edges(DG, pos, edgelist=indirect_ham_edges, ax=ax2,
                                   edge_color='red', width=2.5, arrows=True,
                                   arrowsize=20, arrowstyle='-|>', style='dashed',
                                   connectionstyle='arc3,rad=0.1')

        # Text box with total cost
        textstr = f"Hamiltonian Circuit Cost: {ham_cost} units"
        props = dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='red', alpha=0.9)
        ax2.text(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=11, verticalalignment='top', bbox=props)
    else:
        # Add a visible warning text box on Figure 2 saying "No Hamiltonian Circuit Found" in red if ham_path is None
        textstr = "No Hamiltonian Circuit Found"
        props = dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='red', alpha=0.9)
        ax2.text(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=11, color='red', verticalalignment='top', bbox=props)

    legend_handles2 = [
        Line2D([0], [0], color='#f1c40f', lw=4, label='Bellman-Ford Shortest Path Tree'),
        Line2D([0], [0], color='red', lw=2.5, linestyle='solid', label='Hamiltonian Circuit (Direct Route)'),
        Line2D([0], [0], color='red', lw=2.5, linestyle='dashed', label='Hamiltonian Circuit (Indirect Path)'),
    ]
    ax2.legend(handles=legend_handles2, loc='lower left', fontsize=9)
    ax2.axis('off')
    fig2.tight_layout()
    fig2.savefig("Graph_Image/figure2_results.png", dpi=150, bbox_inches='tight')
    print("  ✓ Saved Graph_Image/figure2_results.png")

    # plt.close('all')
    try:
        plt.show()
    except Exception:
        pass
