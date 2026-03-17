# core/lyrics_generator.py

"""
Explanation:
This script defines a LyricsGenerator class that creates lyrics programmatically using a database of theme-based words.
It connects to a SQLite database containing a 'vocabulary' table, retrieves words matching a theme, and assembles them into lines, verses, hooks, and full songs.

Key functionalities include:
- 'get_theme_words': fetches high-frequency words for a specific theme from the database.
- 'generate_line': constructs a single line by randomly selecting words from the theme vocabulary.
- 'generate_rhyming_couplet': generates two lines where the second line rhymes with the first, using the 'pronouncing' library.
- 'generate_verse': builds a verse of multiple lines, optionally following a rhyme scheme (default AABB).
- 'generate_hook': generates shorter lines suitable for a chorus or hook.
- 'generate_full_lyrics': assembles a full song according to a user-defined structure (e.g., 'verse-hook-verse-hook') with configurable line counts.

The class allows seeded randomness for reproducibility and leverages rhyming dictionaries to add lyrical coherence.
"""

"""
*Content:
LyricsGenerator.__init__()
LyricsGenerator._get_connection()
LyricsGenerator.get_theme_words()
LyricsGenerator.generate_line()
LyricsGenerator.generate_rhyming_couplet()
LyricsGenerator.generate_verse()
LyricsGenerator.generate_hook()
LyricsGenerator.generate_full_lyrics()
"""




import sqlite3
import random
import pronouncing
import json
import os



class LyricsGenerator:
    def __init__(self, db_path='data/beat_lyrics.db', seed=None):
        self.db_path = db_path
        self._theme_config = None
        self.START_TOKEN = "__START__"
        self.END_TOKEN = "__END__"
        if seed:
            random.seed(seed)

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _load_theme_config(self):
        """
        Load and cache theme configuration from JSON file.
        Provides fallback if file missing or invalid.
        """
        if self._theme_config is None:
            config_path = os.path.join('data', 'theme_config.json')
            # Default minimal config in case file is missing
            default_config = {
                "themes": {
                    "hard": {
                        "sentiment_range": [-1.0, -0.1],
                        "keywords": ["grind", "hustle"],
                        "genres": ["trap", "drill"]},
                    "melancholic": {
                        "sentiment_range": [-0.3, 0.1],
                        "keywords": ["lost", "pain"],
                        "genres": ["any"]},
                    "smooth": {
                        "sentiment_range": [0.1, 0.9],
                        "keywords": ["vibe", "love"],
                        "genres": ["trap", "boom-bap"]}
                },
                "default_theme": "hard"
            }
            try:
                with open(config_path, 'r') as f:
                    self._theme_config = json.load(f)
            except FileNotFoundError:
                print(f"Warning: Theme config not found at {config_path}. Using hardcoded defaults.")
                self._theme_config = default_config
            except json.JSONDecodeError:
                print(f"Error: Theme config at {config_path} is invalid JSON. Using hardcoded defaults.")
                self._theme_config = default_config
        return self._theme_config

    def get_themes_for_genre(self, genre):
        """
        Return a list of theme names that match the given genre.
        A theme matches if its 'genres' list contains the genre or 'any'.
        """
        config = self._load_theme_config()
        matching_themes = []
        for theme_name, theme_data in config['themes'].items():
            genres = theme_data.get('genres', [])
            if genre in genres or 'any' in genres:
                matching_themes.append(theme_name)
        return matching_themes

    def get_default_theme(self):
        """Return the default theme from config."""
        config = self._load_theme_config()
        return config.get('default_theme', 'hard')

    # ---------- Vocabulary methods ----------
    def get_theme_words(self, theme, min_freq=2, limit=200):
        """Retrieve words for a given theme with frequency >= min_freq."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT word FROM vocabulary
                    WHERE theme = ? AND frequency >= ?
                    ORDER BY frequency DESC
                    LIMIT ?
                ''', (theme, min_freq, limit))
                rows = cursor.fetchall()
                return [row['word'] for row in rows]
        except sqlite3.Error as e:
            print(f"Database error in get_theme_words: {e}")
            return []

    def generate_line(self, theme_words, length_range=(4, 8)):
        """Generate a single line by randomly selecting words from theme vocabulary."""
        if not theme_words:
            return "[no words available]"
        num_words = random.randint(*length_range)
        # Ensure we don't try to choose more words than available
        k = min(num_words, len(theme_words))
        line_words = random.choices(theme_words, k=k)
        line = ' '.join(line_words)
        return line.capitalize()

    def generate_rhyming_couplet(self, theme_words, line1=None):
        """Generate two lines that rhyme (AABB scheme)."""
        if line1 is None:
            line1 = self.generate_line(theme_words)
        last_word = line1.split()[-1].lower()
        rhymes    = pronouncing.rhymes(last_word)
        if not rhymes:
            line2 = self.generate_line(theme_words)
        else:
            rhyme_word  = random.choice(rhymes)
            num_words   = random.randint(4, 8)
            other_words = random.choices(theme_words, k=num_words-1)
            line2       = ' '.join(other_words + [rhyme_word]).capitalize()
        return line1, line2

    def generate_verse(self, theme, num_bars=16, rhyme_scheme='AABB'):
        """Generate a verse of num_bars lines."""
        theme_words = self.get_theme_words(theme)
        lines = []
        i = 0
        while i < num_bars:
            if rhyme_scheme == 'AABB':
                line1, line2 = self.generate_rhyming_couplet(theme_words)
                lines.append(line1)
                lines.append(line2)
                i += 2
            else:
                lines.append(self.generate_line(theme_words))
                i += 1
        return lines[:num_bars]

    def generate_hook(self, theme, num_lines=4):
        """Generate a hook (chorus) - can be shorter lines."""
        theme_words = self.get_theme_words(theme)
        hook = []
        for _ in range(num_lines):
            line = self.generate_line(theme_words, length_range=(3, 6))
            hook.append(line)
        return hook

    def generate_full_lyrics(self, theme, structure='verse-hook-verse-hook', bars_verse=16, bars_hook=8):
        """Generate lyrics according to structure."""
        sections  = structure.split('-')
        all_lines = []
        for section in sections:
            if section == 'verse':
                lines = self.generate_verse(theme, num_bars=bars_verse)
                all_lines.extend(lines)
            elif section == 'hook':
                lines = self.generate_hook(theme, num_lines=bars_hook)
                all_lines.extend(lines)
        return all_lines

    # ---------- Markov methods ----------
    def load_markov_transitions(self, theme, prev_word):
        """Return a list of (next_word, count) for given theme and prev_word."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT next_word, count FROM markov_transitions
                    WHERE theme = ? AND prev_word = ?
                ''', (theme, prev_word))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error in load_markov_transitions: {e}")
            return []

    def weighted_choice(self, items, temperature=1.0):
        """
        items: list of (item, weight)
        temperature: >0.
                    Lower = more conservative (picks high-weight items more often),
                    higher = more random. 1.0 is standard.
        Returns chosen item.
        """
        if temperature <= 0:
            raise ValueError("Temperature must be > 0")
        
        # Adjust weights by temperature
        weights = [weight ** (1.0 / temperature) for _, weight in items]
        total = sum(weights)
        r = random.uniform(0, total)
        upto = 0
        for (item, _), weight in zip(items, weights):
            upto += weight
            if upto >= r:
                return item
        return items[-1][0]  # fallback

    def generate_line_markov(self, theme, min_words=4, max_words=8, temperature=1.0):
        """Generate a line using bigram Markov model with weighted sampling.
        temperature: randomness control (lower = more predictable, higher = more creative).
        """
        # First, get possible first words from START_TOKEN
        start_transitions = self.load_markov_transitions(theme, self.START_TOKEN)
        if not start_transitions:
            # Fallback to random vocabulary
            return self.generate_line(self.get_theme_words(theme))

        first_word = self.weighted_choice(start_transitions, temperature)
        words = [first_word]

        for _ in range(max_words - 1):
            prev = words[-1]
            transitions = self.load_markov_transitions(theme, prev)
            if not transitions:
                break
            next_word = self.weighted_choice(transitions, temperature)
            if next_word == self.END_TOKEN:
                break
            words.append(next_word)
            if len(words) >= max_words:
                break

        # Pad if too short
        while len(words) < min_words:
            theme_words = self.get_theme_words(theme)
            if theme_words:
                words.append(random.choice(theme_words))
            else:
                break

        return ' '.join(words).capitalize()

    def generate_rhyming_couplet_markov(self, theme, line1=None, temperature=1.0):
        if line1 is None:
            line1 = self.generate_line_markov(theme, temperature=temperature)
        last_word = line1.split()[-1].lower()
        rhymes = pronouncing.rhymes(last_word)
        if not rhymes:
            line2 = self.generate_line_markov(theme, temperature=temperature)
        else:
            rhyme_word = random.choice(rhymes)
            line2 = self.generate_line_markov(theme, temperature=temperature)
            # Replace last word with rhyme word
            words = line2.split()
            if words:
                words[-1] = rhyme_word
                line2 = ' '.join(words).capitalize()
            else:
                line2 = rhyme_word.capitalize()
        return line1, line2

    def generate_verse_markov(self, theme=None, genre=None, num_bars=16, rhyme_scheme='AABB', temperature=1.0):
        """
        Generate a verse using Markov chains.
        Either theme or genre must be provided.
        If genre is given, pick a random matching theme.
        """
        if theme is None and genre is None:
            raise ValueError("Either theme or genre must be provided")

        # Determine which theme to use
        if genre is not None:
            matching_themes = self.get_themes_for_genre(genre)
            if not matching_themes:
                # Fallback to default theme
                theme = self.get_default_theme()
                print(f"Warning: No themes match genre '{genre}'. Using default theme: {theme}")
            else:
                theme = random.choice(matching_themes)

        lines = []
        i = 0
        while i < num_bars:
            if rhyme_scheme == 'AABB':
                line1, line2 = self.generate_rhyming_couplet_markov(theme, temperature=temperature)
                lines.append(line1)
                lines.append(line2)
                i += 2
            else:
                lines.append(self.generate_line_markov(theme, temperature=temperature))
                i += 1
        return lines[:num_bars]

    def generate_full_lyrics_markov(self, theme=None, genre=None, structure='verse-hook-verse-hook', bars_verse=16, bars_hook=8, temperature=1.0):
        """
        Generate full lyrics using Markov.
        Either theme or genre must be provided.
        """
        if theme is None and genre is None:
            raise ValueError("Either theme or genre must be provided")

        # Determine which theme to use
        if genre is not None:
            matching_themes = self.get_themes_for_genre(genre)
            if not matching_themes:
                theme = self.get_default_theme()
                print(f"Warning: No themes match genre '{genre}'. Using default theme: {theme}")
            else:
                theme = random.choice(matching_themes)

        sections = structure.split('-')
        all_lines = []
        for section in sections:
            if section == 'verse':
                lines = self.generate_verse_markov(theme=theme, num_bars=bars_verse, temperature=temperature)
                all_lines.extend(lines)
            elif section == 'hook':
                for _ in range(bars_hook):
                    all_lines.append(self.generate_line_markov(theme, min_words=3, max_words=6, temperature=temperature))
        return all_lines