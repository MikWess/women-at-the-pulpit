"""
03_talk_length.py — Average words per talk: women vs men
"""

from helpers import load_data

df, women, men = load_data()

# Add word count
df["word_count"] = df["talk"].apply(lambda t: len(str(t).split()))
women = df[df["is_woman"]]
men = df[~df["is_woman"]]

# Per year
print("PER YEAR:")
for year in sorted(df["year"].unique()):
    yw = women[women["year"] == year]
    ym = men[men["year"] == year]
    w_avg = yw["word_count"].mean() if len(yw) > 0 else 0
    m_avg = ym["word_count"].mean() if len(ym) > 0 else 0
    print(f"  {year}: Women {w_avg:6.0f} avg words ({len(yw)} talks)  |  Men {m_avg:6.0f} avg words ({len(ym)} talks)")
