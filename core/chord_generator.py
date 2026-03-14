# core/chord_generator.py

"""
Explanation:
This script defines a ChordGenerator class that creates musical chord progressions based on genre and theme data stored in a SQLite database.
It leverages the 'music21' library to convert Roman numeral progressions into actual chords in a specified key.

Key functionalities include:
- '_get_connection': establishes a connection to the SQLite database.
- 'get_random_progression': queries the database for all chord progressions matching a given genre and theme, and selects one at random. Returns a list of Roman numeral strings.
- 'roman_to_chords': converts a list of Roman numerals into 'music21' Chord objects in the specified key, assigning a standard whole-note duration for each chord.
- 'generate': high-level method combining the above two steps to return a ready-to-use list of chord objects for musical composition.

This setup allows dynamic generation of chord sequences tailored to specific musical styles or lyrical themes.
"""

"""
*Content:
ChordGenerator.__init__()
ChordGenerator._get_connection()
ChordGenerator.get_random_progression()
ChordGenerator.roman_to_chords()
ChordGenerator.generate()
"""









import random
import sqlite3
from music21 import roman, key




class ChordGenerator:
    def __init__(self, db_path='data/beat_lyrics.db'):
        self.db_path = db_path

    def _get_connection(self):
        """Return a database connection."""
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def get_random_progression(self, genre, theme):
        """
        Retrieve a random Roman numeral progression from the database
        for the given genre and theme.
        Returns a list of Roman numeral strings (e.g., ['i', 'III', 'iv', 'VI']).
        """
        with self._get_connection() as connection:
            cursor = connection.cursor()
        # Get genre id
            cursor.execute('SELECT id FROM genres WHERE name = ?', (genre,))
            genre_row = cursor.fetchone()
            if not genre_row:
                raise ValueError(f"Genre '{genre}' not found in database.")
            genre_id = genre_row['id']
        # Get theme id
            cursor.execute('SELECT id FROM themes WHERE name = ?', (theme,))
            theme_row = cursor.fetchone()
            if not theme_row:
                raise ValueError(f"Theme '{theme}' not found in database.")
            theme_id = theme_row['id']

        # Get all progressions for that genre/theme
            cursor.execute('''
                SELECT roman_numerals FROM chord_progressions
                WHERE genre_id = ? AND theme_id = ? ''', (genre_id, theme_id))
            rows = cursor.fetchall()
            if not rows:
                raise ValueError(f"No progression found for genre '{genre}' and theme '{theme}'.")

        # Choose a random progression
            chosen = random.choice(rows)
            numerals = [n.strip() for n in chosen['roman_numerals'].split(',')] # roman_numerals is a comma-sep str : "i,III,iv,VI"
            return numerals

    def roman_to_chords(self, roman_list, key_name='C'):
        """
        Convert a list of Roman numeral strings into a list of music21 Chord objects
        in the specified key.
        """
    # Create a key object
        key_obj = key.Key(key_name)
        chords = []

        for roman_numeral in roman_list:
    # Create a RomanNumeral object
            roman_numeral_obj = roman.RomanNumeral(roman_numeral, key_obj)
            roman_numeral_obj.duration.quarterLength = 4.0       # Set a standard duration "whole note"
            chords.append(roman_numeral_obj)
        return chords

    def generate(self, genre, theme, key_name='C'):
        """
        High-level method: get a random progression and convert to chords.
        Returns a list of music21 Chord objects.
        """
        roman_list = self.get_random_progression(genre, theme)
        chords = self.roman_to_chords(roman_list, key_name)
        return chords