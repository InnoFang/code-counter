setup:
	python setup.py install


.PHONY:
build:
	python setup.py bdist_wheel

install:build
	pip install dist/*.whl

uninstall:
	echo y | pip uninstall code-counter

clean:
	rm -rf build code_counter.* dist