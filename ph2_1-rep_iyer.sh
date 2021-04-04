#!/usr/bin/env bash

# -Ee ensures script will stop on first command failure (alternatively, use: set -o errexit)
# -u ensures script will exit on first unset variable encountered (alternatively, use: set -o nounset)
# -o pipefail ensures that if any command in a set of piped commands failed, the overall status is that of the failed one
set -Eeuo pipefail

# remove parameter `test` to execute the scripts of the full dataset
Rscript --vanilla rep-packages/iyer2019tse/RQ0/RQ0.R  rep-packages/iyer2019tse/data/final.csv test
Rscript --vanilla rep-packages/iyer2019tse/RQ1/RQ1.R  rep-packages/iyer2019tse/data/final_LIWC.csv test
Rscript --vanilla rep-packages/iyer2019tse/RQ2/RQ2.R  rep-packages/iyer2019tse/data/final_LIWC.csv test
Rscript --vanilla rep-packages/iyer2019tse/RQ3/RQ3.R  rep-packages/iyer2019tse/data/final_LIWC.csv test
