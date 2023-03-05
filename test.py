import unittest
import time
from src.pygraphprofiler import Profiler, merge_profiler_instances

class TestProfiler(unittest.TestCase):

    def test_monitor(self):
        profiler = Profiler()

        @profiler.monitor
        def test_func():
            time.sleep(0.5)

        test_func()

        self.assertEqual(len(profiler._func_names_list), 1)
        self.assertEqual(len(profiler._parent_func_list), 1)
        self.assertEqual(len(profiler._start_time_list), 1)
        self.assertEqual(len(profiler._end_time_list), 1)

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

        self.assertEqual(len(merged_profiler._func_names_list), 2)
        self.assertEqual(len(merged_profiler._parent_func_list), 2)
        self.assertEqual(len(merged_profiler._start_time_list), 2)
        self.assertEqual(len(merged_profiler._end_time_list), 2)

    def test_to_json_from_json(self):
        profiler = Profiler()

        @profiler.monitor
        def test_func():
            time.sleep(0.5)

        test_func()

        json_str = profiler.to_json()
        new_profiler = Profiler.from_json(json_str)

        self.assertEqual(len(new_profiler._func_names_list), 1)
        self.assertEqual(len(new_profiler._parent_func_list), 1)
        self.assertEqual(len(new_profiler._start_time_list), 1)
        self.assertEqual(len(new_profiler._end_time_list), 1)

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


if __name__ == '__main__':
    unittest.main()
