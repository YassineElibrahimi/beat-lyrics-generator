"""
Explanation:
This script seeds the core beat and lyrics database with initial data for genres, themes, instruments, chord progressions, and drum patterns.
It loads predefined JSON templates from the 'data/templates' directory and populates the corresponding database tables.

Key functionalities include:
- 'load_json': reads a JSON file from the 'data/templates' directory, creating the directory if it doesn't exist.
- 'seed_database': initializes tables using 'init_db', then inserts:
    - predefined genres (e.g., trap, drill, old_school)
    - predefined themes (e.g., hard, melancholic, aggressive, smooth)
    - instruments with MIDI program numbers from 'instruments.json'
    - chord progressions from 'chord_progressions.json', linked to genres and themes
    - drum patterns from 'drum_patterns.json', storing probability grids as JSON strings
- Ensures duplicate entries are ignored using 'INSERT OR IGNORE' and validates that genre/theme keys exist before insertion.

This script sets up the database with structured musical templates, enabling procedural generation of chords, drums, and melodies.
"""

"""
*Content:
load_json()
seed_database()
"""










import os
from data.database import get_connection, init_db
import json




def load_json(filename):
    TEMPLATES_DIR = os.path.join('data', 'templates')
    if not os.path.exists(TEMPLATES_DIR):
        os.makedirs(TEMPLATES_DIR)

    path = os.path.join(TEMPLATES_DIR, filename)
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


# ============== CREATE / INSERT ==============
def seed_database():

    # Create tables
    init_db()
    conn = get_connection()
    cursor     = conn.cursor()

    # Insert genre
    genres_data = ['trap', 'drill', 'old_school']

    for genre in genres_data:
        cursor.execute('INSERT OR IGNORE INTO genres (name) VALUES (?)', (genre,))
    conn.commit()

    # Insert themes
    themes_data = ['hard', 'melancholic', 'aggressive', 'smooth']

    for theme in themes_data:
        cursor.execute('INSERT OR IGNORE INTO themes (name) VALUES (?)', (theme,))
    conn.commit()

    # Get genre and theme IDs for lookups
    cursor.execute('SELECT id, name FROM genres')
    genre_ids = {row['name']: row['id'] for row in cursor.fetchall()}
    # print("Genre IDs found:", list(genre_ids.keys()))  # <-- ADD THIS LINE for debugging

    cursor.execute('SELECT id, name FROM themes')
    theme_ids = {row['name']: row['id'] for row in cursor.fetchall()}
    # print("Theme IDs found:", list(theme_ids.keys()))  # <-- ADD THIS LINE for debugging

    # Insert instruments
    instruments = load_json('instruments.json')

    for name , program in instruments.items():
        cursor.execute('INSERT OR IGNORE INTO instruments (name, midi_program) VALUES (?, ?)', (name, program))
    conn.commit()

    # Insert chord progressions
    chord_progs = load_json('chord_progressions.json')

    for key, progressions in chord_progs.items():
        if '_' not in key:
            print(f"Skipping invalid key format: {key}")
            continue
        genre_name, theme_name = key.rsplit('_',1)         # key format: "genre_theme" (e.g., "trap_hard")
        # print(f"Processing: {key} -> genre='{genre_name}', theme='{theme_name}'")  # <-- ADD THIS for debugging
        if genre_name not in genre_ids or theme_name not in theme_ids:
            print(f"Skipping unknown genre/theme : {key}")
            continue

        genre_id   = genre_ids[genre_name]
        theme_id   = theme_ids[theme_name]

        for progression in progressions:
            numerals_str = ','.join(progression)        # Convert list to comma-separated str for storage
            cursor.execute('''
                INSERT INTO chord_progressions (genre_id, theme_id, roman_numerals)
                VALUES (?, ?, ?)''',           (genre_id, theme_id, numerals_str)
            )
    conn.commit()

    # Insert drum patterns
    drum_patterns = load_json('drum_patterns.json')

    for genre_name, patterns in drum_patterns.items():
        if genre_name not in genre_ids:
            print(f"Skipping unknown genre : {genre_name}")
            continue

        genre_id = genre_ids[genre_name]
        for pattern_name, probabilities in patterns.items():# probabilities is a list of floats; convert to JSON str
            probabilities_json = json.dumps(probabilities)
            cursor.execute('''
                INSERT INTO drum_patterns (genre_id, pattern_name, probabilities)
                VALUES (?, ?, ?)''', (genre_id, pattern_name, probabilities_json)
            )
    conn.commit()
    conn.close()
    print("Database seeded successfully.")




if __name__ == "__main__":
    seed_database()