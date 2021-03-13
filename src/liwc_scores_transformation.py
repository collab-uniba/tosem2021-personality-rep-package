"""
References
T. Yarkoni, "Personality in 100,000 words: A large-scale analysis of personality and word use among bloggers,"
Journal of research in personality, vol. 44, no. 3, pp.363-373, 2010 (suppl. material)
"""

import sys

import pandas as pd

import utils.io as io_utils
import utils.math as math_utils


def _get_openness(score, liwc_ver):
    value = (
            - 0.21 * score['pronoun'] - 0.16 * score['i'] - 0.1 * score['we'] - 0.12 * score['you'] - 0.13 *
            score['negate'] - 0.11 * score['assent'] + 0.2 * score['article'] - 0.12 * score['affect'] - 0.15 *
            score['posemo'] - 0.12 * score['discrep'] - 0.08 * score['hear'] - 0.14 * score['social'] - 0.17 *
            score['family'] - 0.22 * score['time'] - 0.11 * score['space'] - 0.22 * score['motion'] -
            0.17 * score['leisure'] - 0.2 * score['home'] + 0.15 * score['death'] - 0.15 * score['ingest'])

    if liwc_ver == '2007':
        value = value + 0.17 * score['preps'] - 0.09 * score['cogmech'] - 0.16 * score['past'] - 0.16 * score[
            'present'] - 0.09 * score['humans'] - 0.11 * score['incl']
    elif liwc_ver == '2015':
        value = value + 0.17 * score['prep'] - 0.09 * score['cogproc'] - 0.16 * score['focuspast'] - 0.16 * score[
            'focuspresent']
    return value


def _get_conscientiousness(score, liwc_ver):
    value = (- 0.17 * score['negate'] - 0.18 * score['negemo'] - 0.19 * score['anger'] - 0.11 * score['sad'] - 0.12 *
             score['cause'] - 0.13 * score['discrep'] - 0.1 * score['tentat'] - 0.1 * score['certain'] - 0.12 *
             score['hear'] + 0.09 * score['time'] + 0.14 * score['achieve'] - 0.12 * score['death'] -
             0.14 * score['swear'])

    if liwc_ver == '2007':
        value = value - 0.11 * score['cogmech'] - 0.12 * score['humans'] - 0.16 * score['excl']
    elif liwc_ver == '2015':
        value = value - 0.11 * score['cogproc']
    return value


def _get_extraversion(score, liwc_ver):
    value = (0.11 * score['we'] + 0.16 * score['you'] - 0.12 * score['number'] + 0.1 * score['posemo'] -
             0.09 * score['cause'] - 0.11 * score['tentat'] + 0.1 * score['certain'] + 0.12 * score['hear'] + 0.15 *
             score['social'] + 0.15 * score['friend'] + 0.09 * score['family'] - 0.08 * score['work'] - 0.09 *
             score['achieve'] + 0.08 * score['leisure'] + 0.11 * score['relig'] + 0.1 * score['body'] + 0.17 *
             score['sexual'])
    if liwc_ver == '2007':
        value = value + 0.13 * score['humans'] + 0.09 * score['incl']
    return value


def _get_agreeableness(score, liwc_ver):
    value = (0.11 * score['pronoun'] + 0.18 * score['we'] + 0.11 * score['number'] + 0.18 *
             score['posemo'] - 0.15 * score['negemo'] - 0.23 * score['anger'] - 0.11 * score['cause'] + 0.09 *
             score['see'] + 0.1 * score['feel'] + 0.13 * score['social'] + 0.11 * score['friend'] + 0.19 *
             score['family'] + 0.12 * score['time'] + 0.16 * score['space'] + 0.14 * score['motion'] + 0.15 *
             score['leisure'] + 0.19 * score['home'] - 0.11 * score['money'] - 0.13 * score['death'] + 0.09 *
             score['body'] + 0.08 * score['sexual'] - 0.21 * score['swear'])
    if liwc_ver == '2007':
        value = value + 0.1 * score['past'] + 0.18 * score['incl']
    elif liwc_ver == '2015':
        value = value + 0.1 * score['focuspast']
    return value


def _get_neuroticism(score, liwc_ver):
    value = (
            0.12 * score['i'] - 0.15 * score['you'] + 0.11 * score['negate'] - 0.11 * score['article'] + 0.16 *
            score['negemo'] + 0.17 * score['anx'] + 0.13 * score['anger'] + 0.1 * score['sad'] + 0.11 *
            score['cause'] + 0.13 * score['discrep'] + 0.12 * score['tentat'] + 0.13 * score['certain'] + 0.1 *
            score['feel'] - 0.08 * score['friend'] - 0.09 * score['space'] + 0.11 + score['swear'])
    if liwc_ver == '2007':
        value = value + 0.13 * score['cogmech'] + 0.1 * score['excl']
    elif liwc_ver == '2015':
        value = value + 0.13 * score['cogproc']
    return value


def compute_big5_scores(emails, raw_results, dict_ver):
    col_names = ('email', 'Openn', 'Consc', 'Extra', 'Agree', 'Neuro')
    scores_list = list()
    for email in emails:
        row = raw_results.loc[raw_results['Source (A)'] == email].copy(deep=True)
        row = row.drop(columns=['Source (A)']).iloc[0]  # there's just one row
        ope = _get_openness(row, dict_ver)
        con = _get_conscientiousness(row, dict_ver)
        ext = _get_extraversion(row, dict_ver)
        agr = _get_agreeableness(row, dict_ver)
        neu = _get_neuroticism(row, dict_ver)
        row_dict = {'email': email.strip('"'), 'Openn': ope, 'Consc': con, 'Extra': ext, 'Agree': agr, 'Neuro': neu}
        scores_list.append(row_dict)
    scores = pd.DataFrame(data=scores_list, columns=col_names)
    return scores


def min_max(scores):
    _min = scores[['Openn', 'Consc', 'Extra', 'Agree', 'Neuro']].min(skipna=True)
    _max = scores[['Openn', 'Consc', 'Extra', 'Agree', 'Neuro']].min(skipna=True)
    return round(_min.min()), round(_max.max())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error, missing argument: pass "2007" or "2015"')
        exit(1)
    liwc_dictionary = str(sys.argv[1])
    path = 'dataset/LIWC/data/LIWC{}_output.csv'.format(liwc_dictionary)
    liwc_results_raw = io_utils.load_csv_into_df(path=path, sep=',', decimal=',')
    liwc_results_raw.drop(columns=['Source (B)'], inplace=True)  # drop email bodies
    hashed_emails = liwc_results_raw['Source (A)']  # these emails are wrapped in ""
    gold_std_df = io_utils.load_gold_standard()

    scores_df = compute_big5_scores(hashed_emails, liwc_results_raw, liwc_dictionary)
    """
        Gold standard contains more developers than the dataset
        So, we remove all the useless entries
    """
    gold_std_df = gold_std_df.loc[gold_std_df['email'].isin(scores_df['email'])]
    min, max = min_max(scores_df)
    rescaled_res_df = math_utils.rescale(scores_df, old_min=min, old_max=max, new_min=1, new_max=5)
    MAE = math_utils.compute_mae(rescaled_res_df, gold_std_df)
    io_utils.store_results('dataset/LIWC/results/mae.json', MAE, 'dataset/LIWC/results/results.json', rescaled_res_df)
