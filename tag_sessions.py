"""
tag_sessions.py — Scrape session labels for each talk from the church website.
Maps each talk URL to its session: general, women, priesthood.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

df = pd.read_csv("data/conference_talks.csv")

# Get unique conference pages (year/season combos)
conferences = df[["year", "season"]].drop_duplicates().sort_values(["year", "season"])

# For each conference, fetch the page and map talk URLs to session names
session_map = {}  # url -> session_type

for _, row in conferences.iterrows():
    year = row["year"]
    month = "04" if row["season"] == "April" else "10"
    page_url = f"https://www.churchofjesuschrist.org/study/general-conference/{year}/{month}?lang=eng"

    try:
        r = requests.get(page_url, timeout=15)
        soup = BeautifulSoup(r.content, "html.parser")
    except Exception as e:
        print(f"  FAILED {year} {row['season']}: {e}")
        continue

    # Walk through the page structure:
    # Session headers (h3/h4) are followed by talk links
    current_session = "general"

    # Find all elements in order
    for element in soup.find_all(["h2", "h3", "h4", "a"]):
        if element.name in ["h2", "h3", "h4"]:
            text = element.get_text().strip().lower()
            if "priesthood" in text and "session" in text:
                current_session = "priesthood"
            elif "women" in text and ("session" in text or "meeting" in text):
                current_session = "women"
            elif "young women" in text:
                current_session = "women"
            elif "relief society" in text:
                current_session = "women"
            elif "session" in text:
                current_session = "general"
        elif element.name == "a" and element.get("href"):
            href = element["href"]
            if re.search(r"/study/general-conference/\d{4}/(04|10)/[\w-]+", href):
                full_url = "https://www.churchofjesuschrist.org" + href.split("?")[0] + "?lang=eng"
                session_map[full_url] = current_session

    count = sum(1 for url in session_map if f"/{year}/{month}/" in url)
    print(f"  {year} {row['season']}: {count} talks tagged")
    time.sleep(0.3)  # be polite

# Map to our dataframe
def get_session(url):
    clean = url.split("?")[0] + "?lang=eng"
    return session_map.get(clean, "general")

df["session_type"] = df["url"].apply(get_session)

# Print summary
print()
print("Session type distribution:")
print(df["session_type"].value_counts())
print()
print("By gender:")
print(df.groupby(["session_type", "gender"]).size().unstack(fill_value=0))

# Save
df.to_csv("data/conference_talks.csv", index=False)
print("\nSaved to data/conference_talks.csv")
