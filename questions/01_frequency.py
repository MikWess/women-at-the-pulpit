"""
01_frequency.py — How often do women speak at General Conference?

For each year: how many total talks, how many by women, what percentage.
"""

from helpers import load_data

df, women, men = load_data()

# For each year, count total talks and women's talks
for year in sorted(df["year"].unique()):
    year_talks = df[df["year"] == year]
    year_women = women[women["year"] == year]

    total = len(year_talks)
    w = len(year_women)
    pct = (w / total * 100) if total > 0 else 0

    print(f"{year}: {w}/{total} women's talks ({pct:.1f}%)")
