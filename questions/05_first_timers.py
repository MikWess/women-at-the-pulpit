"""
05_first_timers.py — How many new women speakers are introduced each year?
"""

import matplotlib.pyplot as plt
from helpers import load_data

df, women, men = load_data()

years = sorted(df["year"].unique())
seen_women = set()
seen_men = set()
new_w = []
new_m = []

for year in years:
    yw = women[women["year"] == year]["speaker"].unique()
    ym = men[men["year"] == year]["speaker"].unique()

    first_time_w = [s for s in yw if s not in seen_women]
    first_time_m = [s for s in ym if s not in seen_men]

    new_w.append(len(first_time_w))
    new_m.append(len(first_time_m))

    seen_women.update(yw)
    seen_men.update(ym)

# Graph
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(years, new_w, color="#B35488", linewidth=1.2, marker="o", markersize=3, label="New women")
ax.plot(years, new_m, color="#4A7FA5", linewidth=1.2, marker="o", markersize=3, label="New men")

ax.set_xlabel("Year")
ax.set_ylabel("First-time speakers")
ax.set_title("New Speakers Introduced Per Year (1971–2025)")
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("slides/05_first_timers.png", dpi=150)
plt.show()
print("Saved slides/05_first_timers.png")
