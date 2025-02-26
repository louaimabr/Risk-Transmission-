import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def graph():
    df = pd.read_csv("significant_results.csv")
    if df.empty:
        print("Aucun résultat de causalité significatif n'a été trouvé. Le graphe sera vide.")
        return

    # Filtre : garder uniquement les liens dont la F-statistic est > 100
    df = df[df["F-statistic"] > 150]
    if df.empty:
        print("Après filtrage (F-statistic > 150), plus aucun lien n'est significatif.")
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

    # Classements
    sorted_absorbers = sorted(metrics.items(), key=lambda x: x[1]["SDI"], reverse=True)
    sorted_transmitters = sorted(metrics.items(), key=lambda x: x[1]["SDO"], reverse=True)

    print("\nPays les plus 'absorbants' (SDI):")
    for country, vals in sorted_absorbers:
        print(f"{country}: SDI = {vals['SDI']:.2f}")

    print("\nPays les plus 'transmetteurs' (SDO):")
    for country, vals in sorted_transmitters:
        print(f"{country}: SDO = {vals['SDO']:.2f}")

    # Layout : spring_layout
    pos = nx.planar_layout(G)

    plt.figure(figsize=(12, 7))

    # Dessin des nœuds
    nx.draw_networkx_nodes(
        G, pos,
        node_size=2000,  # Ajustez selon vos préférences
        node_color="lightblue"
    )

    # Labels des nœuds
    nx.draw_networkx_labels(
        G, pos,
        font_size=10,
        font_weight="bold"
    )

    # Dessin des arêtes (lignes droites) avec flèches
    nx.draw_networkx_edges(
        G, pos,
        arrowstyle='-|>',  # ou '->'
        arrows=True,
        arrowsize=20,
        edge_color='gray',
        min_source_margin=15,  # éloigne la flèche du nœud source
        min_target_margin=15   # éloigne la flèche du nœud cible
    )

    # Labels des arêtes : F-stat et lag
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

    plt.title("Réseau de Causalité de Granger (F-stat > 100)")
    plt.axis("off")
    plt.tight_layout()
    plt.show()
    plt.close()
