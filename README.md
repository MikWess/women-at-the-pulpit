# Women at the Pulpit

A static explorer for a bundled snapshot of 4,001 LDS General Conference talks spanning 1971–2025. Compare language, speaking frequency, talk length, speakers, and topics across the recorded gender and session categories.

## Three useful questions to investigate

1. **How does word choice differ across comparable talks?** In **Word Frequency**, search a word or phrase, choose the same session category and year grouping, and compare women and men using **per 10k words**. Try “mother” or “faith,” then inspect the underlying counts and sample sizes. Normalization handles unequal text volume; it does not remove all differences in topic or audience.
2. **How has women's share of speaking changed?** In **Talk frequency**, compare yearly and decade groupings, switch between counts and percentage, and separate general, women's, and priesthood sessions. Percentage axes span 0–100%, including women's sessions where the proportion exceeds 50%.
3. **What might explain a language pattern?** Use talk-length and speaker views to check whether a pattern coincides with longer talks, particular speakers, or a different session mix. Explore topic samples and return to the source talks before treating a chart as a conclusion.

## Run locally

Requires Python 3 for a static server; the browser app needs no build step or account.

```sh
git clone https://github.com/MikWess/women-at-the-pulpit.git
cd women-at-the-pulpit
python3 -m http.server 8000 --bind 127.0.0.1
```

Open **http://127.0.0.1:8000/** and wait for the loaded-talk count. Opening `index.html` directly with `file://` can block JSON fetches. The app reports failed data loads instead of leaving a permanent loading message.

Chart.js and fonts load from external CDNs, so the browser needs network access for the complete visual experience. For a local text-only frequency ranking, run `python3 word_frequency.py` from the repository root; it reads the bundled JSON using only the Python standard library.

## Dataset and interpretation

This is a **snapshot, not a verified complete census** of every talk in the date range. The current JSON contains 395 talks tagged female and 3,606 tagged male (9.9% female), with 3,087 general-session, 352 women's-session, and 562 priesthood-session talks. Tags reflect the dataset's classifications, not an exhaustive model of identity or session history.

Comparisons depend on session selection, year range, repeated speakers, topic, and talk length. The displayed statistical significance calculation is exploratory: repeated speakers, many word searches, and corpus selection limit causal or population-level interpretations. Equal displayed rates are shown as equal, rather than defaulting to a male lead.

Source material comes from [the Church's General Conference archive](https://www.churchofjesuschrist.org/study/general-conference). Consult original talks for context; source text retains its original ownership.

- `data/talks.json`: the browser's text, speaker, year, gender, and session snapshot.
- `data/surprising.json` and `data/topics.json`: precomputed comparison/topic data.
- `data/conference_talks.csv` and `speaker_genders.csv`: pipeline inputs/intermediates.
- `scrape.py`, `tag_sessions.py`, `build_gender_table.py`, `word_frequency.py`: scraping, tagging, and analysis utilities.

The repository does not currently provide a single reproducible command to regenerate all three browser JSON files. Re-running a scraper alone does not refresh every view. Keep them consistent when updating the dataset and verify the resulting counts and samples before publishing.

## Manual checks after changing the viewer

Serve the folder, confirm the loaded count, search a common word and a nonexistent phrase, compare session filters, and inspect the percentage chart for women's sessions. Temporarily unavailable JSON should produce a visible load error. A zero-result phrase should not claim either group uses it more.

Any static host can serve the same files. Local edits do not update an existing hosted deployment until you publish them.
