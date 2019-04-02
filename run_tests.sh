#!/usr/bin/env bash
echo "Build cython modules..."
compile_result="$(python setup.py build_ext)"
if [ "$compile_result" == 'running build_ext' ]
then
    echo "Installing project locally..."
    pip install -e .
    echo "Running pytest..."
    pytest $@
    echo "Running radon..."
    radon cc -s -a gideon
fi
