import json
import os
import unittest
import networkx as nx

import pandas as pd
from src.pygraphprofiler import monitor, plot_graph, to_dataframe, to_graph, to_json


class TestModuleLevel(unittest.TestCase):

    def test_to_dataframe(self):

        @monitor
        def test_func():
            pass

        test_func()

        df = to_dataframe()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)

    def test_to_json_from_json(self):

        @monitor
        def test_func():
            pass

        test_func()

        json_string = to_json()
        self.assertIsInstance(json_string, str)
        data = json.loads(json_string)
        self.assertIn('task', data)
        self.assertIn('parent_task', data)
        self.assertIn('start_time', data)
        self.assertIn('end_time', data)

    def test_to_graph(self):

        @monitor
        def test_func():
            test_func_sub_a()
            test_func_sub_b()
        
        @monitor
        def test_func_sub_a():
            pass
        
        @monitor
        def test_func_sub_b():
            test_func_sub_a()

        test_func()
        graph = to_graph()
        self.assertIsInstance(graph, nx.DiGraph)
        self.assertGreater(len(graph.nodes), 0)
        self.assertGreater(len(graph.edges), 0)

    def test_plot_graph(self):

        @monitor
        def func1():
            pass

        @monitor
        def func2():
            func1()

        @monitor
        def func3():
            func1()
            func2()

        func3()
        filename = "test_plot_graph.png"
        plot_graph(filename, weight_node_on='count')

        self.assertTrue(os.path.exists(filename))
        os.remove(filename)


if __name__ == '__main__':
    unittest.main()
