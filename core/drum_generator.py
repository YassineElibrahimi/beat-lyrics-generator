# core/drum_generator.py

"""
Explanation:
This script defines a DrumGenerator class for programmatic drum pattern creation based on genre-specific probabilities stored in a SQLite database.
It supports generation of kick, snare, hi-hat, and open-hat patterns and allows partial regeneration of individual instruments.

Key functionalities include:
- '_get_connection': establishes a connection to the SQLite database.
- 'load_patterns': loads all drum patterns for a given genre, returning a dictionary of instrument names to probability lists (parsed from JSON).
- 'generate_pattern': generates a full 16-step drum grid for each instrument, using probabilities to determine hits, and converts the grid to MIDI events (step, note, velocity). Can optionally regenerate specific instruments while keeping others unchanged.
- 'regenerate_kick/snare/hihat/open_hat': convenience methods to regenerate only the specified instrument.
- 'get_all_events': generates all drum patterns for a genre and returns a flat, time-sorted list of events with time in beats, suitable for sequencing or MIDI output.

The class uses a persistent 'current_grid' attribute to maintain state between partial regenerations, ensuring consistent patterns across calls.
"""

"""
*Content:
DrumGenerator.__init__()
DrumGenerator._get_connection()
DrumGenerator.load_patterns()
DrumGenerator.generate_pattern()
DrumGenerator.regenerate_kick()
DrumGenerator.regenerate_snare()
DrumGenerator.regenerate_hihat()
DrumGenerator.regenerate_open_hat()
DrumGenerator.get_all_events()
"""



import random
import sqlite3
import json





class DrumGenerator:
    # MIDI note number for standard drum sound
    DRUM_NOTES = {
        'kick'      : 36,
        'snare'     : 38,
        'hihat'     : 42,
        'open_hat'  : 46
    }

    def __init__(self, db_path='data/beat_lyrics.db', seed=None):
        self.db_path = db_path
        if seed is not None:
            random.seed(seed)

    def _get_connection(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def load_patterns(self, genre):
        """
        Load all patterns for a given genre from the database
        Returns a dictionary: {instrument_name: probabilities_list}
        """
        with self._get_connection() as connection:
            cursor = connection.cursor()
            # Get genre id
            cursor.execute('SELECT id FROM genres WHERE name = ?', (genre,))
            row = cursor.fetchone()
            if not row:
                raise ValueError (f"Genre '{genre}' not found.")
            genre_id = row['id']

        # Get all patterns for this genre
            cursor.execute('''
                SELECT pattern_name, probabilities FROM drum_patterns
                WHERE genre_id = ? ''', (genre_id,)
            )
            rows = cursor.fetchall()

        if not rows:
            raise ValueError(f"No drum patterns found for genre '{genre}'.")

        patterns = {}
        for row in rows:
            name = row['pattern_name']
            # Probabilities stored as JSON string
            prob_list = json.loads(row['probabilities'])
            patterns[name] = prob_list
        return patterns

    def generate_pattern(self, genre, regenerate=None):
        """
        1. Generate a full drum pattern for the genre.
        regenerate: 'optional' list of instrument names to regenerate (others keep previous values).
        2. Returns a dictionary with instrument names as keys and lists of (step_index, note, velocity) events.
        3. Also stores the full 16-step grid for each instrument in self.current_grid.
        """
        patterns = self.load_patterns(genre)
        # If we don't have a stored grid yet, create empty.
        if not hasattr(self, 'current_grid'):
            self.current_grid = {}

        result_events = {}
        for instrument, prob_list in patterns.items():
            # Check if we should regenerate this instrument
            if regenerate is not None and instrument not in regenerate:
                # Use existing grid if available, else generate anyway (shouldn't happen)
                if instrument in self.current_grid:
                    events = []     # Convert grid to events
                    for step, active in enumerate(self.current_grid[instrument]):
                        if active:
                            events.append((step, self.DRUM_NOTES[instrument], 100))
                    result_events[instrument] = events
                    continue
                # else fall through to generate

            # Generate new pattern for this instrument
            grid    = []
            events  = []
            
            for step, prob in enumerate(prob_list):
                active = random.random() < prob
                grid.append(active)
                if active:
                    note_val = self.DRUM_NOTES.get(instrument)  # safer lookup; note_value = MIDI number for this drum
                    if note_val is not None:
                        events.append((step, note_val, 100))
            self.current_grid[instrument]   = grid
            result_events[instrument]       = events

        return result_events

    def regenerate_kick(self, genre):
        """Regenerate only the kick pattern."""
        return self.generate_pattern(genre, regenerate=['kick'])

    def regenerate_snare(self, genre):
        """Regenerate only the snare pattern."""
        return self.generate_pattern(genre, regenerate=['snare'])

    def regenerate_hihat(self, genre):
        """Regenerate only the hihat pattern."""
        return self.generate_pattern(genre, regenerate=['hihat'])

    def regenerate_open_hat(self, genre):
        """Regenerate only the open_hat pattern."""
        return self.generate_pattern(genre, regenerate=['open_hat'])

    def get_all_events(self, genre):
        """
        Convenience method: generate all patterns and return a flat list of (time, note, velocity)
        for the entire bar, assuming 16 steps per bar at the given tempo.
        Time is in beats (quarter notes) - step = i * 0.25 (16th note = 0.25 beats).
        """
        patterns    = self.generate_pattern(genre)     # This regenerates everything
        events      = []

        for instrument, events_list in patterns.items():
            for step, note, velocity in events_list:
                time_in_beats = step * 0.25            # 16th note resolution
                events.append((time_in_beats, note, velocity))

        # Sorted by time
        events.sort(key=lambda x: x[0])
        return events