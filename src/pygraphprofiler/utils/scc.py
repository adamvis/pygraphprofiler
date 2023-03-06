import random
import networkx as nx

def assign_scc(G):
    # Run Kosaraju's algorithm to find strongly connected components
    sccs = list(nx.strongly_connected_components(G))

    # Assign a unique ID to each SCC
    scc_ids = {node: i for i, scc in enumerate(sccs) for node in scc}

    # Generate a color map for the SCCs
    colors = ["lightblue", "red", "green", "orange", "purple", "pink", "yellow", "grey", "brown", "blue"]
    color_map = {i: colors[i % len(colors)] for i in range(len(sccs))}

    # Assign a color to each node based on its SCC ID
    node_colors = {node: color_map[scc_ids[node]] for node in G.nodes()}

    # Add SCC ID and node color as attributes to each node
    for node in G.nodes():
        G.nodes[node]['scc_id'] = scc_ids[node]
        G.nodes[node]['color'] = node_colors[node]

    return G
