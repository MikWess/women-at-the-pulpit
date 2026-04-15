# Women at the Pulpit

Interactive word-frequency explorer for LDS General Conference talks, filterable by speaker gender.

## Run locally

```
python3 -m http.server 8000
```

Then open http://localhost:8000/

## Data

- `data/talks.json` — all talks (used by the viewer)
- `data/conference_talks.csv` / `speaker_genders.csv` — source data for the scrape pipeline
- `scrape.py`, `tag_sessions.py`, `build_gender_table.py`, `word_frequency.py` — build scripts

## Hosted on

Vercel (static site).
