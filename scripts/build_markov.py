# scripts/build_markov.py

import re
from collections import defaultdict, Counter
from data.database import get_connection

# Special tokens for line boundaries
START_TOKEN = "__START__"
END_TOKEN = "__END__"
MIN_COUNT = 2  # minimum frequency to keep a transition

def tokenize(line):
    """Convert line to list of lowercase words."""
    return re.findall(r'\b[a-z]+\b', line.lower())

def build_markov_transitions():
    conn = get_connection()
    cursor = conn.cursor()

    # Create bigram table (if not exists)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS markov_transitions (
            theme       TEXT NOT NULL,
            prev_word   TEXT NOT NULL,
            next_word   TEXT NOT NULL,
            count       INTEGER DEFAULT 1,
            PRIMARY KEY (theme, prev_word, next_word)
        )
    ''')

    # Create trigram table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS markov_trigrams (
            theme       TEXT NOT NULL,
            prev1       TEXT NOT NULL,
            prev2       TEXT NOT NULL,
            next_word   TEXT NOT NULL,
            count       INTEGER DEFAULT 1,
            PRIMARY KEY (theme, prev1, prev2, next_word)
        )
    ''')

    # Clear existing data (optional – we'll rebuild fresh)
    cursor.execute('DELETE FROM markov_transitions')
    cursor.execute('DELETE FROM markov_trigrams')

    # Fetch all lines with themes
    cursor.execute('SELECT theme, text FROM lines WHERE theme IS NOT NULL')
    rows = cursor.fetchall()

    # Counters for bigrams and trigrams
    bigram_counts  = defaultdict(Counter)      # (theme, prev) -> Counter of next words
    trigram_counts = defaultdict(Counter)     # (theme, prev1, prev2) -> Counter of next words

    for row in rows:
        theme = row['theme']
        words = tokenize(row['text'])
        if len(words) < 1:
            continue

        # --- Bigram transitions ---
        # START_TOKEN -> first word
        bigram_counts[(theme, START_TOKEN)][words[0]] += 1
        # between words
        for i in range(len(words)-1):
            prev = words[i]
            nxt  = words[i+1]
            bigram_counts[(theme, prev)][nxt] += 1
        # last word -> END_TOKEN
        bigram_counts[(theme, words[-1])][END_TOKEN] += 1

        # --- Trigram transitions ---
        # For the first word, prefix is (START_TOKEN, START_TOKEN)
        trigram_counts[(theme, START_TOKEN, START_TOKEN)][words[0]] += 1
        if len(words) >= 2:
            # second word: prefix (START_TOKEN, first_word)
            trigram_counts[(theme, START_TOKEN, words[0])][words[1]] += 1
        for i in range(len(words)-2):
            prev1, prev2, nxt = words[i], words[i+1], words[i+2]
            trigram_counts[(theme, prev1, prev2)][nxt] += 1
        # last word -> END_TOKEN (prefix is (prev2_last, last_word) where prev2_last is second-last)
        if len(words) >= 2:
            trigram_counts[(theme, words[-2], words[-1])][END_TOKEN] += 1
        else:
            # line with only one word: prefix (START_TOKEN, that_word) -> END_TOKEN
            trigram_counts[(theme, START_TOKEN, words[0])][END_TOKEN] += 1

    # Insert bigrams with MIN_COUNT filter
    bigram_inserted = 0
    for (theme, prev), next_counter in bigram_counts.items():
        for nxt, cnt in next_counter.items():
            if cnt >= MIN_COUNT:
                cursor.execute('''
                    INSERT INTO markov_transitions (theme, prev_word, next_word, count)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(theme, prev_word, next_word)
                    DO UPDATE SET count = count + excluded.count
                ''', (theme, prev, nxt, cnt))
                bigram_inserted += 1

    # Insert trigrams with MIN_COUNT filter
    trigram_inserted = 0
    for (theme, prev1, prev2), next_counter in trigram_counts.items():
        for nxt, cnt in next_counter.items():
            if cnt >= MIN_COUNT:
                cursor.execute('''
                    INSERT INTO markov_trigrams (theme, prev1, prev2, next_word, count)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(theme, prev1, prev2, next_word)
                    DO UPDATE SET count = count + excluded.count
                ''', (theme, prev1, prev2, nxt, cnt))
                trigram_inserted += 1

    conn.commit()
    conn.close()

    total_bigrams_raw  = sum(len(c) for c in bigram_counts.values())
    total_trigrams_raw = sum(len(c) for c in trigram_counts.values())
    print(f"Bigrams built: {bigram_inserted} (min count={MIN_COUNT}) from {total_bigrams_raw} raw")
    print(f"Trigrams built: {trigram_inserted} (min count={MIN_COUNT}) from {total_trigrams_raw} raw")

if __name__ == '__main__':
    build_markov_transitions()