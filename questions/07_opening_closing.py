"""
07_opening_closing.py — Has a woman ever opened or closed a conference?
"""

from helpers import load_data

df, women, men = load_data()

# Assign position within each session
df["position"] = df.groupby(["year", "season"]).cumcount() + 1
df["session_size"] = df.groupby(["year", "season"])["title"].transform("count")

# First talk and last talk of each session
firsts = df[df["position"] == 1]
lasts = df[df["position"] == df["session_size"]]

w_firsts = firsts[firsts["speaker"].isin(women["speaker"].unique()) & firsts["speaker"].apply(lambda s: s in women["speaker"].values)]
w_lasts = lasts[lasts["speaker"].isin(women["speaker"].unique()) & lasts["speaker"].apply(lambda s: s in women["speaker"].values)]

# Simpler: just check gender column
firsts_w = firsts[firsts["gender"] == "female"]
lasts_w = lasts[lasts["gender"] == "female"]

total_sessions = df.groupby(["year", "season"]).ngroups

print(f"Total conference sessions analyzed: {total_sessions}")
print()

print(f"OPENING TALKS BY WOMEN: {len(firsts_w)}")
if len(firsts_w) > 0:
    for _, r in firsts_w.iterrows():
        print(f"  {r['speaker']} — \"{r['title']}\" ({r['season']} {r['year']})")
else:
    print("  None. A woman has never opened a conference session.")

print()
print(f"CLOSING TALKS BY WOMEN: {len(lasts_w)}")
if len(lasts_w) > 0:
    for _, r in lasts_w.iterrows():
        print(f"  {r['speaker']} — \"{r['title']}\" ({r['season']} {r['year']})")
else:
    print("  None. A woman has never closed a conference session.")

print()

# Where DO women fall?
women_positions = df[df["gender"] == "female"].copy()
women_positions["relative"] = women_positions["position"] / women_positions["session_size"]

men_positions = df[df["gender"] == "male"].copy()
men_positions["relative"] = men_positions["position"] / men_positions["session_size"]

print(f"AVERAGE POSITION (0.0 = first, 1.0 = last):")
print(f"  Women: {women_positions['relative'].mean():.3f}")
print(f"  Men:   {men_positions['relative'].mean():.3f}")
