"""
01_frequency_graph.py — Line chart: # of women's talks per session (biannual)
"""

import matplotlib.pyplot as plt
from helpers import load_data

df, women, men = load_data()

# Each conference is a session: e.g. "1995 April", "1995 October"
# This gives us 2 data points per year
sessions = df.groupby(["year", "season"]).size().reset_index(name="total")
women_sessions = women.groupby(["year", "season"]).size().reset_index(name="women")

merged = sessions.merge(women_sessions, on=["year", "season"], how="left")
merged["women"] = merged["women"].fillna(0).astype(int)

# Create an x-axis value: year + 0.0 for April, year + 0.5 for October
merged["x"] = merged["year"] + (merged["season"] == "October").astype(float) * 0.5

# Sort by x
merged = merged.sort_values("x")

# Plot
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(merged["x"], merged["women"], color="#B35488", linewidth=1.2, zorder=2)
ax.scatter(merged["x"], merged["women"], color="#B35488", s=20, zorder=3)

ax.set_xlabel("Year")
ax.set_ylabel("Number of women who spoke")
ax.set_title("Women's Talks at General Conference by Session (1971–2025)")
ax.set_ylim(0, merged["women"].max() + 2)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("slides/01_frequency.png", dpi=150)
plt.show()
print("Saved to slides/01_frequency.png")
