import json
import math
from collections import Counter
import matplotlib.pyplot as plt
from stats import compare_distributions

try:
    from zxcvbn import zxcvbn
    ZXCVBN_AVAILABLE = True
except ImportError:
    ZXCVBN_AVAILABLE = False


# -------------------------------
# Loading
# -------------------------------

def load_passwords(path, limit=None):
    passwords = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            pwd = line.strip()
            if pwd:
                passwords.append(pwd)
            if limit and len(passwords) >= limit:
                break
    return passwords


# -------------------------------
# Metrics
# -------------------------------

def shannon_entropy(password):
    if not password:
        return 0.0

    counts = Counter(password)
    length = len(password)

    entropy = 0.0
    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)

    return entropy * length


def charset_size(password):
    size = 0
    if any(c.islower() for c in password):
        size += 26
    if any(c.isupper() for c in password):
        size += 26
    if any(c.isdigit() for c in password):
        size += 10
    if any(not c.isalnum() for c in password):
        size += 33
    return size


def effective_entropy(password):
    length = len(password)
    charset = charset_size(password)

    if length == 0 or charset == 0:
        return 0.0

    entropy = math.log2(charset ** length)

    # penalties = attacker-aware adjustments
    if len(set(password)) < length / 2:
        entropy *= 0.7

    if password.islower() or password.isupper():
        entropy *= 0.85

    if password.isdigit():
        entropy *= 0.6

    return entropy


def search_space_ratio(password):
    length = len(password)
    if length == 0:
        return 0.0

    ideal_entropy = math.log2(94 ** length)
    return effective_entropy(password) / ideal_entropy


def zxcvbn_score(password):
    if not ZXCVBN_AVAILABLE:
        return None
    return zxcvbn(password)["score"]


# -------------------------------
# Analysis
# -------------------------------

def analyze(passwords):
    results = {
        "shannon": [],
        "effective": [],
        "ratio": [],
        "zxcvbn": []
    }

    for p in passwords:
        results["shannon"].append(shannon_entropy(p))
        results["effective"].append(effective_entropy(p))
        results["ratio"].append(search_space_ratio(p))

        if ZXCVBN_AVAILABLE:
            results["zxcvbn"].append(zxcvbn_score(p))

    return results


# -------------------------------
# Plotting
# -------------------------------

def plot_box(data, labels, title, ylabel):
    plt.figure()
    plt.boxplot(data, labels=labels)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()


# -------------------------------
# Main
# -------------------------------

# Sample sizes used for the published article. Only the first N passwords
# of each file are analysed; changing these changes the reported results.
SAMPLE_LIMIT = 100
ROCKYOU_LIMIT = 1000

RESULTS_FILE = "results.json"

if __name__ == "__main__":
    # ===== Load password datasets =====
    random_pw = load_passwords("Randompasswords.txt", limit=SAMPLE_LIMIT)

    claude_pw = load_passwords("AI_password_claude.txt", limit=SAMPLE_LIMIT)
    gemini_pw = load_passwords("AI_password_gemini.txt", limit=SAMPLE_LIMIT)
    chatgpt_pw = load_passwords("AI_password_chatgpt.txt", limit=SAMPLE_LIMIT)

    human_pw = load_passwords("PasswordsHuman.txt")
    rockyou_pw = load_passwords("rockyou.txt", limit=ROCKYOU_LIMIT)

    # ===== Analyze datasets =====
    random_res = analyze(random_pw)

    claude_res = analyze(claude_pw)
    gemini_res = analyze(gemini_pw)
    chatgpt_res = analyze(chatgpt_pw)

    human_res = analyze(human_pw)
    rockyou_res = analyze(rockyou_pw)

    # ===== Labels =====
    labels = [
        "Random",
        "Claude",
        "Gemini",
        "ChatGPT",
        "Human",
        "RockYou"
    ]

    # ===== Boxplots =====
    plot_box(
        [
            random_res["shannon"],
            claude_res["shannon"],
            gemini_res["shannon"],
            chatgpt_res["shannon"],
            human_res["shannon"],
            rockyou_res["shannon"]
        ],
        labels,
        "Shannon Entropy Distribution",
        "Entropy (bits)"
    )

    plot_box(
        [
            random_res["effective"],
            claude_res["effective"],
            gemini_res["effective"],
            chatgpt_res["effective"],
            human_res["effective"],
            rockyou_res["effective"]
        ],
        labels,
        "Effective Entropy Distribution",
        "Entropy (bits)"
    )

    plot_box(
        [
            random_res["ratio"],
            claude_res["ratio"],
            gemini_res["ratio"],
            chatgpt_res["ratio"],
            human_res["ratio"],
            rockyou_res["ratio"]
        ],
        labels,
        "Search Space Reduction Ratio",
        "Effective / Ideal Entropy"
    )

    if ZXCVBN_AVAILABLE:
        plot_box(
            [
                random_res["zxcvbn"],
                claude_res["zxcvbn"],
                gemini_res["zxcvbn"],
                chatgpt_res["zxcvbn"],
                human_res["zxcvbn"],
                rockyou_res["zxcvbn"]
            ],
            labels,
            "zxcvbn Score Distribution",
            "Score (0–4)"
        )

    # ===== Statistical comparisons =====
    print("\n=== Statistical Comparisons ===")

    results = {
        "Random": random_res,
        "Claude": claude_res,
        "Gemini": gemini_res,
        "ChatGPT": chatgpt_res,
        "Human": human_res,
        "RockYou": rockyou_res
    }

    # Short names are the row labels used by plots.py
    metrics = {
        "Shannon": ("Shannon entropy", "shannon"),
        "Effective": ("Effective entropy", "effective"),
        "Ratio": ("Search space ratio", "ratio")
    }

    pairs = [
        ("Claude", "Gemini"),
        ("Claude", "ChatGPT"),
        ("Gemini", "ChatGPT"),

        ("Claude", "Human"),
        ("Gemini", "Human"),
        ("ChatGPT", "Human"),

        ("Claude", "RockYou"),
        ("Gemini", "RockYou"),
        ("ChatGPT", "RockYou"),

        ("Random", "Claude"),
        ("Random", "Gemini"),
        ("Random", "ChatGPT")
    ]

    stats_results = {}
    for short_name, (metric_name, key) in metrics.items():
        stats_results[short_name] = {}
        for a, b in pairs:
            mw_p, ks_p = compare_distributions(
                results[a][key],
                results[b][key],
                a, b,
                metric_name
            )
            stats_results[short_name][f"{a} vs {b}"] = {
                "mw_p": float(mw_p),
                "ks_p": float(ks_p)
            }

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats_results, f, indent=2)
    print(f"\nSaved p-values to {RESULTS_FILE}")
