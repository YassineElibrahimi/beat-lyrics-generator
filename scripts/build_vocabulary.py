# scripts/build_vocabulary.py

"""
Explanation:
'build_vocabulary' scans all lyric lines stored in the database and builds a vocabulary frequency table.
It retrieves the text from the 'lines' table, converts each line to lowercase, and extracts words using a regular expression.
Only alphabetic words are kept, and very short words (less than 3 characters) are ignored to avoid noise.

For each valid word, the script counts how many times it appears and stores the result in a dictionary
using a (theme, word) pair as the key. Currently, the theme is hardcoded as 'hard' as a placeholder,
but this can later be replaced with real theme data from the database.

Before inserting new data, the script clears the existing 'vocabulary' table.
Then it inserts each word with its theme and frequency into the database.

The script can also be executed directly, in which case it runs 'build_vocabulary'
to rebuild the vocabulary table automatically.
"""

"""
*Content:
build_vocabulary()
"""











import re
from data.database import get_connection




def build_vocabulary():
    conn    = get_connection()
    cursor  = conn.cursor()

    # Fetch all lines (theme is currently 'hard' for all)
    cursor.execute('SELECT text FROM lines')
    rows = cursor.fetchall()

    word_counts = {}
    theme       = 'hard'  # placeholder – we'll improve later

    for row in rows:
        text    = row['text'].lower()
        words   = re.findall(r'\b[a-z]+\b', text)
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