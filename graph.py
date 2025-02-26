import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def graph():
    df = pd.read_csv("significant_results.csv")
    if df.empty:
        print("No significant Granger causality results found. The graph will be empty.")
        return

    # Filter: keep only edges with F-statistic > 150
    df = df[df["F-statistic"] > 150]
    if df.empty:
        print("After filtering (F-statistic > 150), no significant links remain.")
        return

    G = nx.DiGraph()
    metrics = {}

    for _, row in df.iterrows():
        source = row["Source"]
        target = row["Target"]
        f_stat = row["F-statistic"]
        lag = row["Lag"]

        G.add_edge(source, target, weight=f_stat, lag=lag)

        if source not in metrics:
            metrics[source] = {"SDO": 0.0, "SDI": 0.0}
        if target not in metrics:
            metrics[target] = {"SDO": 0.0, "SDI": 0.0}

        metrics[source]["SDO"] += f_stat
        metrics[target]["SDI"] += f_stat

    # Rankings
    sorted_absorbers = sorted(metrics.items(), key=lambda x: x[1]["SDI"], reverse=True)
    sorted_transmitters = sorted(metrics.items(), key=lambda x: x[1]["SDO"], reverse=True)

    print("\nMost 'Absorbing' Countries (SDI):")
    for country, vals in sorted_absorbers:
        print(f"{country}: SDI = {vals['SDI']:.2f}")

    print("\nMost 'Transmitting' Countries (SDO):")
    for country, vals in sorted_transmitters:
        print(f"{country}: SDO = {vals['SDO']:.2f}")

    # Layout: planar_layout
    pos = nx.planar_layout(G)

    plt.figure(figsize=(12, 7))

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos,
        node_size=2000,  # Adjust as needed
        node_color="lightblue"
    )

    # Draw node labels
    nx.draw_networkx_labels(
        G, pos,
        font_size=10,
        font_weight="bold"
    )

    # Draw edges (straight lines) with arrows
    nx.draw_networkx_edges(
        G, pos,
        arrowstyle='-|>',  # or '->'
        arrows=True,
        arrowsize=20,
        edge_color='gray',
        min_source_margin=15,  # Moves the arrow away from the source node
        min_target_margin=15   # Moves the arrow away from the target node
    )

    # Edge labels: F-stat and lag
    edge_labels = {
        (u, v): f"{d['weight']:.2f} (Lag {d['lag']})"
        for u, v, d in G.edges(data=True)
    }
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_size=8,
        label_pos=0.5
    )

    plt.title("Granger Causality Network (F-stat > 100)")
    plt.axis("off")
    plt.tight_layout()
    plt.show()
    plt.close()
