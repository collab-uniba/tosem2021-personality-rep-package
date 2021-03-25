import matplotlib.pyplot as plt
import numpy as np


def save_violins_plot(openness, conscientiousness, extraversion, agreeableness, neuroticism, path):
    fig, axes = plt.subplots()
    axes.violinplot(dataset=[openness, conscientiousness, extraversion, agreeableness, neuroticism], showmeans=True)
    xticklabels = ['Ope', 'Con', 'Ext', 'Agr', 'Neu']
    axes.set_xticks([1, 2, 3, 4, 5])
    axes.set_xticklabels(xticklabels)
    axes.set_yticks(np.arange(1, 5.5, step=0.5))  # Set label locations.
    axes.yaxis.grid(True)
    plt.savefig(path)
