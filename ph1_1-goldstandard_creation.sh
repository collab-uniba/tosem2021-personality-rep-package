#!/usr/bin/env bash

PYTHONPATH=./src

echo "Setting up the gold standard files"
python src/goldstandard_creation.py
echo "Done"
