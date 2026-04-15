"""
03c_talk_length_spread_no_prophet.py — Same as 03b but excluding the prophet
"""

import matplotlib.pyplot as plt
from helpers import load_data

df, women, men = load_data()
df["word_count"] = df["talk"].apply(lambda t: len(str(t).split()))

# Exclude President of the Church
df = df[~df["calling"].str.contains("President of the Church|President of The Church", case=False, na=False, regex=True)]

years = sorted(df["year"].unique())
std_devs = []

for year in years:
    yr = df[df["year"] == year]
    std_devs.append(yr["word_count"].std())

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(years, std_devs, color="#8C7058", linewidth=1.2, marker="o", markersize=3)

ax.set_xlabel("Year")
ax.set_ylabel("Standard deviation (words)")
ax.set_title("How Much Do Talk Lengths Vary? — Excluding Prophet (1971–2025)")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("slides/03c_talk_length_spread_no_prophet.png", dpi=150)
plt.show()
print("Saved slides/03c_talk_length_spread_no_prophet.png")
