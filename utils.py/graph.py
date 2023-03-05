import networkx as nx
import matplotlib.dates as mdates
import pandas as pd


date_format = mdates.DateFormatter('%m/%d/%Y %H:%M')


def _add_graph_edges(task_df: pd.DataFrame, graph: nx.Graph):
    edge_counts = {}
    for index, row in task_df.iterrows():
        node = row['task']
        parent = row['parent_task']
        if parent:
            if (parent, node) not in edge_counts:
                edge_counts[(parent, node)] = 1
            else:
                edge_counts[(parent, node)] += 1
            graph.add_edge(parent, node, calls=edge_counts[(parent, node)])

    return graph


def _add_graph_nodes(task_df: pd.DataFrame, graph: nx.Graph):
    total_exec_time_dict = {}
    count_dict = {}
    for index, row in task_df.iterrows():
        node = row['task']
        start_time = row['start_time']
        end_time = row['end_time']
        exec_time = end_time - start_time
        if node not in total_exec_time_dict:
            total_exec_time_dict[node] = exec_time
            count_dict[node] = 1
        else:
            total_exec_time_dict[node] += exec_time
            count_dict[node] += 1
        graph.add_node(
            node,
            total_exec_time=total_exec_time_dict[node],
            count=count_dict[node],
            average_exec_time=total_exec_time_dict[node]/count_dict[node]
        )

    return graph
