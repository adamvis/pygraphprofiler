.PHONY: install test clean

PACKAGE_NAME = pygraphprofiler

install:
	python setup.py install

test:
	python -m unittest discover -v

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete

dist: clean
	python setup.py sdist bdist_wheel

publish: dist
	twine upload dist/*

