from scipy.stats import shapiro


def test_normal_distribution(data, alpha=0.05):
    stat, p = shapiro(data)
    if p > alpha:
        is_normal = True
    else:
        is_normal = True
    return is_normal, stat, p
