#!/usr/bin/env python3
"""
build_gender_table.py — Create a verified gender lookup for every speaker.

APPROACH (layered, most reliable first):
  1. Official Church Historian's Press list of women conference speakers
  2. Web-verified corrections (names the library gets wrong)
  3. gender_guesser library on first names
  4. Calling-based fallback for remaining unknowns

Outputs: speaker_genders.csv — the definitive table.
"""

import pandas as pd
import gender_guesser.detector as gender

df = pd.read_csv("data/conference_talks.csv")
detector = gender.Detector()

# ─── LAYER 1: Official list of women from Church Historian's Press ────
# Source: https://www.churchhistorianspress.org/at-the-pulpit/reference/appendix
# This is the GOLD STANDARD — verified by the Church's own historians.
# Plus recent speakers we confirmed via web search.

VERIFIED_WOMEN = {
    # From Church Historian's Press appendix
    "Barbara B. Smith", "Elaine A. Cannon", "Ardeth G. Kapp",
    "Dwan J. Young", "Michaelene P. Grassli", "Joy F. Evans",
    "Jayne B. Malan", "Barbara W. Winder", "Elaine L. Jack",
    "Ruth B. Wright", "Janette C. Hales", "Aileen H. Clyde",
    "Betty Jo N. Jepsen", "Chieko N. Okazaki", "Virginia H. Pearce",
    "Patricia P. Pinegar", "Bonnie D. Parkin", "Janette Hales Beckham",
    "Anne G. Wirthlin", "Susan L. Warner", "Mary Ellen Smoot",
    "Carol B. Thomas", "Sheri L. Dew", "Sharon G. Larsen",
    "Coleen K. Menlove", "Sydney S. Reynolds", "Gayle M. Clegg",
    "Kathleen H. Hughes", "Susan W. Tanner", "Anne C. Pingree",
    "Julie B. Beck", "Elaine S. Dalton", "Cheryl C. Lant",
    "Margaret S. Lifferth", "Vicki F. Matsumori", "Mary N. Cook",
    "Silvia H. Allred", "Barbara Thompson", "Ann M. Dibb",
    "Rosemary M. Wixom", "Jean A. Stevens", "Cheryl A. Esplin",
    "Linda K. Burton", "Carole M. Stephens", "Bonnie L. Oscarson",
    "Linda S. Reeves", "Neill F. Marriott", "Carol F. McConkie",
    "Mary R. Durham", "Jean B. Bingham", "Margaret D. Nadauld",
    "Virginia U. Jensen", "JoAnn Randall", "Shirley W. Thomas",
    "Naomi M. Shumway", "Joy D. Jones", "Ruth H. Funk",
    "Joanne B. Doxey", "Betty Jo Jepsen", "Mary Ellen W. Smoot",
    "Mary F. Foulger", "Addie Fuhriman",

    # Recent speakers (2018–2025) confirmed via web / church site
    "Bonnie H. Cordon", "Becky Craven", "Michelle Craig",
    "Michelle D. Craig", "Cristina B. Franco", "Sharon Eubank",
    "Reyna I. Aburto", "Lisa L. Harkness", "Amy A. Wright",
    "Camille N. Johnson", "Susan H. Porter", "Tracy Y. Browning",
    "J. Anette Dennis", "Rebecca L. Craven", "Kristin M. Yee",
    "Emily Belle Freeman", "Tamara W. Runia", "Andrea Muñoz Spannaus",

    # Ordinary members / youth speakers — confirmed female via web
    "Laudy Ruth Kaouk", "Hilarie Cole", "Fono Lavatai",
    "Alejandra Hernández", "Kristin Banner", "Anne Marie Rose",
    "Anne Prescott", "Karen Maxwell", "Kirstin Boyer",
    "Melanie Eaton", "Jeanne Inouye", "Andrea Allen",
    "Nyle Randall",  # JoAnn Randall's co-speaker
}

# ─── LAYER 2: Web-verified MALE overrides ────────────────────────────
# Names the gender_guesser library wrongly flags as female.

VERIFIED_MALE = {
    "Marion D. Hanks",       # General Authority, Of the Seventy
    "Marion G. Romney",      # Apostle / First Presidency
    "Merlin R. Lybbert",     # Of the Seventy
    "Shirley D. Christensen",# Of the Seventy (confirmed male via web)
    "Joni L. Koch",          # Elder Koch, General Authority Seventy (confirmed male via web)

    # "mostly_female" names that are actually men (Of the Seventy, etc.)
    "Lynn G. Robbins", "Lynn A. Mickelsen", "Lynn A. Sorensen",
    "Brook P. Hales", "Kelly R. Johnson", "Kim B. Clark",
    "Kyle S. McKay", "Val R. Christensen",
}


def classify_speaker(speaker_name, calling):
    """
    Classify a speaker as 'female' or 'male'.
    Uses layered approach: verified lists → library → calling fallback.
    """
    # Clean the "By " prefix that some names have
    clean_name = str(speaker_name).replace("By ", "").strip()

    # Layer 1: Check verified lists (highest confidence)
    if clean_name in VERIFIED_WOMEN:
        return "female"
    # Also check with "By " prefix since some entries in our data have it
    if speaker_name in VERIFIED_WOMEN:
        return "female"

    if clean_name in VERIFIED_MALE:
        return "male"
    if speaker_name in VERIFIED_MALE:
        return "male"

    # Layer 2: gender_guesser library
    first_name = clean_name.split()[0] if clean_name else ""
    guess = detector.get_gender(first_name)

    if guess == "female":
        # Double-check: if calling is Seventy/Apostle/Bishop, override to male
        calling_lower = str(calling).lower()
        male_callings = ["seventy", "apostle", "bishop", "quorum of the twelve",
                         "first presidency", "presiding bishop", "council of the twelve",
                         "assistant to the"]
        if any(mc in calling_lower for mc in male_callings):
            return "male"
        return "female"

    if guess == "male" or guess == "mostly_male":
        return "male"

    if guess == "mostly_female":
        # Check calling to disambiguate
        calling_lower = str(calling).lower()
        female_callings = ["relief society", "young women", "primary"]
        if any(fc in calling_lower for fc in female_callings):
            return "female"
        return "male"  # Default for mostly_female with non-female calling

    # Layer 3: Calling-based fallback for unknowns
    calling_lower = str(calling).lower()
    female_callings = ["relief society", "young women", "primary"]
    if any(fc in calling_lower for fc in female_callings):
        return "female"

    # Default to male (the vast majority of unknown names in this dataset
    # are men with initials or non-English names in male callings)
    return "male"


def main():
    # Get unique speakers
    speakers = df.drop_duplicates("speaker")[["speaker", "calling"]].copy()

    # Classify each
    speakers["gender"] = speakers.apply(
        lambda row: classify_speaker(row["speaker"], row["calling"]), axis=1
    )

    # Build the lookup table: speaker → gender
    # Some speakers appear with multiple callings over the years,
    # so we take the first classification (they don't change gender)
    lookup = speakers.drop_duplicates("speaker")[["speaker", "gender"]]

    # Save
    lookup.to_csv("data/speaker_genders.csv", index=False)

    # ── Report ───────────────────────────────────────────────────────
    women = lookup[lookup["gender"] == "female"]
    men = lookup[lookup["gender"] == "male"]

    print("=" * 60)
    print("SPEAKER GENDER TABLE — BUILT")
    print("=" * 60)
    print(f"Total unique speakers: {len(lookup)}")
    print(f"  Female: {len(women)}")
    print(f"  Male:   {len(men)}")
    print()

    print("Method breakdown:")
    # Count how each was classified
    verified_f = 0
    verified_m = 0
    library = 0
    calling_fb = 0

    for _, row in speakers.iterrows():
        clean = str(row["speaker"]).replace("By ", "").strip()
        if clean in VERIFIED_WOMEN or row["speaker"] in VERIFIED_WOMEN:
            verified_f += 1
        elif clean in VERIFIED_MALE or row["speaker"] in VERIFIED_MALE:
            verified_m += 1
        else:
            first = clean.split()[0] if clean else ""
            guess = detector.get_gender(first)
            if guess in ("female", "male", "mostly_male"):
                library += 1
            elif guess == "mostly_female":
                library += 1
            else:
                calling_fb += 1

    print(f"  Verified women (historian's list + web): {verified_f}")
    print(f"  Verified men (web override):             {verified_m}")
    print(f"  Library (gender_guesser):                {library}")
    print(f"  Calling fallback:                        {calling_fb}")

    print()
    print("ALL WOMEN SPEAKERS:")
    print("-" * 60)
    # Cross-reference with talk counts
    woman_talks = df[df["speaker"].isin(women["speaker"].values)]
    woman_summary = (woman_talks.groupby("speaker")
                     .agg(talks=("title", "count"),
                          years=("year", lambda x: f"{x.min()}-{x.max()}"),
                          calling=("calling", "first"))
                     .sort_values("talks", ascending=False))

    for name, row in woman_summary.iterrows():
        # Strip "By " for cleaner display
        display = str(name).replace("By ", "")
        print(f"  {display:>35}  {row['talks']:>3} talks  ({row['years']})  {row['calling']}")

    print()
    print(f"Saved to: speaker_genders.csv")
    print("=" * 60)


if __name__ == "__main__":
    main()
