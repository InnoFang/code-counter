.PHONY:
test:
	python -m unittest discover -s tests -p "test_*.py"

setup:
	python setup.py install

check:
	python setup.py check

build:check
	python setup.py sdist bdist_wheel

install:build
	pip install dist/*.whl

upload:build
	twine upload dist/*

uninstall:
	echo y | pip uninstall code-counter

clean:
	rm -rf build code_counter.* dist
