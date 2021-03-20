#!/usr/bin/env bash

export PYTHONPATH=.:./src

echo "Computing PHASE 1 analyses"
python src/phase1_analysis.py

echo "Done"
