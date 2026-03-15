# scripts/build_markov.py

import re
from collections import defaultdict, Counter
from data.database import get_connection

def tokenize(line):
    """convert line to list of lowercase words (simple tokenizer)."""
    return re.findall(r'\b[a-z]+\b', line.lower())

def build_markov_transitions():
    conn = get_connection()
    cursor = conn.cursor()

    # Create new table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS markov_transitions (
            theme       TEXT NOT NULL,
            prev_word   TEXT NOT NULL,
            next_word   TEXT NOT NULL,
            count       INTEGER DEFAULT 1,
            PRIMARY KEY (theme, prev_word, next_word)
        )
    ''')

    # Clear existing data (if rebuilding)
    cursor.execute('DELETE FROM markov_transitions')

    # Fetch all lines with themes
    cursor.execute('SELECT theme, text FROM lines WHERE theme IS NOT NULL')
    rows = cursor.fetchall()

    # Use local counter to batch inserts
    transitions = defaultdict(Counter)      # (theme, prev) -> Counter of next words

    for row in rows:
        theme = row['theme']
        words = tokenize(row['text'])
        if len(words) < 2:
            continue
        for i in range(len(words)-1):
            prev = words[i]
            nxt  = words[i+1]
            transitions[(theme, prev)][nxt] += 1

    # Insert into database
    for (theme, prev), next_counter in transitions.items():
        for nxt, cnt in next_counter.items():
            cursor.execute('''
                INSERT INTO markov_transitions (theme, prev_word, next_word, count)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(theme, prev_word, next_word)
                DO UPDATE SET count = count + excluded.count
            ''', (theme, prev, nxt, cnt)
            )

    conn.commit()
    conn.close()
    print(f"Markov transitions built: {sum(len(c) for c in transitions.values())} unique (prev,next) pairs.")

if __name__ == '__main__':
    build_markov_transitions()