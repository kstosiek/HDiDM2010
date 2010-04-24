#!/bin/sh

# Run all tests, should be launched ONLY from src/tests
# directory.

export PYTHONPATH="../"

for test_file in *.py;
do
	python $test_file
done;
