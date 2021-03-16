import pandas as pd
import json
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


if __name__ == '__main__':
    tools = {'LIWC': 'dataset/LIWC/results/results.json',
             'PR': 'dataset/PersonalityRecognizer/results/results.json'}  # ,
    # 'TP': 'dataset/twitpersonality/Results/results.json',
    # 'PI': 'dataset/PersonalityInsights/results'}
    df_o, df_c, df_e, df_a, df_n = build_dataframe(tools)

    normality_test(df_o, df_c, df_e, df_a, df_n, tools.keys())
    pairwise_correlations(df_o, df_c, df_e, df_a, df_n)



