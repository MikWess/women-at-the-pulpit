"""
02_spring_vs_fall.py — Are women more likely to speak in April or October?
"""

from helpers import load_data

df, women, men = load_data()

# For each year, get % women in April vs October
april_wins = 0
october_wins = 0
ties = 0

for year in sorted(df["year"].unique()):
    apr_total = len(df[(df["year"] == year) & (df["season"] == "April")])
    apr_women = len(women[(women["year"] == year) & (women["season"] == "April")])
    oct_total = len(df[(df["year"] == year) & (df["season"] == "October")])
    oct_women = len(women[(women["year"] == year) & (women["season"] == "October")])

    apr_pct = (apr_women / apr_total * 100) if apr_total > 0 else 0
    oct_pct = (oct_women / oct_total * 100) if oct_total > 0 else 0

    if apr_pct > oct_pct:
        winner = "APRIL"
        april_wins += 1
    elif oct_pct > apr_pct:
        winner = "OCTOBER"
        october_wins += 1
    else:
        winner = "TIE"
        ties += 1

    print(f"{year}: April {apr_pct:5.1f}% ({apr_women}/{apr_total})  |  October {oct_pct:5.1f}% ({oct_women}/{oct_total})  →  {winner}")

print()
print(f"April had more women:   {april_wins} years")
print(f"October had more women: {october_wins} years")
print(f"Tied:                   {ties} years")
