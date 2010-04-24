#!/bin/sh

# Run all tests, should be launched ONLY from src/tests
# directory. Cd into src/tests and type sh run_tests.sh.

export PYTHONPATH="../"

for test_file in *.py;
do
	python $test_file
done;
