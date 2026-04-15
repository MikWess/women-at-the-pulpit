"""
09_word_discovery.py — Find the most interesting words automatically.

Scores every word on three dimensions:
  1. GENDER GAP — how different is the rate between women and men?
  2. TIME TREND — how much has usage changed over the decades?
  3. FREQUENCY — how common is the word? (rare words are less interesting)

Final score = gender_gap * time_change * log(frequency)
"""

import math
from collections import Counter
from helpers import load_data

df, women, men = load_data()

# ── Step 1: Build vocabulary from all talks ─────────────────────────
print("Building vocabulary...")

# Count every word across all talks
all_words = Counter()
for text in df["talk"]:
    for word in str(text).lower().split():
        # Strip punctuation from edges
        word = word.strip(".,;:!?\"'()-–—[]")
        if len(word) > 2 and word.isalpha():
            all_words[word] += 1

# Only look at words that appear 100+ times (frequent enough to matter)
vocab = {word: count for word, count in all_words.items() if count >= 100}
print(f"Vocabulary: {len(vocab)} words (appearing 100+ times)")

# ── Step 2: Compute gender rates for each word ─────────────────────
print("Computing gender rates...")

w_total_words = women["talk"].apply(lambda t: len(str(t).split())).sum()
m_total_words = men["talk"].apply(lambda t: len(str(t).split())).sum()

# Count each vocab word in women's vs men's talks
w_counts = Counter()
m_counts = Counter()

for text in women["talk"]:
    for word in str(text).lower().split():
        word = word.strip(".,;:!?\"'()-–—[]")
        if word in vocab:
            w_counts[word] += 1

for text in men["talk"]:
    for word in str(text).lower().split():
        word = word.strip(".,;:!?\"'()-–—[]")
        if word in vocab:
            m_counts[word] += 1

# ── Step 3: Compute time trend for each word ────────────────────────
print("Computing time trends...")

# Split into early (1971-1997) and late (1998-2025)
early = df[df["year"] <= 1997]
late = df[df["year"] >= 1998]

early_words_total = early["talk"].apply(lambda t: len(str(t).split())).sum()
late_words_total = late["talk"].apply(lambda t: len(str(t).split())).sum()

early_counts = Counter()
late_counts = Counter()

for text in early["talk"]:
    for word in str(text).lower().split():
        word = word.strip(".,;:!?\"'()-–—[]")
        if word in vocab:
            early_counts[word] += 1

for text in late["talk"]:
    for word in str(text).lower().split():
        word = word.strip(".,;:!?\"'()-–—[]")
        if word in vocab:
            late_counts[word] += 1

# ── Step 4: Score every word ────────────────────────────────────────
print("Scoring...")

results = []

for word in vocab:
    freq = vocab[word]

    # Gender gap: absolute difference in rate per 10k words
    w_rate = (w_counts.get(word, 0) / w_total_words) * 10000
    m_rate = (m_counts.get(word, 0) / m_total_words) * 10000
    gender_gap = abs(w_rate - m_rate)
    who_more = "women" if w_rate > m_rate else "men"

    # Time trend: absolute difference in rate between early and late halves
    early_rate = (early_counts.get(word, 0) / early_words_total) * 10000
    late_rate = (late_counts.get(word, 0) / late_words_total) * 10000
    time_change = abs(late_rate - early_rate)
    direction = "rising" if late_rate > early_rate else "falling"

    # Combined score: gender_gap * time_change * log(frequency)
    # log(frequency) rewards common words without letting them dominate
    score = gender_gap * time_change * math.log(freq + 1)

    results.append({
        "word": word,
        "freq": freq,
        "w_rate": w_rate,
        "m_rate": m_rate,
        "gender_gap": gender_gap,
        "who_more": who_more,
        "early_rate": early_rate,
        "late_rate": late_rate,
        "time_change": time_change,
        "direction": direction,
        "score": score,
    })

# ── Step 5: Print results ──────────────────────────────────────────

# Sort by combined score
results.sort(key=lambda r: r["score"], reverse=True)

# Filter out boring function words
STOP_WORDS = {
    "the", "and", "that", "this", "with", "have", "from", "they",
    "been", "were", "will", "would", "could", "should", "about",
    "their", "them", "than", "then", "into", "also", "each",
    "which", "when", "what", "there", "these", "those", "some",
    "other", "more", "most", "very", "just", "like", "know",
    "can", "has", "had", "was", "are", "but", "not", "you",
    "all", "her", "his", "she", "for", "who", "how", "may",
    "its", "our", "out", "did", "one", "said", "may", "way",
    "come", "came", "made", "make", "many", "much", "own",
    "such", "well", "does", "being", "because", "through",
    "over", "after", "before", "where", "here", "only", "even",
}

filtered = [r for r in results if r["word"] not in STOP_WORDS]

print()
print("=" * 80)
print("  TOP 30 MOST INTERESTING WORDS")
print("  (biggest combined gender gap + time change + frequency)")
print("=" * 80)
print()
print(f"  {'Word':<18} {'Freq':>6} {'Women/10k':>10} {'Men/10k':>10} {'Gap':>8} {'Who':>8} {'Early':>8} {'Late':>8} {'Trend':>8}")
print(f"  {'-'*18} {'-'*6} {'-'*10} {'-'*10} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")

for r in filtered[:30]:
    print(f"  {r['word']:<18} {r['freq']:>6} {r['w_rate']:>10.2f} {r['m_rate']:>10.2f} {r['gender_gap']:>8.2f} {r['who_more']:>8} {r['early_rate']:>8.2f} {r['late_rate']:>8.2f} {r['direction']:>8}")

# ── Separate rankings ──────────────────────────────────────────────

print()
print("=" * 80)
print("  TOP 20 — BIGGEST GENDER GAP (frequent words only)")
print("=" * 80)
print()

by_gender = sorted(filtered, key=lambda r: r["gender_gap"], reverse=True)
for r in by_gender[:20]:
    arrow = "♀" if r["who_more"] == "women" else "♂"
    print(f"  {arrow} {r['word']:<18} women={r['w_rate']:.2f}  men={r['m_rate']:.2f}  gap={r['gender_gap']:.2f}  ({r['freq']} total)")

print()
print("=" * 80)
print("  TOP 20 — BIGGEST TIME CHANGE (frequent words only)")
print("=" * 80)
print()

by_time = sorted(filtered, key=lambda r: r["time_change"], reverse=True)
for r in by_time[:20]:
    arrow = "↑" if r["direction"] == "rising" else "↓"
    print(f"  {arrow} {r['word']:<18} early={r['early_rate']:.2f}  late={r['late_rate']:.2f}  change={r['time_change']:.2f}  ({r['freq']} total)")
