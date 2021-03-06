#!/usr/bin/env bash

# -Ee ensures script will stop on first command failure (alternatively, use: set -o errexit)
# -u ensures script will exit on first unset variable encountered (alternatively, use: set -o nounset)
# -o pipefail ensures that if any command in a set of piped commands failed, the overall status is that of the failed one
set -Eeuo pipefail

echo "Setting up environment dependencies."
if [[ "$OSTYPE" == "darwin"* ]]; then
  echo "Installing macOS-specific requirements"
  brew install icu4c
  brew link icu4c --force
  ver=$(icu-config --version)
  export ICU_VERSION="${ver}"
  export PYICU_INCLUDES="/usr/local/Cellar/icu4c/${ver}/include"
  export PYICU_LFLAGS=-L"/usr/local/Cellar/icu4c/${ver}/lib"
  brew install libxml2
fi

echo "Installing R packages, please enter the sudo password"
REPO='https://cloud.r-project.org'
sudo Rscript -e "install.packages('remotes', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "remotes::install_github('M3SOulu/NLoN')"
sudo Rscript -e "install.packages('readr', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('dplyr', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('sqldf', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('nortest', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('Hmisc', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "remotes::install_github('slowkow/ggrepel')"
sudo Rscript -e "install.packages('FactoMineR', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('factoextra', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('psych', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('cluster', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('ggplot2', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('plyr', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('sjstats', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('PMCMR', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('rcompanion', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('archetypes', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('effsize', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('metan', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('arm', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('ROCR', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('piecewiseSEM', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('effects', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('IRdisplay', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('moments', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('MuMIn', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"
sudo Rscript -e "install.packages('renv', dependencies=TRUE, INSTALL_opts='--no-lock', repos='${REPO}')"

echo "Setting up the virtual environment"
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt

echo "Setting up TwitPersonality"
wget https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M.vec.zip
unzip wiki-news-300d-1M.vec.zip -d twitpersonality/FastText
rm wiki-news-300d-1M.vec.zip
mv twitpersonality/FastText/wiki-news-300d-1M.vec twitpersonality/FastText/dataset.vec
ln -s "$(pwd)/dataset/twitpersonality/myPersonality" "$(pwd)/twitpersonality/training/dataset"
ln -s "$(pwd)/dataset/twitpersonality/Results" "$(pwd)/twitpersonality/training/Results"
ln -s "$(pwd)/dataset/twitpersonality/Models" "$(pwd)/twitpersonality/training/Models"
ln -s "$(pwd)/dataset/twitpersonality/Data" "$(pwd)/twitpersonality/test/Data"

echo "Setting up replication packages"
unzip rep-packages/iyer2019tse/data/final.csv.zip -d rep-packages/iyer2019tse/data/
unzip rep-packages/iyer2019tse/data/final_LIWC.csv.zip -d rep-packages/iyer2019tse/data/

echo "Done"
