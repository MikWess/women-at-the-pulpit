"""
03_talk_length_men_only.py — Average words per talk: men only
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from helpers import load_data

df, women, men = load_data()
df["word_count"] = df["talk"].apply(lambda t: len(str(t).split()))
men = df[~df["is_woman"]]

# ── PER YEAR ─────────────────────────────────────────────
years = sorted(men["year"].unique())
m_avgs = [men[men["year"] == y]["word_count"].mean() for y in years]

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(years, m_avgs, color="#4A7FA5", linewidth=1.2, marker="o", markersize=3)

ax.set_xlabel("Year")
ax.set_ylabel("Average words per talk")
ax.set_title("Average Talk Length: Men Only — Per Year (1971–2025)")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("slides/03_talk_length_men_only.png", dpi=150)
plt.show()
print("Saved slides/03_talk_length_men_only.png")

# ── PER SESSION ──────────────────────────────────────────
sessions = men.groupby(["year", "season"]).first().reset_index()[["year", "season"]]
sessions["x"] = sessions["year"] + (sessions["season"] == "October").astype(float) * 0.5
sessions = sessions.sort_values("x")

m_avgs_s = []
m_xs = []

for _, row in sessions.iterrows():
    mask = (men["year"] == row["year"]) & (men["season"] == row["season"])
    sm = men[mask]
    if len(sm) > 0:
        m_avgs_s.append(sm["word_count"].mean())
        m_xs.append(row["x"])

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(m_xs, m_avgs_s, color="#4A7FA5", linewidth=1, marker="o", markersize=2.5, alpha=0.8)

ax.set_xlabel("Year")
ax.set_ylabel("Average words per talk")
ax.set_title("Average Talk Length: Men Only — Per Session (1971–2025)")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("slides/03_talk_length_men_only_session.png", dpi=150)
plt.show()
print("Saved slides/03_talk_length_men_only_session.png")
