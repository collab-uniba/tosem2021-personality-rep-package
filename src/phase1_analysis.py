import json

import numpy as np
import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer

from utils import io as io_utils
from utils import plot as plot_utils
from utils.math import test_normal_distribution as normal, qq_plot


def build_dataframe(tool_resfile_dict, gs_df):
    gs_df.drop(columns=['email'], inplace=True)
    df_o = pd.DataFrame(columns=['GOLDSTD'] + list(tool_resfile_dict.keys()))
    df_c = pd.DataFrame(columns=['GOLDSTD'] + list(tool_resfile_dict.keys()))
    df_e = pd.DataFrame(columns=['GOLDSTD'] + list(tool_resfile_dict.keys()))
    df_a = pd.DataFrame(columns=['GOLDSTD'] + list(tool_resfile_dict.keys()))
    df_n = pd.DataFrame(columns=['GOLDSTD'] + list(tool_resfile_dict.keys()))
    for tool in tool_resfile_dict:
        with open(file=tool_resfile_dict[tool], mode='r') as jsf:
            js = json.load(jsf)
            temp = pd.DataFrame.from_dict(js)
            df_o[tool] = temp['Openn']
            df_c[tool] = temp['Consc']
            df_e[tool] = temp['Extra']
            df_a[tool] = temp['Agree']
            df_n[tool] = temp['Neuro']

    df_o['GOLDSTD'] = gs_df['openness'].values
    df_c['GOLDSTD'] = gs_df['conscientiousness'].values
    df_e['GOLDSTD'] = gs_df['extraversion'].values
    df_a['GOLDSTD'] = gs_df['agreeableness'].values
    df_n['GOLDSTD'] = gs_df['neuroticism'].values
    return df_o, df_c, df_e, df_a, df_n, df_o.columns


def normality_test(df_o, df_c, df_e, df_a, df_n, tools):
    with open(file="results/phase1/shapiro.txt", mode="w") as f:
        for tool in tools:
            f.write("{}\n".format(tool))
            is_normal, stat, p = normal(df_o[tool])
            f.write("Openness normally distributed? {} (W={:.3f}, p={:.3f})\n".format(is_normal, stat, p))
            is_normal, stat, p = normal(df_c[tool])
            f.write("Conscientiousness normally distributed? {} (W={:.3f}, p={:.3f})\n".format(is_normal, stat, p))
            is_normal, stat, p = normal(df_e[tool])
            f.write("Extraversion normally distributed? {} (W={:.3f}, p={:.3f})\n".format(is_normal, stat, p))
            is_normal, stat, p = normal(df_a[tool])
            f.write("Agreeableness normally distributed? {} (W={:.3f}, p={:.3f})\n".format(is_normal, stat, p))
            is_normal, stat, p = normal(df_n[tool])
            f.write("Neuroticism normally distributed? {} (W={:.3f}, p={:.3f})\n\n".format(is_normal, stat, p))
            # QQ plot
            qq_plot(tool, df_o[tool], df_c[tool], df_e[tool], df_a[tool], df_n[tool])


def pairwise_correlations(df_o, df_c, df_e, df_a, df_n, method):
    corr_matrices = dict()
    out = "Openness\n"
    corr_matrices['Openn'] = df_o.corr(method=method).round(3)
    out += str(corr_matrices['Openn'])
    corr_matrices['Openn'] = corr_matrices['Openn'].to_dict()
    out += "\n\nConscientiousness\n"
    corr_matrices['Consc'] = df_c.corr(method=method).round(3)
    out += str(corr_matrices['Consc'])
    corr_matrices['Consc'] = corr_matrices['Consc'].to_dict()
    out += "\n\nExtraversion\n"
    corr_matrices['Extra'] = df_e.corr(method=method).round(3)
    out += str(corr_matrices['Extra'])
    corr_matrices['Extra'] = corr_matrices['Extra'].to_dict()
    out += "\n\nAgreeableness\n"
    corr_matrices['Agree'] = df_a.corr(method=method).round(3)
    out += str(corr_matrices['Agree'])
    corr_matrices['Agree'] = corr_matrices['Agree'].to_dict()
    out += "\n\nNeuro\n"
    corr_matrices['Neuro'] = df_n.corr(method=method).round(3)
    out += str(corr_matrices['Neuro'])
    corr_matrices['Neuro'] = corr_matrices['Neuro'].to_dict()
    with open(file='results/phase1/{}.txt'.format(method), mode='w') as f:
        f.write(out)
    with open(file='results/phase1/{}.json'.format(method), mode='w') as js_f:
        json.dump(corr_matrices, js_f, indent=4)


def mailcorpus_stats():
    emails_dict = dict()
    no_emails = 0
    all_bodies = ""
    words_per_email = dict()
    tot_words_user = dict()
    no_emails_per_user = dict()
    with open(file="dataset/goldstandard/mailcorpus-sha.json", mode="r") as jsf:
        emails = json.load(jsf)
        # count emails
        for subject in emails:
            no_emails_per_user[subject] = len(emails[subject])
            no_emails += no_emails_per_user[subject]
            bodies = ' '.join(emails[subject])
            emails_dict[subject] = bodies
            all_bodies += " " + bodies
            tot_words_user[subject] = len(bodies.split())
            words_per_email[subject] = tot_words_user[subject] / len(emails[subject])
    # count addresses
    with open(file="dataset/goldstandard/address_list_sha.txt", mode="r") as f:
        no_subjects = len(f.readlines())

    with open(file="results/phase1/mail_corpus_stats.txt", mode="w") as f:
        f.write("No. of subjects: {}\n".format(no_subjects))
        f.write("Total no. of emails: {}\n".format(no_emails))
        f.write("Total no. of words: {}\n".format(len(all_bodies.split())))
        f.write("Avg. no. of emails per user {:.0f} (SD {:.2f})\n".format(no_emails / no_subjects,
                                                                          np.std(list(
                                                                              no_emails_per_user.values()))))
        # f.write(
        #    "Avg. no. of words per email {:.0f} (SD {:.2f})\n".format(np.mean(list(words_per_email.values())),
        #                                                                        np.std(list(words_per_email.values()))))
        f.write("Avg. no. words per user {:.0f} (SD {:.2f})\n".format(np.mean(list(tot_words_user.values())),
                                                                      np.std(list(tot_words_user.values()))))


def descriptive_stats(df_o, df_c, df_e, df_a, df_n, tools):
    with open(file="results/phase1/descriptive_stats.txt", mode="w") as f:
        for tool in tools:
            openness = df_o[tool].values
            conscientiousness = df_c[tool].values
            extraversion = df_e[tool].values
            agreeableness = df_a[tool].values
            neuroticism = df_n[tool].values
            f.write("{}\n".format(tool))
            f.write(
                "Mean Openness {:.2f}, Median {:.2f} (Min {:.2f}, Max {:.2f}, SD {:.2f})\n".format(np.mean(openness),
                                                                                                   np.median(openness),
                                                                                                   min(openness),
                                                                                                   max(openness),
                                                                                                   np.std(openness)))
            f.write(
                "Mean Conscientiousness {:.2f}, Median {:.2f} (Min {:.2f}, Max {:.2f}, SD {:.2f})\n".format(
                    np.mean(conscientiousness),
                    np.median(conscientiousness),
                    min(conscientiousness),
                    max(conscientiousness),
                    np.std(conscientiousness)))
            f.write("Mean Extraversion {:.2f}, Median {:.2f} (Min {:.2f}, Max {:.2f}, SD {:.2f})\n".format(
                np.mean(extraversion),
                np.median(extraversion),
                min(extraversion),
                max(extraversion),
                np.std(extraversion)))
            f.write("Mean Agreeableness {:.2f}, Median {:.2f} (Min {:.2f}, Max {:.2f}, SD {:.2f})\n".format(
                np.mean(agreeableness),
                np.median(agreeableness),
                min(agreeableness),
                max(agreeableness),
                np.std(agreeableness)))
            f.write("Mean Neuroticism {:.2f}, Median {:.2f} (Min {:.2f}, Max {:.2f}, SD {:.2f})\n\n".format(
                np.mean(neuroticism),
                np.median(neuroticism),
                min(neuroticism),
                max(neuroticism),
                np.std(neuroticism)))


def save_plots(df_o, df_c, df_e, df_a, df_n, tools):
    for tool in tools:
        path = "results/phase1/{}-violins.png".format(tool)
        plot_utils.save_violins_plot(df_o[tool], df_c[tool], df_e[tool], df_a[tool], df_n[tool], path)


def _mark_strong_disagreements(tool_scores, ids, gs_scores):
    res = list()
    for i in range(0, len(gs_scores)):
        if abs(tool_scores[i] - gs_scores[i]) == 2:
            res.append(ids[i].strip())
    return res


def _mark_disagreements(tool_scores, ids, gs_scores):
    res = list()
    for i in range(0, len(gs_scores)):
        if tool_scores[i] != gs_scores[i]:
            res.append(ids[i].strip())
    return res


def error_analysis(_tools, gs_df):
    # 0=LOW, 1=MEDIUM, 2=HIGH
    discretizer = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='kmeans')

    gs_df = discretizer.fit_transform(gs_df.values)

    res_dict = dict()
    _df_o = dict()
    _df_c = dict()
    _df_e = dict()
    _df_a = dict()
    _df_n = dict()
    _df_id = dict()
    for tool in _tools:
        with open(file=_tools[tool], mode='r') as jsf:
            temp = pd.DataFrame.from_dict(json.load(jsf))
            _df_o[tool] = discretizer.fit_transform(temp['Openn'].values.reshape(-1, 1))
            _df_c[tool] = discretizer.fit_transform(temp['Consc'].values.reshape(-1, 1))
            _df_e[tool] = discretizer.fit_transform(temp['Extra'].values.reshape(-1, 1))
            _df_a[tool] = discretizer.fit_transform(temp['Agree'].values.reshape(-1, 1))
            _df_n[tool] = discretizer.fit_transform(temp['Neuro'].values.reshape(-1, 1))
            _df_id[tool] = temp['email'].values
    res_dict['Openn'] = _df_o
    res_dict['Consc'] = _df_c
    res_dict['Extra'] = _df_e
    res_dict['Agree'] = _df_a
    res_dict['Neuro'] = _df_n
    res_dict['email'] = _df_id

    strong_disagreements = dict()
    disagreements = dict()
    for tool in _tools:
        strong_disagreements["{}-{}".format(tool, 'Openn')] = _mark_strong_disagreements(res_dict['Openn'][tool],
                                                                                         res_dict['email'][tool],
                                                                                         gs_df[:, 0])
        disagreements[(tool, 'Openn')] = _mark_disagreements(res_dict['Openn'][tool],
                                                             res_dict['email'][tool],
                                                             gs_df[:, 0])
        strong_disagreements["{}-{}".format(tool, 'Consc')] = _mark_strong_disagreements(res_dict['Consc'][tool],
                                                                                         res_dict['email'][tool],
                                                                                         gs_df[:, 1])
        disagreements[(tool, 'Consc')] = _mark_disagreements(res_dict['Consc'][tool],
                                                             res_dict['email'][tool],
                                                             gs_df[:, 1])
        strong_disagreements["{}-{}".format(tool, 'Extra')] = _mark_strong_disagreements(res_dict['Extra'][tool],
                                                                                         res_dict['email'][tool],
                                                                                         gs_df[:, 2])
        disagreements[(tool, 'Extra')] = _mark_disagreements(res_dict['Extra'][tool],
                                                             res_dict['email'][tool],
                                                             gs_df[:, 2])
        strong_disagreements["{}-{}".format(tool, 'Agree')] = _mark_strong_disagreements(res_dict['Agree'][tool],
                                                                                         res_dict['email'][tool],
                                                                                         gs_df[:, 3])
        disagreements[(tool, 'Agree')] = _mark_disagreements(res_dict['Agree'][tool],
                                                             res_dict['email'][tool],
                                                             gs_df[:, 3])
        strong_disagreements["{}-{}".format(tool, 'Neuro')] = _mark_strong_disagreements(res_dict['Neuro'][tool],
                                                                                         res_dict['email'][tool],
                                                                                         gs_df[:, 4])
        disagreements[(tool, 'Neuro')] = _mark_disagreements(res_dict['Neuro'][tool],
                                                             res_dict['email'][tool],
                                                             gs_df[:, 4])

    with open(file='results/phase1/errors_strong.json', mode='w') as js_f:
        json.dump(strong_disagreements, js_f, indent=4)

    results = dict()
    for tool in _tools:
        o_s = set(disagreements[(tool, 'Openn')])
        try:
            results['Openn'] = set.intersection(results['Openn'], o_s)
        except KeyError:
            results['Openn'] = o_s
        c_s = set(disagreements[(tool, 'Consc')])
        try:
            results['Consc'] = set.intersection(results['Consc'], c_s)
        except KeyError:
            results['Consc'] = c_s
        e_s = set(disagreements[(tool, 'Extra')])
        try:
            results['Extra'] = set.intersection(results['Extra'], e_s)
        except KeyError:
            results['Extra'] = e_s
        a_s = set(disagreements[(tool, 'Agree')])
        try:
            results['Agree'] = set.intersection(results['Agree'], a_s)
        except KeyError:
            results['Agree'] = a_s
        n_s = set(disagreements[(tool, 'Neuro')])
        try:
            results['Neuro'] = set.intersection(results['Neuro'], n_s)
        except KeyError:
            results['Neuro'] = n_s

    for k in results:
        results[k] = list(results[k])
    with open(file='results/phase1/errors_common.json', mode='w') as js_f:
        json.dump(results, js_f, indent=4)


if __name__ == '__main__':
    mailcorpus_stats()
    with open(file="dataset/goldstandard/address_list_sha.txt", mode="r") as f:
        emails_addr = [e.strip() for e in f.readlines()]
        goldstd_df = io_utils.load_gold_standard()
        goldstd_df = goldstd_df[goldstd_df['email'].isin(emails_addr)].reset_index(drop=True)
        goldstd_df.drop(goldstd_df.tail(1).index, inplace=True)  # remove extra line

        tools = {'LIWC': 'dataset/LIWC/results/results.json',
                 'PI': 'dataset/PersonalityInsights/results/results.json',
                 'PR': 'dataset/PersonalityRecognizer/results/results.json',
                 'TP': 'dataset/twitpersonality/Results/results.json'}
        df_o, df_c, df_e, df_a, df_n, col_names = build_dataframe(tools, goldstd_df)
        descriptive_stats(df_o, df_c, df_e, df_a, df_n, col_names)
        normality_test(df_o, df_c, df_e, df_a, df_n, col_names)
        # With large sample, where Pearson normality assumption is violated, this is not an issue.
        # With small samples though, Spearman's correlation should be preferred.
        # Source: On the Effects of Non-Normality on the Distribution of the Sample Product-Moment
        #         Correlation Coefficient (Kowalski, 1975), url: www.jstor.org/pss/2346598
        pairwise_correlations(df_o, df_c, df_e, df_a, df_n, method="pearson")
        pairwise_correlations(df_o, df_c, df_e, df_a, df_n, method="spearman")
        save_plots(df_o, df_c, df_e, df_a, df_n, col_names)

        error_analysis(tools, goldstd_df.copy(deep=True))
