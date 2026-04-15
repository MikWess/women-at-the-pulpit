"""
08_politeness.py — Measure politeness/deference using ConvoKit's classifier.

ConvoKit's PolitenessStrategies is based on Brown & Levinson's politeness theory
and was built by computational linguists at Cornell. It detects:

  Gratitude       — "thank you", "grateful"
  Apologizing     — "I apologize", "sorry"
  Hedges          — "perhaps", "maybe", "I think"
  Deference       — formal/deferential framing
  Please          — direct politeness marker
  Subjunctive     — "could you", "would you" (indirect requests)
  1st person      — "I" statements
  Positive/Negative politeness markers

We run it on every talk and compare women vs men.
"""

from convokit import PolitenessStrategies, TextParser, Speaker, Utterance, Corpus
from helpers import load_data
import matplotlib.pyplot as plt

df, women, men = load_data()

# ── Run ConvoKit on every talk ──────────────────────────────────────
print("Running politeness classifier on all talks (this takes a minute)...")

tp = TextParser(verbosity=0)
ps = PolitenessStrategies()

# Build ConvoKit corpus from our talks
utterances = []
for idx, row in df.iterrows():
    utt = Utterance(
        id=str(idx),
        text=str(row["talk"])[:5000],  # cap length for speed
        speaker=Speaker(id=row["speaker"]),
    )
    utt.meta["gender"] = row["gender"]
    utt.meta["year"] = row["year"]
    utterances.append(utt)

corpus = Corpus(utterances=utterances)
corpus = tp.transform(corpus)
corpus = ps.transform(corpus)

# ── Extract features ────────────────────────────────────────────────
# Features we care about for deference
DEFERENCE_FEATURES = [
    "feature_politeness_==Gratitude==",
    "feature_politeness_==Apologizing==",
    "feature_politeness_==Hedges==",
    "feature_politeness_==Deference==",
    "feature_politeness_==Please==",
    "feature_politeness_==SUBJUNCTIVE==",
    "feature_politeness_==HASHEDGE==",
]

ASSERTIVE_FEATURES = [
    "feature_politeness_==Direct_start==",
    "feature_politeness_==Direct_question==",
    "feature_politeness_==Factuality==",
    "feature_politeness_==INDICATIVE==",
]

# Collect scores
results = []
for utt in corpus.iter_utterances():
    feats = utt.meta.get("politeness_strategies", {})
    results.append({
        "gender": utt.meta["gender"],
        "year": utt.meta["year"],
        **{f: feats.get(f, 0) for f in DEFERENCE_FEATURES + ASSERTIVE_FEATURES},
    })

import pandas as pd
scores = pd.DataFrame(results)

# ── Compare women vs men ────────────────────────────────────────────
print()
print("=" * 60)
print("  POLITENESS FEATURES: WOMEN VS MEN")
print("=" * 60)
print()

w_scores = scores[scores["gender"] == "female"]
m_scores = scores[scores["gender"] == "male"]

print(f"{'Feature':<45} {'Women':>8} {'Men':>8} {'Diff':>8}")
print("-" * 70)

all_features = DEFERENCE_FEATURES + ASSERTIVE_FEATURES
for feat in all_features:
    short_name = feat.replace("feature_politeness_==", "").replace("==", "")
    w_avg = w_scores[feat].mean()
    m_avg = m_scores[feat].mean()
    diff = w_avg - m_avg
    marker = " ***" if abs(diff) > 0.05 else ""
    print(f"  {short_name:<43} {w_avg:>8.3f} {m_avg:>8.3f} {diff:>+8.3f}{marker}")

# ── Composite deference score ───────────────────────────────────────
print()
print("=" * 60)
print("  COMPOSITE SCORES")
print("=" * 60)
print()

scores["deference_score"] = sum(scores[f] for f in DEFERENCE_FEATURES) / len(DEFERENCE_FEATURES)
scores["assertive_score"] = sum(scores[f] for f in ASSERTIVE_FEATURES) / len(ASSERTIVE_FEATURES)

w = scores[scores["gender"] == "female"]
m = scores[scores["gender"] == "male"]

print(f"Deference score — Women: {w['deference_score'].mean():.3f}, Men: {m['deference_score'].mean():.3f}")
print(f"Assertive score — Women: {w['assertive_score'].mean():.3f}, Men: {m['assertive_score'].mean():.3f}")

# ── Graph: deference over time ──────────────────────────────────────
years = sorted(scores["year"].unique())
w_by_year = []
m_by_year = []
years_with_w = []

for year in years:
    wy = w[w["year"] == year]
    my = m[m["year"] == year]
    m_by_year.append(my["deference_score"].mean())
    if len(wy) > 0:
        w_by_year.append(wy["deference_score"].mean())
        years_with_w.append(year)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(years, m_by_year, color="#4A7FA5", linewidth=1.2, marker="o", markersize=3, label="Men")
ax.plot(years_with_w, w_by_year, color="#B35488", linewidth=1.2, marker="o", markersize=3, label="Women")

ax.set_xlabel("Year")
ax.set_ylabel("Deference score (higher = more deferential)")
ax.set_title("Deference in Conference Talks: Women vs Men (1971–2025)")
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("slides/08_politeness.png", dpi=150)
plt.show()
print("\nSaved slides/08_politeness.png")
