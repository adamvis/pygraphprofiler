import json
import os
import unittest
import time
import networkx as nx

import pandas as pd
from src.pygraphprofiler import Profiler, merge_profiler_instances, monitor, plot_graph, to_dataframe, to_graph, to_json
from src.pygraphprofiler import profiler as profiler_lib


class TestProfiler(unittest.TestCase):

    def test_monitor(self):
        profiler = Profiler()

        @profiler.monitor
        def test_func():
            time.sleep(0.5)

        test_func()

        self.assertEqual(len(profiler.profiling_data["task"]), 1)
        self.assertEqual(len(profiler.profiling_data["parent_task"]), 1)
        self.assertEqual(len(profiler.profiling_data["start_time"]), 1)
        self.assertEqual(len(profiler.profiling_data["end_time"]), 1)

    def test_merge_profiler_instances(self):
        profiler1 = Profiler()

        @profiler1.monitor
        def test_func1():
            time.sleep(0.5)

        test_func1()

        profiler2 = Profiler()

        @profiler2.monitor
        def test_func2():
            time.sleep(0.5)

        test_func2()

        merged_profiler = merge_profiler_instances(profiler1, profiler2)

        self.assertEqual(len(merged_profiler.profiling_data["task"]), 2)
        self.assertEqual(len(merged_profiler.profiling_data["parent_task"]), 2)
        self.assertEqual(len(merged_profiler.profiling_data["start_time"]), 2)
        self.assertEqual(len(merged_profiler.profiling_data["end_time"]), 2)

    def test_to_json_from_json(self):
        profiler = Profiler()

        @profiler.monitor
        def test_func():
            time.sleep(0.5)

        test_func()

        json_str = profiler.to_json()
        new_profiler = Profiler.from_json(json_str)

        self.assertEqual(len(new_profiler.profiling_data["task"]), 1)
        self.assertEqual(len(new_profiler.profiling_data["parent_task"]), 1)
        self.assertEqual(len(new_profiler.profiling_data["start_time"]), 1)
        self.assertEqual(len(new_profiler.profiling_data["end_time"]), 1)

    def test_to_dataframe(self):
        profiler = Profiler()

        @profiler.monitor
        def test_func():
            time.sleep(0.5)

        test_func()

        df = profiler.to_dataframe()

        self.assertEqual(len(df), 1)
        self.assertIn('task', df.columns)
        self.assertIn('parent_task', df.columns)
        self.assertIn('start_time', df.columns)
        self.assertIn('end_time', df.columns)


class TestMonitor(unittest.TestCase):

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
            pass

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
