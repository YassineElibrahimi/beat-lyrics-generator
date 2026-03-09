'''
Explanation:
This script will:
Call database.init_db() to create tables.
Insert genres and themes.
Insert instruments from JSON.
Insert chord progressions from JSON.
Insert drum patterns from JSON.
'''

import os
from data.database import get_connection, init_db
import json




def load_json(filename):
    path = os.path.join('data', 'templates', filename)
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


# ============== CREATE / INSERT ==============
def seed_database():

# Create tables
    init_db()
    connection = get_connection()
    cursor     = connection.cursor()

# Insert genre
    genres_data = ['trap', 'drill', 'old_school']

    for genre in genres_data:
        cursor.execute('INSERT OR IGNORE INTO genres (name) VALUES (?)', (genre,))
    connection.commit()

# Insert themes
    themes_data = ['hard', 'melancholic', 'aggressive', 'smooth']

    for theme in themes_data:
        cursor.execute('INSERT OR IGNORE INTO themes (name) VALUES (?)', (theme,))
    connection.commit()

# Get genre and theme IDs for lookups
    cursor.execute('SELECT id, name FROM genres')
    genre_ids = {row['name']: row['id'] for row in cursor.fetchall()}

    cursor.execute('SELECT id, name FROM themes')
    theme_ids = {row['name']: row['id'] for row in cursor.fetchall()}

# Insert instruments
    instruments = load_json('instruments.json')

    for name , program in instruments.items():
        cursor.execute('INSERT OR IGNORE INTO instruments (name, midi_program) VALUES (?, ?)', (name, program))
    connection.commit()

# Insert chord progressions
    chord_progs = load_json('chord_progressions.json')

    for key, progressions in chord_progs.items():
        genre_name, theme_name = key.split('_',1)         # key format: "genre_theme" (e.g., "trap_hard")
        
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
    connection.commit()

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
    connection.commit()
    connection.close()
    print("Database seeded successfully.")




if __name__ == "__main__":
    seed_database()