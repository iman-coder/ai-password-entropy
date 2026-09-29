import matplotlib.pyplot as plt
import math

#mw_p (Mann–Whitney p-value results) Are values in group A generally larger or smaller than in group B?
#ks_p (Kolmogorov–Smirnov p-value results) Are the two distributions shaped differently, regardless of average value?

stats_results = {
    "Shannon": {
        "Claude vs Gemini": {"mw_p": 1.600e-41, "ks_p": 2.209e-59},
        "Claude vs ChatGPT": {"mw_p": 1.334e-25, "ks_p": 2.621e-22},
        "Gemini vs ChatGPT": {"mw_p": 4.795e-39, "ks_p": 2.209e-59},
        "Claude vs Human": {"mw_p": 1.090e-24, "ks_p": 1.407e-31},
        "Gemini vs Human": {"mw_p": 5.781e-01, "ks_p": 3.856e-07},
        "ChatGPT vs Human": {"mw_p": 6.389e-13, "ks_p": 1.421e-17},
        "Claude vs RockYou": {"mw_p": 9.877e-62, "ks_p": 1.406e-144},
        "Gemini vs RockYou": {"mw_p": 9.495e-62, "ks_p": 1.406e-144},
        "ChatGPT vs RockYou": {"mw_p": 1.034e-61, "ks_p": 1.406e-144},
        "Random vs Claude": {"mw_p": 1.156e-17, "ks_p": 1.767e-16},
        "Random vs Gemini": {"mw_p": 5.411e-39, "ks_p": 2.209e-59},
        "Random vs ChatGPT": {"mw_p": 2.540e-09, "ks_p": 2.359e-10},
    },
    "Effective": {
        "Claude vs Gemini": {"mw_p": 3.522e-45, "ks_p": 2.209e-59},
        "Claude vs ChatGPT": {"mw_p": 7.374e-20, "ks_p": 4.528e-17},
        "Gemini vs ChatGPT": {"mw_p": 7.989e-40, "ks_p": 2.209e-59},
        "Claude vs Human": {"mw_p": 3.222e-27, "ks_p": 2.195e-25},
        "Gemini vs Human": {"mw_p": 2.399e-01, "ks_p": 1.040e-07},
        "ChatGPT vs Human": {"mw_p": 7.335e-10, "ks_p": 5.384e-14},
        "Claude vs RockYou": {"mw_p": 5.724e-64, "ks_p": 1.406e-144},
        "Gemini vs RockYou": {"mw_p": 5.724e-64, "ks_p": 1.406e-144},
        "ChatGPT vs RockYou": {"mw_p": 6.294e-64, "ks_p": 1.406e-144},
        "Random vs Claude": {"mw_p": 1.0, "ks_p": 1.0},
        "Random vs Gemini": {"mw_p": 3.522e-45, "ks_p": 2.209e-59},
        "Random vs ChatGPT": {"mw_p": 7.374e-20, "ks_p": 4.528e-17},
    },
    "Ratio": {
        "Claude vs Gemini": {"mw_p": 1.0, "ks_p": 1.0},
        "Claude vs ChatGPT": {"mw_p": 6.040e-05, "ks_p": 2.112e-01},
        "Gemini vs ChatGPT": {"mw_p": 6.040e-05, "ks_p": 2.112e-01},
        "Claude vs Human": {"mw_p": 3.686e-21, "ks_p": 4.063e-15},
        "Gemini vs Human": {"mw_p": 3.686e-21, "ks_p": 4.063e-15},
        "ChatGPT vs Human": {"mw_p": 6.153e-14, "ks_p": 1.494e-11},
        "Claude vs RockYou": {"mw_p": 2.972e-68, "ks_p": 1.406e-144},
        "Gemini vs RockYou": {"mw_p": 2.972e-68, "ks_p": 1.406e-144},
        "ChatGPT vs RockYou": {"mw_p": 3.123e-68, "ks_p": 1.406e-144},
        "Random vs Claude": {"mw_p": 1.0, "ks_p": 1.0},
        "Random vs Gemini": {"mw_p": 1.0, "ks_p": 1.0},
        "Random vs ChatGPT": {"mw_p": 6.040e-05, "ks_p": 2.112e-01},
    }
}

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
#plot_pvalues(stats_results, "mw_p")
#plot_pvalues(stats_results, "ks_p")

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

plot_significance_heatmap(stats_results, "mw_p")
plot_significance_heatmap(stats_results, "ks_p")