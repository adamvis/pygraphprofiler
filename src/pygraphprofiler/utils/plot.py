import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
from .scc import assign_scc


def _draw_graph_to_file(filename: str, graph: nx.Graph, pos: nx.nx_agraph.graphviz_layout, node_labels: dict, edge_labels: dict, node_sizes: dict,  color_nodes: bool = False):
    
    if color_nodes:
        graph = assign_scc(graph)
        node_colors = [node['color'] for node in graph.nodes.values()]
    else:
        node_colors = ['lightblue' for node in graph.nodes.values()]
    
    nx.draw_networkx(graph, pos, labels=node_labels, with_labels=True, font_size=10, node_size=node_sizes, node_color=node_colors)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10, label_pos=0.5)
    
    plt.savefig(filename, format='png', dpi=300, bbox_inches='tight')
    plt.close()



def _set_node_sizes(weight_node_on: str, graph: nx.Graph):
    node_sizes = None
    if weight_node_on:
        values = [node.get(weight_node_on, 1)
                for node in graph.nodes.values()]
        norm = mpl.colors.Normalize(vmin=min(values), vmax=max(values))
        cmap = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.Blues_r)
        node_sizes = [1000 * cmap.to_rgba(val)[0] for val in values]
    return node_sizes


def _set_edge_labels(graph: nx.Graph):
    edge_labels = {(u, v): graph.edges[u, v]['calls']
                for (u, v) in graph.edges}
    return edge_labels


def _set_node_labels(weight_node_on: str, graph: nx.Graph):
    node_labels = {}
    for node in graph.nodes:
        weight_value = graph.nodes[node].get(weight_node_on, 0)
        if weight_node_on == 'count':
            node_labels[node] = f"{node}\n{weight_value}"
        else:
            node_labels[node] = f"{node}\n{weight_value:.2f}s"
    return node_labels


def _set_graph_layout(graph: nx.Graph):
    pos = nx.nx_agraph.graphviz_layout(graph, prog='dot')
    return pos
