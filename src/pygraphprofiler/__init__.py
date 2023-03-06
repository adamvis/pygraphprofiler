import json
import time
import functools
import inspect
import networkx as nx
import time
import pandas as pd

from .profiler import Profiler, merge_profiler_instances
from . import utils
from .utils.graph import _add_graph_edges, _add_graph_nodes
from .utils.plot import _draw_graph_to_file, _set_edge_labels, _set_graph_layout, _set_node_labels, _set_node_sizes


# initialize global, in-memory variables
profiling_data = {
    "task" : [],
    "parent_task" : [],
    "start_time" : [],
    "end_time" : [],
}

def monitor(func):
    """The monitor function is a decorator that can be used to monitor a Python function and record its execution time, along with the function name and the parent function name. The decorated function is returned by the wrapper function wrapper, which records the start time of the function, runs the original function, records the end time of the function, and adds the relevant data to the global, in-memory variables _func_names_list, _parent_func_list, _start_time_list, and _end_time_list.

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
        profiling_data["task"].append(func.__name__)
        profiling_data["parent_task"].append(inspect.stack()[1].function)
        profiling_data["start_time"].append(start_time)
        profiling_data["end_time"].append(end_time)
        return result
    return wrapper


def plot_graph(filename, weight_node_on: str = 'count'):
    """The plot_graph function generates a visualization of the function call graph created by the profiler and saves it to a file.

    Args:
    filename (str): The name of the file to save the plot to.
    weight_node_on (str, optional): The column name of the dataframe that contains the weights of nodes, which are used to determine the size of the nodes in the plot (available options: 'count', 'total_exec_time', 'average_exec_time'). If not provided, defaults to 'count'.

    Returns:
    None. The plot is saved to the file specified by filename.
    """
    return Profiler._plot_graph(profiling_data, filename=filename, weight_node_on=weight_node_on)

def to_graph():
    return Profiler._to_graph(profiling_data)

def to_dataframe():
    return Profiler._to_dataframe(profiling_data)
    
def to_json(name=__name__):
    """
    Convert the information to a JSON string.

    Args:
    None

    Returns:
        str: A JSON-encoded string representing the contents of the object.
    """
    return Profiler._to_json(profiling_data)
    
