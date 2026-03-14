# data/database.py

"""
Explanation:
This script sets up and manages the core SQLite database used for beat and lyric generation.
It provides functions to connect to the database and initialize essential tables if they do not exist.

Key functionalities include:
- 'get_connection': returns a SQLite connection with row access by column name and enforces foreign key constraints.
- 'init_db': creates tables required for musical and lyrical generation:
    - 'genres': stores unique music genres.
    - 'themes': stores lyrical themes.
    - 'instruments': stores instrument names with corresponding MIDI program numbers.
    - 'chord_progressions': stores chord sequences in Roman numeral format, linked to genres and themes.
    - 'drum_patterns': stores probability grids for percussion patterns per genre, saved as JSON.

This setup ensures the database has all tables needed to store musical structures and rhythmic patterns for procedural generation.
"""

"""
*Content:
get_connection()
init_db()
"""










import os
import sqlite3




DB_PATH = os.path.join(os.path.dirname(__file__),'beat_lyrics.db')

def get_connection():
    """Return a connection to the database"""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row            # access columns by name
    connection.execute("PRAGMA foreign_keys = ON")  # ensures referential integrity. 
    return connection

# ============== CREATE TABLES ==============

def init_db():
    """Create tables if they don't exist."""
    with get_connection() as connect:
        cursor = connect.cursor()

        # Genres table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS genres (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT UNIQUE NOT NULL
            )
        ''')

        # Theme table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS themes(
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT UNIQUE NOT NULL
            )
        ''')

        # Instruments table (MIDI program number)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS instruments (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT UNIQUE NOT NULL,
                midi_program    INTEGER NOT NULL
            )
        ''')

        # Chord progressions table (use roman numeral "i,III,iv,VI")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chord_progressions (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                genre_id        INTEGER NOT NULL,
                theme_id        INTEGER NOT NULL,
                roman_numerals  TEXT NOT NULL,               -- "i,III,iv,VI"
                FOREIGN KEY (genre_id) REFERENCES genres(id),
                FOREIGN KEY (theme_id) REFERENCES themes(id)
            )
        ''')

        # Drum patterns table (probabilities as JSON)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drum_patterns (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                genre_id        INTEGER NOT NULL,
                pattern_name    TEXT NOT NULL,              -- "kick", "snare", "hi-hat"
                probabilities   TEXT NOT NULL,              -- JSON array of float
                FOREIGN KEY (genre_id) REFERENCES genres(id)
            )
        ''')