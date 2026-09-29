import matplotlib.pyplot as plt
import json
import math

#mw_p (Mann–Whitney p-value results) Are values in group A generally larger or smaller than in group B?
#ks_p (Kolmogorov–Smirnov p-value results) Are the two distributions shaped differently, regardless of average value?

# p-values are produced by metrics.py and saved to results.json
RESULTS_FILE = "results.json"


def load_results(path=RESULTS_FILE):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def plot_pvalues(stats_results, test_type="mw_p"):
    comparisons = list(next(iter(stats_results.values())).keys())
    metrics = stats_results.keys()

    for metric in metrics:
        pvals = [stats_results[metric][c][test_type] for c in comparisons]

        plt.figure()
        plt.bar(comparisons, [math.log10(p) if p > 0 else -300 for p in pvals])
        plt.axhline(math.log10(0.05), linestyle="--", label="p = 0.05")
        plt.title(f"{metric} — {test_type} (log10 scale)")
        plt.ylabel("log10(p-value)")
        plt.xticks(rotation=30, ha="right")
        plt.legend()
        plt.tight_layout()
        plt.show()

def plot_significance_heatmap(stats_results, test_type="mw_p"):
    metrics = list(stats_results.keys())
    comparisons = list(next(iter(stats_results.values())).keys())

    data = []
    for metric in metrics:
        row = []
        for comp in comparisons:
            p = stats_results[metric][comp][test_type]
            row.append(-math.log10(p) if p > 0 else 300)
        data.append(row)

    plt.figure()
    plt.imshow(data)
    plt.colorbar(label="-log10(p-value)")
    plt.xticks(range(len(comparisons)), comparisons, rotation=30, ha="right")
    plt.yticks(range(len(metrics)), metrics)
    plt.title(f"Statistical significance heatmap ({test_type})")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    stats_results = load_results()
    plot_significance_heatmap(stats_results, "mw_p")
    plot_significance_heatmap(stats_results, "ks_p")
