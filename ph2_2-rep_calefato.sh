#!/usr/bin/env bash

# -Ee ensures script will stop on first command failure (alternatively, use: set -o errexit)
# -u ensures script will exit on first unset variable encountered (alternatively, use: set -o nounset)
# -o pipefail ensures that if any command in a set of piped commands failed, the overall status is that of the failed one
set -Eeuo pipefail

Rscript -e "rmarkdown::render('rep-packages/calefato2019ist/RQ1.Rmd',
                              params=list(data = 'datasets/pers_liwc07_nlon.csv'))"
Rscript -e "rmarkdown::render('rep-packages/calefato2019ist/RQ2-3-4.Rmd',
                              params=list(data = 'datasets/pers_liwc07_nlon.csv', commits = 'datasets/commits.csv'))"
Rscript -e "rmarkdown::render('rep-packages/calefato2019ist/RQ5-6.Rmd',
                              params=list(data = 'datasets/pers_liwc07_nlon.csv', commits = 'datasets/commits.csv'))"
