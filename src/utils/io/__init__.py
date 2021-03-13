import csv
import json

import pandas as pd

GOLDSTANDARD_PATH = 'dataset/goldstandard/ipip-scores-sha.json'


def load_gold_standard():
    with open(file=GOLDSTANDARD_PATH, mode='r') as js_f:
        gs = json.load(js_f)
    gold_standard = pd.DataFrame.from_dict(gs)
    gold_standard = gold_standard.drop(columns=['id_test', 'time'])
    return gold_standard


def load_csv_into_df(path, sep=',', decimal='.'):
    return pd.read_csv(path, sep=sep, decimal=decimal)


def store_results(path_mae, mae, path_scores, scores):
    with open(file=path_mae, mode='w') as js_f:
        json.dump(mae, js_f, indent=4)
    scores.to_json(path_scores, indent=4)
