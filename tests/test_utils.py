import os
import unittest
import networkx as nx
import pandas as pd
from src.pygraphprofiler.utils.scc import assign_scc
from src.pygraphprofiler.utils.plot import _draw_graph_to_file, _set_node_sizes, _set_edge_labels, _set_node_labels, _set_graph_layout
from src.pygraphprofiler.utils.graph import _add_graph_edges, _add_graph_nodes
from src.pygraphprofiler.profiler import Profiler

class TestUtils(unittest.TestCase):

    def setUp(self):
        profiling_data = {
            'task': ['A', 'B', 'C', 'D', 'E'],
            'parent_task': [None, 'A', 'B', None, 'D'],
            'start_time': [0, 1, 3, 5, 6],
            'end_time': [2, 4, 6, 7, 9]
        }
        self.weight_node_on = 'total_exec_time'
        
        self.graph = Profiler._to_graph(profiling_data)
        self.task_df = pd.DataFrame(profiling_data)

    def test_assign_scc(self):
        sccs = list(nx.strongly_connected_components(self.graph))
        scc_ids = {node: i for i, scc in enumerate(sccs) for node in scc}
        result = assign_scc(self.graph)
        self.assertEqual(result.nodes['A']['scc_id'], scc_ids['A'])
        self.assertEqual(result.nodes['B']['scc_id'], scc_ids['B'])
        self.assertEqual(result.nodes['C']['scc_id'], scc_ids['C'])
        self.assertEqual(result.nodes['D']['scc_id'], scc_ids['D'])
        self.assertEqual(result.nodes['E']['scc_id'], scc_ids['E'])

    def test_draw_graph_to_file(self):
        pos = nx.spring_layout(self.graph)
        node_labels = {'A': 'Node A', 'B': 'Node B', 'C': 'Node C', 'D': 'Node D', 'E': 'Node E'}
        edge_labels = {('A', 'B'): '1', ('B', 'C'): '2', ('C', 'A'): '3', ('D', 'E'): '4'}
        node_sizes = [3, 9, 9, 3, 10]
        _draw_graph_to_file('test.png', self.graph, pos, node_labels, edge_labels, node_sizes, True)
        os.remove('test.png')

    def test_add_graph_edges(self):
        result = _add_graph_edges(self.task_df, self.graph)
        self.assertEqual(result.number_of_edges(), 3)
    
    def test_add_graph_nodes(self):
        result = _add_graph_edges(self.task_df, self.graph)
        self.assertEqual(result.number_of_nodes(), 5)
