#!/usr/bin/env bash

echo "Setting up environment dependencies."

if [[ "$OSTYPE" == "darwin"* ]]; then
  # TODO check if brew is available
  echo "Installing macOS-specific requirements"
  brew install icu4c
  brew link icu4c --force
  ver=$(icu-config --version)
  export ICU_VERSION="${ver}"
  export PYICU_INCLUDES="/usr/local/Cellar/icu4c/${ver}/include"
  export PYICU_LFLAGS=-L"/usr/local/Cellar/icu4c/${ver}/lib"
fi

echo "Installing R packages"
# TODO check if R is available
Rscript -e "install.packages('remotes', dependencies=TRUE, repos='https://cloud.r-project.org')"
Rscript -e "remotes::install_github('M3SOulu/NLoN')"

echo "Setting up the virtual environment"
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
deactivate

echo "Setting up TwitPersonality"
wget https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M.vec.zip
unzip wiki-news-300d-1M.vec.zip -d twitpersonality/FastText
rm wiki-news-300d-1M.vec.zip
mv twitpersonality/FastText/wiki-news-300d-1M.vec twitpersonality/FastText/dataset.vec

ln -s "$(pwd)/dataset/twitpersonality/myPersonality" "$(pwd)/twitpersonality/training/dataset"
ln -s "$(pwd)/dataset/twitpersonality/Results" "$(pwd)/twitpersonality/training/Results"
ln -s "$(pwd)/dataset/twitpersonality/Models" "$(pwd)/twitpersonality/training/Models"
ln -s "$(pwd)/dataset/twitpersonality/Data" "$(pwd)/twitpersonality/test/Data"

echo "Setting up Personality Recognizer"
test
if [ -z "${JAVA_HOME}" ]; then
  echo "JAVA_HOME is unset, error"
  exit 1
else
  echo "JAVA_HOME is set to '$JAVA_HOME'"
fi
chmod +x ./PersonalityRecognizer/PersonalityRecognizer.sh
echo "Done"
