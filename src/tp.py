import os

import joblib
import numpy as np
import pandas as pd

from twitpersonality.training import datasetUtils, embeddings
from utils import io as io_utils
from utils import math as math_utils


def get_profile_twit_pers():
    word_dict = datasetUtils.parseFastText("twitpersonality/FastText/dataset.vec")

    content = os.listdir("dataset/twitpersonality/Data")
    email_addr = list()
    scores_list = list()
    for file in content:
        sha = file.split('.')[0]
        email_addr.append(sha)

        try:
            user_emails = open(file=os.path.join("dataset/twitpersonality/Data", file), mode="r").read()
            content = embeddings.transformTextForTesting(embed_dictionary=word_dict, length_threshold=3,
                                                         documents=[user_emails], operation="conc")
        except Exception:
            print("Not enough words for the prediction of subject {}.".format(sha))
            continue

        scores = dict()
        for trait in ["O", "C", "E", "A", "N"]:
            model = joblib.load("dataset/twitpersonality/Models/MPBig/SVM_Big_conc_" + trait + ".pkl")
            preds = model.predict(content)
            scores[trait] = float(str(np.mean(np.array(preds)))[0:5])
        row_dict = {'email': sha, 'Openn': scores["O"], 'Consc': scores["C"], 'Extra': scores["E"], 'Agree': scores["A"], 'Neuro': scores["N"]}
        scores_list.append(row_dict)

    scores_df = pd.DataFrame(data=scores_list, columns=('email', 'Openn', 'Consc', 'Extra', 'Agree', 'Neuro'))
    return scores_df, email_addr


if __name__ == '__main__':
    gold_std_df = io_utils.load_gold_standard()
    pred_scores_df, hashed_email_addresses = get_profile_twit_pers()
    MAE = math_utils.compute_mae(pred_scores_df, gold_std_df)
    RMSE = math_utils.compute_rmse(pred_scores_df, gold_std_df)
    io_utils.store_results('dataset/twitpersonality/Results/mae.json', MAE,
                           'dataset/twitpersonality/Results/rmse.json', RMSE,
                           'dataset/twitpersonality/Results/results.json', pred_scores_df)
