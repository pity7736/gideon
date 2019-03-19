#!/usr/bin/env bash
echo "Build cython modules..."
python setup.py build_ext
echo "Installing project locally..."
pip install -e .
echo "Running pytest..."
pytest $@
echo "Running radon..."
radon cc -s -a gideon
