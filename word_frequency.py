#!/usr/bin/env python3
"""
word_frequency.py — Rank the 500 most frequently used words across all conference talks.
Filters out common English stop words to surface meaningful content words.
"""

import json
import re
from collections import Counter

STOP_WORDS = {
    "the", "and", "of", "to", "a", "in", "that", "is", "it", "for",
    "was", "i", "we", "be", "with", "are", "not", "this", "as", "but",
    "have", "they", "his", "he", "our", "by", "on", "or", "an", "has",
    "will", "from", "you", "all", "them", "their", "had", "who", "been",
    "do", "would", "she", "her", "which", "him", "so", "if", "at", "when",
    "can", "one", "my", "there", "what", "were", "no", "about", "may",
    "us", "more", "than", "its", "also", "up", "could", "into", "those",
    "did", "other", "how", "then", "each", "these", "shall", "some",
    "your", "said", "me", "out", "am", "very", "should", "just", "own",
    "because", "over", "such", "even", "being", "after", "through",
    "before", "most", "must", "any", "where", "only", "many", "much",
    "well", "might", "come", "like", "upon", "now", "way", "make",
    "made", "does", "here", "two", "know", "first", "while", "back",
    "get", "go", "came", "take", "see", "say", "too", "let", "still",
    "down", "between", "never", "off", "under", "every", "again",
    "another", "himself", "herself", "around", "without", "both",
    "during", "same", "something", "going", "new", "long", "since",
    "why", "away", "yet", "day", "things", "thing", "time", "times",
    "however", "though", "always", "once", "went", "given", "got",
    "put", "far", "often", "set", "keep", "tell", "told", "don",
    "didn", "doesn", "won", "isn", "aren", "wasn", "weren", "hadn",
    "couldn", "wouldn", "shouldn", "didn", "don", "s", "t", "ve",
    "re", "d", "ll", "m",
}


def main():
    with open("data/talks.json") as f:
        talks = json.load(f)

    counts = Counter()
    for talk in talks:
        words = re.findall(r"[a-z']+", talk["t"].lower())
        for word in words:
            clean = word.strip("'")
            if clean and clean not in STOP_WORDS and len(clean) > 1:
                counts[clean] += 1

    print(f"Analyzed {len(talks)} talks")
    print(f"Unique words (after filtering): {len(counts)}")
    print()
    print(f"{'RANK':<6} {'WORD':<25} {'COUNT':>10}")
    print("-" * 43)

    for rank, (word, count) in enumerate(counts.most_common(500), 1):
        print(f"{rank:<6} {word:<25} {count:>10}")


if __name__ == "__main__":
    main()
