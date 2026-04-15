"""
03_talk_length_graph.py — Average words per talk: women vs men
Two graphs: per year and per session
"""

import matplotlib.pyplot as plt
from helpers import load_data

df, women, men = load_data()
df["word_count"] = df["talk"].apply(lambda t: len(str(t).split()))
women = df[df["is_woman"]]
men = df[~df["is_woman"]]

# ── PER YEAR ─────────────────────────────────────────────
years = sorted(df["year"].unique())
w_avgs_yr = []
m_avgs_yr = []
years_with_women = []

for year in years:
    yw = women[women["year"] == year]
    ym = men[men["year"] == year]
    m_avgs_yr.append(ym["word_count"].mean())
    if len(yw) > 0:
        w_avgs_yr.append(yw["word_count"].mean())
        years_with_women.append(year)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(years, m_avgs_yr, color="#4A7FA5", linewidth=1.2, marker="o", markersize=3, label="Men")
ax.plot(years_with_women, w_avgs_yr, color="#B35488", linewidth=1.2, marker="o", markersize=3, label="Women")

ax.set_xlabel("Year")
ax.set_ylabel("Average words per talk")
ax.set_title("Average Talk Length: Women vs Men — Per Year (1971–2025)")
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("slides/03_talk_length_year.png", dpi=150)
plt.show()
print("Saved slides/03_talk_length_year.png")

# ── PER SESSION ──────────────────────────────────────────
sessions = df.groupby(["year", "season"]).first().reset_index()[["year", "season"]]
sessions["x"] = sessions["year"] + (sessions["season"] == "October").astype(float) * 0.5
sessions = sessions.sort_values("x")

w_avgs_s = []
m_avgs_s = []
w_xs = []
m_xs = []

for _, row in sessions.iterrows():
    mask = (df["year"] == row["year"]) & (df["season"] == row["season"])
    sw = df[mask & df["is_woman"]]
    sm = df[mask & ~df["is_woman"]]
    if len(sm) > 0:
        m_avgs_s.append(sm["word_count"].mean())
        m_xs.append(row["x"])
    if len(sw) > 0:
        w_avgs_s.append(sw["word_count"].mean())
        w_xs.append(row["x"])

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(m_xs, m_avgs_s, color="#4A7FA5", linewidth=1, marker="o", markersize=2.5, label="Men", alpha=0.8)
ax.plot(w_xs, w_avgs_s, color="#B35488", linewidth=1, marker="o", markersize=2.5, label="Women", alpha=0.8)

ax.set_xlabel("Year")
ax.set_ylabel("Average words per talk")
ax.set_title("Average Talk Length: Women vs Men — Per Session (1971–2025)")
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("slides/03_talk_length_session.png", dpi=150)
plt.show()
print("Saved slides/03_talk_length_session.png")
