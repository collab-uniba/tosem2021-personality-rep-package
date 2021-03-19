import pandas as pd

import utils.io as io_utils
import utils.math as math_utils

if __name__ == '__main__':
    gold_std_df = io_utils.load_gold_standard()
    res_df = pd.read_json("dataset/PersonalityInsights/data/dataset.json")
    rescaled_res_df = math_utils.rescale(res_df, old_min=0, old_max=1, new_min=1, new_max=5)
    MAE = math_utils.compute_mae(rescaled_res_df, gold_std_df)
    RMSE = math_utils.compute_rmse(rescaled_res_df, gold_std_df)
    io_utils.store_results('dataset/PersonalityInsights/results/mae.json', MAE,
                           'dataset/PersonalityInsights/results/rmse.json', RMSE,
                           'dataset/PersonalityInsights/results/results.json', rescaled_res_df)
