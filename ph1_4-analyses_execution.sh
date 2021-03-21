#!/usr/bin/env bash

# -Ee ensures script will stop on first command failure (alternatively, use: set -o errexit)
# -u ensures script will exit on first unset variable encountered (alternatively, use: set -o nounset)
# -o pipefail ensures that if any command in a set of piped commands failed, the overall status is that of the failed one
set -Eeuo pipefail
export PYTHONPATH=.:./src

echo "Computing PHASE 1 analyses"
python src/phase1_analysis.py

echo "Done"
