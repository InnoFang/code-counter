VERSION=0.1.0

all:
	python setup.py bdist_wheel

.PHONY:

install:
	pip install dist/code_counter-${VERSION}-py3-none-any.whl

uninstall:
	echo y | pip uninstall dist/code_counter-${VERSION}-py3-none-any.whl

clean:
	rm -rf build code_counter.* dist