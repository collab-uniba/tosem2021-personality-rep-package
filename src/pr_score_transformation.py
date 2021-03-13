import re
from io import StringIO

import numpy as np
import pandas as pd

from utils import io as io_utils
from utils import math as math_utils

tab_header = ['email', 'Extra', 'Neuro', 'Agree', 'Consc', 'Openn']


def get_results_table(txt):
    table = txt.strip().split('\n\n\n\n')[3]
    hashes = re.findall(r'(.*)\.txt', table)
    return hashes, table.replace('.txt ', '')


def parse_results_table(hashes, data):
    t_array = np.genfromtxt(StringIO(data), delimiter='\t', skip_header=1, usecols=(0, 1, 2, 3, 4, 5))
    df = pd.DataFrame(t_array, columns=tab_header)
    df['email'] = hashes
    return df


if __name__ == '__main__':
    with open(file="dataset/PersonalityRecognizer/results/output.txt", mode="r") as f:
        text = '\n'.join(f.readlines())
    hashed_email_addresses, txt_table = get_results_table(text)
    res_df = parse_results_table(hashed_email_addresses, txt_table)
    gold_std_df = io_utils.load_gold_standard()
    """
    Gold standard contains more developers than the dataset
    So, we remove all the useless entries
    """
    gold_std_df = gold_std_df.loc[gold_std_df['email'].isin(hashed_email_addresses)]
    rescaled_res_df = math_utils.rescale(res_df, old_min=1, old_max=7, new_min=1, new_max=5)
    MAE = math_utils.compute_mae(rescaled_res_df, gold_std_df)
    io_utils.store_results('dataset/PersonalityRecognizer/results/mae.json', MAE,
                           'dataset/PersonalityRecognizer/results/results.json', rescaled_res_df)
