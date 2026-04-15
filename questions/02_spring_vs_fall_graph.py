"""
02_spring_vs_fall_graph.py — April vs October: % women per session, per year
"""

import matplotlib.pyplot as plt
from helpers import load_data

df, women, men = load_data()

years = sorted(df["year"].unique())
apr_pcts = []
oct_pcts = []

for year in years:
    apr_total = len(df[(df["year"] == year) & (df["season"] == "April")])
    apr_women = len(women[(women["year"] == year) & (women["season"] == "April")])
    oct_total = len(df[(df["year"] == year) & (df["season"] == "October")])
    oct_women = len(women[(women["year"] == year) & (women["season"] == "October")])

    apr_pcts.append((apr_women / apr_total * 100) if apr_total > 0 else 0)
    oct_pcts.append((oct_women / oct_total * 100) if oct_total > 0 else 0)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(years, apr_pcts, color="#B35488", linewidth=1.2, marker="o", markersize=4, label="April")
ax.plot(years, oct_pcts, color="#4A7FA5", linewidth=1.2, marker="o", markersize=4, label="October")

ax.set_xlabel("Year")
ax.set_ylabel("% of talks by women")
ax.set_title("Women as % of Speakers: April vs October (1971–2025)")
ax.set_ylim(0, 25)
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("slides/02_spring_vs_fall.png", dpi=150)
plt.show()
print("Saved to slides/02_spring_vs_fall.png")
