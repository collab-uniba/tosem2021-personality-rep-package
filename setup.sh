#!/usr/bin/env bash

echo "Setting up TwitPersonality"
wget https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M.vec.zip
unzip wiki-news-300d-1M.vec.zip -d twitpersonality/FastText
rm wiki-news-300d-1M.vec.zip
mv twitpersonality/FastText/wiki-news-300d-1M.vec twitpersonality/FastText/dataset.vec
ln -s twitpersonality-dataset twitpersonality/training/dataset
echo "Done\n"

echo "Setting up Personality Recognizer"
test
if [ -z ${JAVA_HOME} ]; then
  echo "JAVA_HOME is unset, error"
  exit 1
else
  echo "JAVA_HOME is set to '$JAVA_HOME'"
fi
chmod +x ./PersonalityRecognizer/PersonalityRecognizer.sh
