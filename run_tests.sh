#!/usr/bin/env bash
echo "Build cython modules..."
python setup.py build_ext
echo "Installing project locally..."
pip install -e .
echo "Running pytest..."
pytest -vvvv -s --cov=gideon --cov-report term-missing tests/
