#!/usr/bin/env bash

PYTHONPATH=./src

echo "Setting up input data for the tools"
python src/data_preparation.py
echo "Done"
