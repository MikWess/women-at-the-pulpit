"""
helpers.py — Shared code that every script uses.

WHY THIS FILE EXISTS:
Instead of copy-pasting the same "load data" and "figure out who is a woman"
code into every script, we write it once here and import it.

HOW TO USE IT:
    from helpers import load_data
    df, women, men = load_data()

That one line gives you three things:
    - df:    ALL talks (the full spreadsheet)
    - women: only the rows where the speaker is a woman
    - men:   only the rows where the speaker is a man

GENDER DETECTION:
We used to guess gender from callings (Relief Society = woman, etc).
That missed women with unusual callings and miscategorized some men.

Now we use a VERIFIED LOOKUP TABLE (speaker_genders.csv) built from:
  1. The Church Historian's Press official list of women speakers
  2. Web-confirmed corrections for ambiguous names (Marion D. Hanks = male, etc.)
  3. The gender_guesser Python library on first names
  4. Calling-based fallback for anyone still unknown

Run build_gender_table.py to regenerate the table if you add new data.
"""

import pandas as pd
import os

# ─────────────────────────────────────────────────────────────────────
# STEP 1: Figure out paths
# ─────────────────────────────────────────────────────────────────────
# os.path.dirname(__file__) = the folder THIS file (helpers.py) lives in
# os.path.join(..., "..") = go up one folder (from questions/ to the project root)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..")
CSV_PATH = os.path.join(DATA_DIR, "data", "conference_talks.csv")
GENDER_PATH = os.path.join(DATA_DIR, "data", "speaker_genders.csv")


# ─────────────────────────────────────────────────────────────────────
# STEP 2: Load the verified gender lookup table
# ─────────────────────────────────────────────────────────────────────
# speaker_genders.csv has two columns: "speaker" and "gender"
# We load it into a dictionary for fast lookups:
#   { "Barbara B. Smith": "female", "Gordon B. Hinckley": "male", ... }

def _load_gender_lookup():
    """Load the verified gender table into a dictionary."""
    if not os.path.exists(GENDER_PATH):
        print("WARNING: speaker_genders.csv not found!")
        print("Run: python build_gender_table.py")
        return {}

    gender_df = pd.read_csv(GENDER_PATH)

    # .to_dict() converts two columns into a {key: value} dictionary
    # set_index("speaker") makes the speaker name the key
    # ["gender"] selects just the gender column as values
    return gender_df.set_index("speaker")["gender"].to_dict()


GENDER_LOOKUP = _load_gender_lookup()


def is_woman(speaker_name):
    """
    Look up whether a speaker is female using our verified table.

    Returns True if female, False otherwise.
    Falls back to False (male) if the speaker isn't in the table.
    """
    return GENDER_LOOKUP.get(speaker_name, "male") == "female"


# ─────────────────────────────────────────────────────────────────────
# STEP 3: The main function every script will call
# ─────────────────────────────────────────────────────────────────────

def load_data():
    """
    Load the conference talks CSV and split into women vs men.

    Returns three DataFrames:
        df     — all talks
        women  — only women's talks
        men    — only men's talks
    """
    # pd.read_csv() reads a CSV file into a DataFrame (like a spreadsheet)
    df = pd.read_csv(CSV_PATH)

    # Make sure "year" is an integer (not a string like "1993")
    df["year"] = df["year"].astype(int)

    # Look up each speaker's gender from our verified table.
    # .apply(is_woman) runs is_woman() on every speaker name.
    # OLD WAY: guessed from calling keywords (missed ~20 women)
    # NEW WAY: uses verified lookup table built from multiple sources
    df["is_woman"] = df["speaker"].apply(is_woman)

    # Split into two DataFrames using boolean filtering.
    # df[df["is_woman"]] keeps only rows where is_woman is True.
    # df[~df["is_woman"]] keeps only rows where is_woman is False.
    # (The ~ means "not" — it flips True to False and vice versa.)
    women = df[df["is_woman"]].copy()
    men = df[~df["is_woman"]].copy()

    return df, women, men


# ─────────────────────────────────────────────────────────────────────
# STEP 4: A helper to print section headers nicely
# ─────────────────────────────────────────────────────────────────────

def print_header(title):
    """Print a nice section header for our output."""
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print()
