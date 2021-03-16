import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analysis import test_normal_distribution as normal


def build_dataframe(tool_resfile_dict):
    df_o = pd.DataFrame(columns=tool_resfile_dict.keys())
    df_c = pd.DataFrame(columns=tool_resfile_dict.keys())
    df_e = pd.DataFrame(columns=tool_resfile_dict.keys())
    df_a = pd.DataFrame(columns=tool_resfile_dict.keys())
    df_n = pd.DataFrame(columns=tool_resfile_dict.keys())
    for tool in tool_resfile_dict:
        with open(file=tool_resfile_dict[tool], mode='r') as jsf:
            js = json.load(jsf)
            temp = pd.DataFrame.from_dict(js)
            df_o[tool] = temp['Openn']
            df_c[tool] = temp['Consc']
            df_e[tool] = temp['Extra']
            df_a[tool] = temp['Agree']
            df_n[tool] = temp['Neuro']
    return df_o, df_c, df_e, df_a, df_n


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


def pairwise_correlations(df_o, df_c, df_e, df_a, df_n):
    corr_matrices = dict()
    out = "Openness\n"
    corr_matrices['Openn'] = df_o.corr(method='pearson')
    out += str(corr_matrices['Openn'])
    corr_matrices['Openn'] = corr_matrices['Openn'].to_dict()
    out += "\n\nConscientiousness\n"
    corr_matrices['Consc'] = df_c.corr(method='pearson')
    out += str(corr_matrices['Consc'])
    corr_matrices['Consc'] = corr_matrices['Consc'].to_dict()
    out += "\n\nExtraversion\n"
    corr_matrices['Extra'] = df_e.corr(method='pearson')
    out += str(corr_matrices['Extra'])
    corr_matrices['Extra'] = corr_matrices['Extra'].to_dict()
    out += "\n\nAgreeableness\n"
    corr_matrices['Agree'] = df_a.corr(method='pearson')
    out += str(corr_matrices['Agree'])
    corr_matrices['Agree'] = corr_matrices['Agree'].to_dict()
    out += "\n\nNeuro\n"
    corr_matrices['Neuro'] = df_n.corr(method='pearson')
    out += str(corr_matrices['Neuro'])
    corr_matrices['Neuro'] = corr_matrices['Neuro'].to_dict()
    with open(file='results/phase1/pearson_r.txt', mode='w') as f:
        f.write(out)
    with open(file='results/phase1/pearson_r.json', mode='w') as js_f:
        json.dump(corr_matrices, js_f, indent=4)


def mailcorpus_stats():
    emails_dict = dict()
    no_emails = 0
    all_bodies = ""
    words_per_email = dict()
    tot_words_user = dict()
    with open(file="dataset/goldstandard/mailcorpus-sha.json", mode="r") as jsf:
        emails = json.load(jsf)
        # count emails
        for addr in emails:
            no_emails += len(emails[addr])
            bodies = ' '.join(emails[addr])
            emails_dict[addr] = bodies
            all_bodies += " " + bodies
            tot_words_user[addr] = len(bodies.split())
            words_per_email[addr] = tot_words_user[addr] / len(emails[addr])
    # count addresses
    with open(file="dataset/goldstandard/address_list_sha.txt", mode="r") as f:
        no_subjects = len(f.readlines())

    with open(file="results/phase1/descriptive_stats.txt", mode="w") as f:
        f.write("No. of subjects: {}\n".format(no_subjects))
        f.write("Total no. of emails: {}\n".format(no_emails))
        f.write("Total no. of words: {}\n".format(len(all_bodies.split())))
        f.write("Avg. no. of emails per user: {:.0f}\n".format(no_emails / no_subjects))
        f.write("Avg. no. of words per email: {:.0f}\n".format(np.mean(list(words_per_email.values()))))
        f.write("Avg. no. words per user: {:.0f}\n".format(np.mean(list(tot_words_user.values()))))


def groundtruth_stats(email_addresses):
    with open(file="dataset/goldstandard/ipip-scores-sha.json", mode="r") as jsf:
        df = pd.DataFrame.from_dict(json.load(jsf))
        df = df.loc[df['email'].isin(email_addresses)]
        openness = df['openness'].values
        conscientiousness = df['conscientiousness'].values
        extraversion = df['extraversion'].values
        agreeableness = df['agreeableness'].values
        neuroticism = df['neuroticism'].values

        fig, axes = plt.subplots()
        axes.violinplot(dataset=[openness, conscientiousness, extraversion, agreeableness, neuroticism], showmeans=True)
        xticklabels = ['Ope', 'Con', 'Ext', 'Agr', 'Neu']
        axes.set_xticks([1, 2, 3, 4, 5])
        axes.set_xticklabels(xticklabels)
        axes.yaxis.grid(True)
        plt.savefig("results/phase1/violins.png")


if __name__ == '__main__':
    with open(file="dataset/goldstandard/address_list_sha.txt", mode="r") as f:
        emails_addr = [e.strip() for e in f.readlines()]
        groundtruth_stats(emails_addr)
        mailcorpus_stats()

        tools = {'LIWC': 'dataset/LIWC/results/results.json',
                 'PR': 'dataset/PersonalityRecognizer/results/results.json'}  # ,
        # 'TP': 'dataset/twitpersonality/Results/results.json',
        # 'PI': 'dataset/PersonalityInsights/results'}
        df_o, df_c, df_e, df_a, df_n = build_dataframe(tools)
        normality_test(df_o, df_c, df_e, df_a, df_n, tools.keys())
        pairwise_correlations(df_o, df_c, df_e, df_a, df_n)
