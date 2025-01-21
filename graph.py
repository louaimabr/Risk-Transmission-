# graph.py
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def graph():
    """
    Reads 'significant_results.csv', builds a directed graph with F-statistics
    as edge weights, and computes 'SDI' (sum of incoming weights) and 'SDO'
    (sum of outgoing weights) for each node. Prints ranks and shows a network plot.
    """
    # Load significant edges
    df = pd.read_csv("significant_results.csv")
    if df.empty:
        print("No significant causality results found. The network will be empty.")
        return

    G = nx.DiGraph()

    # We'll keep a dict for summing SDO/SDI
    metrics = {}

    for _, row in df.iterrows():
        source = row["Source"]
        target = row["Target"]
        f_stat = row["F-statistic"]
        lag = row["Lag"]

        # Add edge to the graph
        G.add_edge(source, target, weight=f_stat, lag=lag)

        # Initialize if not in metrics
        if source not in metrics:
            metrics[source] = {"SDO": 0.0, "SDI": 0.0}
        if target not in metrics:
            metrics[target] = {"SDO": 0.0, "SDI": 0.0}

        # Summation approach
        metrics[source]["SDO"] += f_stat
        metrics[target]["SDI"] += f_stat

    # Sort by SDI (absorbers)
    sorted_absorbers = sorted(metrics.items(), key=lambda x: x[1]["SDI"], reverse=True)
    # Sort by SDO (transmitters)
    sorted_transmitters = sorted(metrics.items(), key=lambda x: x[1]["SDO"], reverse=True)

    print("\nRank: Countries with Most Absorbing (SDI)")
    print("//")
    for country, vals in sorted_absorbers:
        print(f"{country}: SDI = {vals['SDI']:.2f}")
    print("//")

    print("\nRank: Countries with Most Transmitting (SDO)")
    print("//")
    for country, vals in sorted_transmitters:
        print(f"{country}: SDO = {vals['SDO']:.2f}")
    print("//")

    # Visualization
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color="lightblue")
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
    edges = nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray')

    # Edge labels
    edge_labels = {}
    for (u, v, d) in G.edges(data=True):
        edge_labels[(u, v)] = f"{d['weight']:.2f} (Lag {d['lag']})"

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Granger Causality Network")
    plt.axis("off")
    plt.show()
    plt.close()
