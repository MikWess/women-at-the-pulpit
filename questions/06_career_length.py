"""
06_career_length.py — How long do speakers serve at the pulpit?
Years between first and last talk.
"""

import matplotlib.pyplot as plt
from helpers import load_data

df, women, men = load_data()

# For each speaker: first year, last year, span
def career_stats(subset):
    careers = subset.groupby("speaker")["year"].agg(["min", "max", "count"])
    careers["span"] = careers["max"] - careers["min"]
    return careers

w_careers = career_stats(women)
m_careers = career_stats(men)

# Only look at speakers with 2+ talks (1 talk = span of 0, not meaningful)
w_multi = w_careers[w_careers["count"] >= 2]
m_multi = m_careers[m_careers["count"] >= 2]

print(f"CAREER LENGTH (speakers with 2+ talks)")
print(f"  Women: {len(w_multi)} speakers, avg span {w_multi['span'].mean():.1f} years, median {w_multi['span'].median():.0f} years")
print(f"  Men:   {len(m_multi)} speakers, avg span {m_multi['span'].mean():.1f} years, median {m_multi['span'].median():.0f} years")
print()

print("LONGEST WOMEN CAREERS:")
for name, row in w_multi.sort_values("span", ascending=False).head(10).iterrows():
    display = str(name).replace("By ", "")
    print(f"  {display:>35}  {row['span']:>2} years  ({int(row['min'])}-{int(row['max'])}, {int(row['count'])} talks)")

print()
print("LONGEST MEN CAREERS:")
for name, row in m_multi.sort_values("span", ascending=False).head(10).iterrows():
    display = str(name).replace("By ", "")
    print(f"  {display:>35}  {row['span']:>2} years  ({int(row['min'])}-{int(row['max'])}, {int(row['count'])} talks)")

# Graph: histogram of career spans
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

ax1.hist(w_multi["span"], bins=range(0, 35, 2), color="#B35488", alpha=0.8, edgecolor="white")
ax1.set_title("Women — Career Span")
ax1.set_xlabel("Years between first and last talk")
ax1.set_ylabel("Number of speakers")

ax2.hist(m_multi["span"], bins=range(0, 55, 2), color="#4A7FA5", alpha=0.8, edgecolor="white")
ax2.set_title("Men — Career Span")
ax2.set_xlabel("Years between first and last talk")

plt.suptitle("How Long Do Speakers Serve at the Pulpit?", y=1.02)
plt.tight_layout()
plt.savefig("slides/06_career_length.png", dpi=150, bbox_inches="tight")
plt.show()
print("Saved slides/06_career_length.png")
