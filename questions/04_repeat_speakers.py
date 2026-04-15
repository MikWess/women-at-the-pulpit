"""
04_repeat_speakers.py — Do the same few women get invited back, or does the pool rotate?
"""

import matplotlib.pyplot as plt
from helpers import load_data

df, women, men = load_data()

# How many talks did each woman give?
w_counts = women.groupby("speaker").size().sort_values(ascending=False)
m_counts = men.groupby("speaker").size().sort_values(ascending=False)

print("TOP 15 WOMEN BY NUMBER OF TALKS:")
for name, count in w_counts.head(15).items():
    yrs = women[women["speaker"] == name]["year"]
    print(f"  {count:>2} talks  {name}  ({yrs.min()}-{yrs.max()})")

print()
print("TOP 15 MEN BY NUMBER OF TALKS:")
for name, count in m_counts.head(15).items():
    yrs = men[men["speaker"] == name]["year"]
    print(f"  {count:>2} talks  {name}  ({yrs.min()}-{yrs.max()})")

print()
print(f"Women: {len(w_counts)} unique speakers gave {len(women)} talks  (avg {len(women)/len(w_counts):.1f} talks each)")
print(f"Men:   {len(m_counts)} unique speakers gave {len(men)} talks  (avg {len(men)/len(m_counts):.1f} talks each)")
