#!/usr/bin/env bash

PYTHONPATH=./src

echo "Running tools"

echo "Personality Recognizer"
cd PersonalityRecognizer || exit
source PersonalityRecognizer.sh -i ../dataset/PersonalityRecognizer/data -d -t 2 -m 4 > output.txt
mv output.txt ../dataset/PersonalityRecognizer/results/
cd ..
python src/pr_score_transformation.py

echo "LIWC"
echo "LIWC is a desktop app, execute it manually to create LIWC2007_output.csv stored in dataset/LIWC/data"
# if you used LIWC 2015, pass 2015 as parameter
python src/liwc_scores_transformation.py 2007


echo "TwitPersonality"


echo "Personality Insights"


echo "Computing PHASE 1 analyses"
python src/analysis/run_analysis.py

echo "Done"
