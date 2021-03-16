import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


def rescale(res_df, old_min, old_max, new_min=1, new_max=5):
    res_5point_df = res_df.copy(deep=True)
    for col_name in ('Openn', 'Consc', 'Extra', 'Agree', 'Neuro'):
        new_values = list()
        col = res_5point_df[col_name]
        for x in col:
            r_x = _rescale(x, old_min, old_max, new_min, new_max)
            new_values.append(r_x)
        res_5point_df[col_name] = new_values
    return res_5point_df


def _rescale(x, old_min, old_max, new_min, new_max):
    x_rescaled = (new_max - new_min) * (x - old_min) / (old_max - old_min) + new_min
    return x_rescaled


def _setup_dataset(goldstd, results):
    data_extra = results.sort_values(by=['email'])
    gold_extra = goldstd.sort_values(by='email')
    """
    Gold standard and Personality Recognizer's output are merged into a single dataset
    to create the confusion matrix. The merge happens on the column email of both
    files.
    """
    merged_dataset = pd.merge(data_extra, gold_extra, on=['email'], how='inner')
    return merged_dataset


def compute_mae(results, goldstd):
    """
    $\mathrm{MAE}=\frac{1}{n} \sum_{i=1}^{n}\left|y_{i}-x_{i}\right|$

    The Mean Absolute Error (MAE) is a measure of errors between paired
    observations expressing the same phenomenon. It is a linear linear
    score, which means that all individual differences are weighted
    equally on the average.
    """
    merged_dataset = _setup_dataset(goldstd, results)
    """
    The Mean Absolute Error is calculated using the scikit function 
    (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html)
    and then stored in a list.
    """
    mae = dict()
    mae['Extra'] = mean_absolute_error(merged_dataset['extraversion'], merged_dataset['Extra'])
    mae['Neuro'] = mean_absolute_error(merged_dataset['neuroticism'], merged_dataset['Neuro'])
    mae['Consc'] = mean_absolute_error(merged_dataset['conscientiousness'], merged_dataset['Consc'])
    mae['Openn'] = mean_absolute_error(merged_dataset['openness'], merged_dataset['Openn'])
    mae['Agree'] = mean_absolute_error(merged_dataset['agreeableness'], merged_dataset['Agree'])
    return mae


def compute_rmse(results, goldstd):
    merged_dataset = _setup_dataset(goldstd, results)
    rmse = dict()
    rmse['Extra'] = mean_squared_error(merged_dataset['Extra'], merged_dataset['extraversion'], squared=True)
    rmse['Neuro'] = mean_squared_error(merged_dataset['Neuro'], merged_dataset['neuroticism'], squared=True)
    rmse['Consc'] = mean_squared_error(merged_dataset['Consc'], merged_dataset['conscientiousness'], squared=True)
    rmse['Openn'] = mean_squared_error(merged_dataset['Openn'], merged_dataset['openness'], squared=True)
    rmse['Agree'] = mean_squared_error(merged_dataset['Agree'], merged_dataset['agreeableness'], squared=True)
    return rmse
