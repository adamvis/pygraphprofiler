import json
import time
import functools
import inspect
import networkx as nx
import time
import pandas as pd

from .utils.graph import _add_graph_edges, _add_graph_nodes
from .utils.plot import _draw_graph_to_file, _set_edge_labels, _set_graph_layout, _set_node_labels, _set_node_sizes


class Profiler:

    def __init__(self, name='__main__'):
        """The __init__ method is the constructor of the Profiler class, initializing the instance variables of a new Profiler object.

        Args:
        None

        Attributes:
        _func_names_list (list): A list of function names monitored by the profiler.
        _parent_func_list (list): A list of parent function names of each monitored function.
        _start_time_list (list): A list of start times of each monitored function.
        _end_time_list (list): A list of end times of each monitored function.

        Returns:
        Profiler instance
        """
        self._func_names_list = []
        self._parent_func_list = []
        self._start_time_list = []
        self._end_time_list = []

    def monitor(self, func):
        """The monitor function is a decorator that can be used to monitor a Python function and record its execution time, along with the function name and the parent function name. The decorated function is returned by the wrapper function wrapper, which records the start time of the function, runs the original function, records the end time of the function, and adds the relevant data to the Profiler instance's _func_names_list, _parent_func_list, _start_time_list, and _end_time_list.

        Args:
        func (function): The function to be monitored.

        Returns:
        wrapper function: A wrapped function that will record the function name, parent function name, start time, and end time of the decorated function when it is executed.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            self._func_names_list.append(func.__name__)
            self._parent_func_list.append(inspect.stack()[1].function)
            self._start_time_list.append(start_time)
            self._end_time_list.append(end_time)
            return result
        return wrapper

    def to_graph(self):
        """The to_graph method converts the profiling data of the Profiler instance into a directed graph and returns it.

        Args:
        None

        Returns:
        graph (networkx.DiGraph): A directed graph representing the execution order of t.
        """
        task_df = self.to_dataframe()
        graph = nx.DiGraph()
        graph = _add_graph_nodes(task_df, graph)
        graph = _add_graph_edges(task_df, graph)
        return graph

    def to_dataframe(self):
        """The to_dataframe method creates a pandas DataFrame object from the monitored function data stored in the Profiler object.

        Args:
        None

        Returns:
        task_df (pandas DataFrame): A DataFrame object containing the monitored function data. Each row of the DataFrame represents a single function call and contains columns for the function name, its parent function name, the start time of the function call, and the end time of the function call.
        """
        task_df = pd.DataFrame({
            'task': self._func_names_list,
            'parent_task': self._parent_func_list,
            'start_time': self._start_time_list,
            'end_time': self._end_time_list
        })
        return task_df

    def plot_graph(self, filename, weight_node_on: str = 'count'):
        """The plot_graph function generates a visualization of the function call graph created by the profiler and saves it to a file.

        Args:
        filename (str): The name of the file to save the plot to.
        weight_node_on (str, optional): The column name of the dataframe that contains the weights of nodes, which are used to determine the size of the nodes in the plot (available options: 'count', 'total_exec_time', 'average_exec_time'). If not provided, defaults to 'count'.

        Returns:
        None. The plot is saved to the file specified by filename.
        """
        graph = self.to_graph()
        pos = _set_graph_layout(graph)
        node_labels = _set_node_labels(weight_node_on, graph)
        edge_labels = _set_edge_labels(graph)
        node_sizes = _set_node_sizes(weight_node_on, graph)
        _draw_graph_to_file(filename, graph, pos,
                            node_labels, edge_labels, node_sizes)

    def to_json(self):
        """
        Convert the information in the TaskMonitor object to a JSON string.

        Args:
        None

        Returns:
            str: A JSON-encoded string representing the contents of the TaskMonitor object.
        """
        data = {
            '_func_names_list': self._func_names_list,
            '_parent_func_list': self._parent_func_list,
            '_start_time_list': self._start_time_list,
            '_end_time_list': self._end_time_list,
        }
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str):
        """
        Returns a new instance of the Profiler class with the data from the given JSON string.

        :param json_str: A JSON string containing the profiler data.
        :type json_str: str
        :return: A new instance of the Profiler class.
        :rtype: Profiler
        """
        data = json.loads(json_str)
        profiler = cls()
        profiler._func_names_list = data['_func_names_list']
        profiler._parent_func_list = data['_parent_func_list']
        profiler._start_time_list = data['_start_time_list']
        profiler._end_time_list = data['_end_time_list']
        return profiler


def merge_profiler_instances(*profilers):
    """Merge multiple instances of the Profiler class into a single instance.

    Args:
        *profilers: one or more instances of the Profiler class.

    Returns:
        A new instance of the Profiler class with all of the function calls
        and timing data from the input profilers.

    Example:
        profiler1 = Profiler()
        my_func1(profiler1)
        my_func2(profiler1)

        profiler2 = Profiler()
        my_func3(profiler2)

        merged_profiler = merge_profiler_instances(profiler1, profiler2)

    """
    merged_profiler = Profiler()
    for profiler in profilers:
        merged_profiler._func_names_list += profiler._func_names_list
        merged_profiler._parent_func_list += profiler._parent_func_list
        merged_profiler._start_time_list += profiler._start_time_list
        merged_profiler._end_time_list += profiler._end_time_list
    return merged_profiler

