#!/usr/bin/env python3
"""
Local scraper for LDS General Conference talks.
Adapted from GeneralConferenceScraper (Colab version) to run locally.
Scrapes talks from 1971–present (~50 years).
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import unicodedata
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = "https://www.churchofjesuschrist.org"
HEADERS = {"User-Agent": "Mozilla/5.0 (conference-research)"}
START_YEAR = 1971  # ~50 years of data


def get_soup(url):
    """Fetch and parse a page."""
    try:
        r = requests.get(url, headers=HEADERS, allow_redirects=True, timeout=15)
        r.raise_for_status()
        return BeautifulSoup(r.content, "html.parser")
    except requests.RequestException as e:
        print(f"  ✗ {url}: {e}")
        return None


def scrape_conference_pages():
    """Get URLs for every conference (year/month) from the main page."""
    main_url = f"{BASE}/study/general-conference?lang=eng"
    soup = get_soup(main_url)
    if not soup:
        return []

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Match individual conference pages (e.g. /2023/04)
        m = re.search(r"/study/general-conference/(\d{4})/(04|10)", href)
        if m:
            year = int(m.group(1))
            if year >= START_YEAR:
                links.append(BASE + href.split("?")[0] + "?lang=eng")
        # Match decade pages (e.g. /19701979)
        elif re.search(r"/study/general-conference/\d{4}\d{4}", href):
            decade_soup = get_soup(BASE + href)
            if decade_soup:
                for da in decade_soup.find_all("a", href=True):
                    dm = re.search(r"/study/general-conference/(\d{4})/(04|10)", da["href"])
                    if dm and int(dm.group(1)) >= START_YEAR:
                        links.append(BASE + da["href"].split("?")[0] + "?lang=eng")

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for url in links:
        normalized = url.split("?")[0]
        if normalized not in seen:
            seen.add(normalized)
            unique.append(url)

    print(f"Found {len(unique)} conferences (from {START_YEAR})")
    return unique


def scrape_talk_urls(conference_url):
    """Get individual talk URLs from a conference page."""
    soup = get_soup(conference_url)
    if not soup:
        return []

    talk_links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if re.search(r"/study/general-conference/\d{4}/(04|10)/[\w-]+", href):
            clean = BASE + href.split("?")[0] + "?lang=eng"
            if not clean.endswith("session?lang=eng"):
                talk_links.add(clean)

    return list(talk_links)


def scrape_talk(url):
    """Scrape a single talk's data."""
    try:
        soup = get_soup(url)
        if not soup:
            return None

        title_tag = soup.find("h1", {"id": "title1"}) or soup.find("h1")
        title = title_tag.text.strip() if title_tag else "No Title Found"

        author_tag = soup.find("p", {"class": "author-name"})
        speaker = author_tag.text.strip() if author_tag else "No Speaker Found"
        # Clean titles from speaker name
        speaker = re.sub(r'\b(By\s+)?(Elder|President|Sister|Brother)\s+', '', speaker, flags=re.IGNORECASE).strip()

        calling_tag = soup.find("p", {"class": "author-role"})
        calling = calling_tag.text.strip() if calling_tag else "No Calling Found"

        body = soup.find("div", {"class": "body-block"})
        text = "\n\n".join(p.text.strip() for p in body.find_all("p")) if body else ""

        year_match = re.search(r'/(\d{4})/', url)
        year = int(year_match.group(1)) if year_match else 0
        season = "April" if "/04/" in url else "October"

        return {
            "title": title,
            "speaker": speaker,
            "calling": calling,
            "year": year,
            "season": season,
            "url": url,
            "talk": text,
        }
    except Exception as e:
        print(f"  ✗ scrape failed: {url} — {e}")
        return None


def main():
    print("=" * 60)
    print("General Conference Scraper (local)")
    print(f"Scraping talks from {START_YEAR} to present")
    print("=" * 60)

    t0 = time.time()

    # Step 1: Get conference pages
    conference_urls = scrape_conference_pages()

    # Step 2: Get all talk URLs
    print("\nGathering talk URLs...")
    all_talk_urls = []
    for i, curl in enumerate(conference_urls):
        urls = scrape_talk_urls(curl)
        all_talk_urls.extend(urls)
        if (i + 1) % 10 == 0:
            print(f"  {i+1}/{len(conference_urls)} conferences scanned ({len(all_talk_urls)} talks so far)")

    # Deduplicate
    all_talk_urls = list(set(all_talk_urls))
    print(f"\nTotal unique talks to scrape: {len(all_talk_urls)}")

    # Step 3: Scrape talks in parallel
    print("\nScraping talks (10 threads)...")
    results = []
    done = 0
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(scrape_talk, url): url for url in all_talk_urls}
        for future in as_completed(futures):
            done += 1
            result = future.result()
            if result and result["talk"]:
                results.append(result)
            if done % 100 == 0:
                print(f"  {done}/{len(all_talk_urls)} scraped ({len(results)} successful)")

    # Step 4: Build dataframe
    df = pd.DataFrame(results)
    for col in df.columns:
        df[col] = df[col].apply(lambda x: unicodedata.normalize("NFC", x) if isinstance(x, str) else x)

    df = df.sort_values(["year", "season"]).reset_index(drop=True)

    # Remove non-talk rows
    df = df[~df["title"].str.contains(r"morning|afternoon|evening", case=False, na=False)]
    df = df[~df["calling"].str.contains("Church Auditing", na=False)]
    df = df[df["speaker"] != "No Speaker Found"]
    df = df[df["talk"].str.len() > 100]  # Filter out stubs

    out = "data/conference_talks.csv"
    df.to_csv(out, index=False)

    elapsed = time.time() - t0
    print(f"\n{'=' * 60}")
    print(f"Done! {len(df)} talks saved to {out}")
    print(f"Year range: {df['year'].min()}–{df['year'].max()}")
    print(f"Unique speakers: {df['speaker'].nunique()}")
    print(f"Time: {elapsed:.0f}s")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
