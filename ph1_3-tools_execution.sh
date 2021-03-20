#!/usr/bin/env bash

export PYTHONPATH=.:./src:./twitpersonality

echo "Running tools"

echo "Personality Recognizer"
#cd PersonalityRecognizer || exit
#source PersonalityRecognizer.sh -i ../dataset/PersonalityRecognizer/data -d -t 2 -m 4 > output.txt
#mv output.txt ../dataset/PersonalityRecognizer/results/
#cd ..
#python src/pr.py

echo "LIWC"
echo "LIWC is a desktop app, execute it manually to create LIWC2007_output.csv stored in dataset/LIWC/data"
# if you used LIWC 2015, pass 2015 as parameter
#python src/liwc.py 2007

echo "TwitPersonality"
python src/tp.py

echo "Personality Insights"
#python src/ibmpi.py

echo "Done"
