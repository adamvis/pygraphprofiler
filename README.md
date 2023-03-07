
<img src="assets/logo_banner.png" width="100%">


# PyGraphProfiler

Unleash the power of PyGraphProfiler - the ultimate Python class for function profiling and execution graph visualization! With PyGraphProfiler, you can effortlessly monitor function calls, create a stunning graph showcasing their execution order, and easily convert the profiling data to a Pandas DataFrame. Say goodbye to the complexity of profiling Python functions, and hello to the ease and efficiency of Profiler!

## Installation

You can install the profiler package using pip:

    pip install pygraphprofiler

Note that this package requires the following dependencies:

    networkx
    matplotlib
    pandas

These dependencies will be automatically installed by pip during the installation process.

## Usage

Here's an example of how to use the Profiler class:

    from pygraphprofiler import Profiler, merge_profiler_instances

    profiler = Profiler()

    @profiler.monitor
    def foo():
        pass

    @profiler.monitor
    def bar():
        pass

    foo()
    bar()

    profiler.plot_graph("graph.png")

This code creates a Profiler object, defines two functions foo and bar, monitors their execution using the monitor decorator, calls foo and bar, and then plots the execution graph to a file named "graph.png". The size of the dots depends on either 'count', 'total_exec_time', 'average_exec_time' that can be set in the optional parameter 'weight_node_on' inside 'plot_graph'. Default is 'count'.

The Profiler class also provides methods to convert the profiling data to a Pandas DataFrame and to serialize it to JSON:

    dataframe = profiler.to_dataframe()
    json_str = profiler.to_json()

You can also merge two instances of Profiler directly:

    merged_profiler = merge_profiler_instances(profiler1, profiler2)

Or merge two instances of Profiler directly:

    profiler1 = Profiler()
    foo()
    json_str1 = profiler1.to_json()

    profiler2 = Profiler()
    bar()
    json_str2 = profiler2.to_json()

    merged_profiler = merge_profiler_instances(profiler1, profiler2)
    merged_dataframe = merged_profiler.to_dataframe()
    merged_json_str = merged_profiler.to_json()


This code creates two instances of Profiler, profiles two functions foo and bar separately using each profiler, converts the profiling data to JSON, merges the two profilers, converts the merged profiling data to a Pandas DataFrame and JSON.

In addition to the class-based profiling provided by the Profiler class, PyGraphProfiler also includes a module-level profiling function monitor, which can be used to profile functions without creating a Profiler object. Here's an example:

    from pygraphprofiler import monitor, plot_graph

    @monitor
    def foo():
        pass

    @monitor
    def bar():
        pass

    foo()
    bar()

    plot_graph("module_dependencies.png")


In this cases profiling logs will be shared across the module.


## Future Changes

- Improve existing visualizations and add new ones: The current version of the Profiler class provides basic visualization options. Future updates may include more advanced visualization techniques to help users better understand the profiling data. This may include interactive visualizations, 3D plots, or other custom visualization techniques.

- Add streaming data monitoring: Currently, the Profiler class only works with data that is stored in memory. Future updates may include the ability to monitor streaming data in real-time, allowing users to visualize the profiling data as it is generated. This would be useful in scenarios where the user needs to monitor a continuously running system or application.