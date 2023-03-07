import subprocess
from setuptools import setup, find_packages

# Install graphviz package using apt-get
subprocess.run(['apt-get', 'update'])
subprocess.run(['apt-get', 'install', '-y', 'graphviz'])
subprocess.run(['apt-get', 'install', '-y', 'libgraphviz-dev'])

# Get the long description from the README.md file
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pygraphprofiler',
    version='0.1.9',
    description='A Python package for profiling functions.',
    author='Adam Viscusi',
    author_email='adam.viscusi@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adamvis/pygraphprofiler",
    install_requires=[
        'networkx>=3.0',
        'pandas>=1.4.0',
        'pygraphviz>=1.10',
        'matplotlib>=3.5.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
