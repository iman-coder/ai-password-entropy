from scipy.stats import mannwhitneyu, ks_2samp

def compare_distributions(sample_a, sample_b, name_a, name_b, metric):
    """
    Statistical comparison between two password groups.
    """

    mw_stat, mw_p = mannwhitneyu(sample_a, sample_b, alternative="two-sided")
    ks_stat, ks_p = ks_2samp(sample_a, sample_b)

    print(f"\n=== {metric}: {name_a} vs {name_b} ===")
    print(f"Mann–Whitney U: statistic={mw_stat:.3f}, p-value={mw_p:.3e}")
    print(f"Kolmogorov–Smirnov: statistic={ks_stat:.3f}, p-value={ks_p:.3e}")

    if mw_p < 0.05:
        print("Significant difference (median)")
    else:
        print("No significant difference (median)")

    if ks_p < 0.05:
        print("Distributions differ significantly")
    else:
        print("Distributions are similar")

    return mw_p, ks_p
