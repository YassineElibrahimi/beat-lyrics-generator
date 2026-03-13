import re
import sqlite3
from data.database import get_connection

def build_vocabulary():
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch all lines (theme is currently 'hard' for all)
    cursor.execute('SELECT text FROM lines')
    rows = cursor.fetchall()

    word_counts = {}
    theme = 'hard'  # placeholder – we'll improve later

    for row in rows:
        text = row['text'].lower()
        words = re.findall(r'\b[a-z]+\b', text)
        for word in words:
            if len(word) < 3:
                continue
            key = (theme, word)
            word_counts[key] = word_counts.get(key, 0) + 1

    # Clear old vocabulary
    cursor.execute('DELETE FROM vocabulary')
    for (theme, word), count in word_counts.items():
        cursor.execute('''
            INSERT INTO vocabulary (theme, word, frequency)
            VALUES (?, ?, ?)
        ''', (theme, word, count))

    conn.commit()
    conn.close()
    print("Vocabulary built successfully.")

if __name__ == '__main__':
    build_vocabulary()