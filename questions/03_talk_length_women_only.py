"""
03_talk_length_women_only.py — Average words per talk: women only
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from helpers import load_data

df, women, men = load_data()
df["word_count"] = df["talk"].apply(lambda t: len(str(t).split()))
women = df[df["is_woman"]]

# ── PER YEAR ─────────────────────────────────────────────
years = sorted(women["year"].unique())
w_avgs = [women[women["year"] == y]["word_count"].mean() for y in years]

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(years, w_avgs, color="#B35488", linewidth=1.2, marker="o", markersize=3)

ax.set_xlabel("Year")
ax.set_ylabel("Average words per talk")
ax.set_title("Average Talk Length: Women Only — Per Year")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("slides/03_talk_length_women_only.png", dpi=150)
plt.show()
print("Saved slides/03_talk_length_women_only.png")

# ── PER SESSION ──────────────────────────────────────────
sessions = women.groupby(["year", "season"]).first().reset_index()[["year", "season"]]
sessions["x"] = sessions["year"] + (sessions["season"] == "October").astype(float) * 0.5
sessions = sessions.sort_values("x")

w_avgs_s = []
w_xs = []

for _, row in sessions.iterrows():
    mask = (women["year"] == row["year"]) & (women["season"] == row["season"])
    sw = women[mask]
    if len(sw) > 0:
        w_avgs_s.append(sw["word_count"].mean())
        w_xs.append(row["x"])

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(w_xs, w_avgs_s, color="#B35488", linewidth=1, marker="o", markersize=2.5, alpha=0.8)

ax.set_xlabel("Year")
ax.set_ylabel("Average words per talk")
ax.set_title("Average Talk Length: Women Only — Per Session")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("slides/03_talk_length_women_only_session.png", dpi=150)
plt.show()
print("Saved slides/03_talk_length_women_only_session.png")
