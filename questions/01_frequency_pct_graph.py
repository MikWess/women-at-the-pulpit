"""
01_frequency_pct_graph.py — Line chart: % of talks by women per session (biannual)
"""

import matplotlib.pyplot as plt
from helpers import load_data

df, women, men = load_data()

# Each conference session: year + season
sessions = df.groupby(["year", "season"]).size().reset_index(name="total")
women_sessions = women.groupby(["year", "season"]).size().reset_index(name="women")

merged = sessions.merge(women_sessions, on=["year", "season"], how="left")
merged["women"] = merged["women"].fillna(0).astype(int)
merged["pct"] = merged["women"] / merged["total"] * 100

# x-axis: year + 0.0 for April, year + 0.5 for October
merged["x"] = merged["year"] + (merged["season"] == "October").astype(float) * 0.5
merged = merged.sort_values("x")

# Plot
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(merged["x"], merged["pct"], color="#B35488", linewidth=1.2, zorder=2)
ax.scatter(merged["x"], merged["pct"], color="#B35488", s=20, zorder=3)

ax.set_xlabel("Year")
ax.set_ylabel("% of addresses by women")
ax.set_title("Women as % of All Speakers per Session (1971–2025)")
ax.set_ylim(0, merged["pct"].max() + 3)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("slides/01_frequency_pct.png", dpi=150)
plt.show()
print("Saved to slides/01_frequency_pct.png")
