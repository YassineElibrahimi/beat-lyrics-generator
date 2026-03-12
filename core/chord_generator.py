# core/chord_generator.py

"""
Explanation:
'get_random_progression' queries the database for all progressions matching the genre and theme,
then picks one at random.
'roman_to_chords' uses 'music21.roman.RomanNumeral' to parse a Roman numeral string (like "i") in the context of a key, and extracts the actual chord.
I assign a whole-note duration for now (chord_obj.duration.quarterLength = 4.0);
later we'll adjust based on tempo and style.
'generate' combines both steps.

*Content:
get_random_progression()
roman_to_chords()
generate()
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