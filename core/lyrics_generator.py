import sqlite3
import random
import pronouncing

class LyricsGenerator:
    def __init__(self, db_path='data/beat_lyrics.db', seed=None):
        self.db_path = db_path
        if seed:
            random.seed(seed)

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_theme_words(self, theme, min_freq=2, limit=200):
        """Retrieve words for a given theme with frequency >= min_freq."""
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

    def generate_line(self, theme_words, length_range=(4, 8)):
        """Generate a single line by randomly selecting words from theme vocabulary."""
        num_words = random.randint(*length_range)
        line_words = random.choices(theme_words, k=num_words)
        line = ' '.join(line_words)
        return line.capitalize()

    def generate_rhyming_couplet(self, theme_words, line1=None):
        """Generate two lines that rhyme (AABB scheme)."""
        if line1 is None:
            line1 = self.generate_line(theme_words)
        last_word = line1.split()[-1].lower()
        rhymes = pronouncing.rhymes(last_word)
        if not rhymes:
            line2 = self.generate_line(theme_words)
        else:
            rhyme_word = random.choice(rhymes)
            num_words = random.randint(4, 8)
            other_words = random.choices(theme_words, k=num_words-1)
            line2 = ' '.join(other_words + [rhyme_word]).capitalize()
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
        """Generate a hook (chorus) – can be shorter lines."""
        theme_words = self.get_theme_words(theme)
        hook = []
        for _ in range(num_lines):
            line = self.generate_line(theme_words, length_range=(3, 6))
            hook.append(line)
        return hook

    def generate_full_lyrics(self, theme, structure='verse-hook-verse-hook', bars_verse=16, bars_hook=8):
        """Generate lyrics according to structure."""
        sections = structure.split('-')
        all_lines = []
        for section in sections:
            if section == 'verse':
                lines = self.generate_verse(theme, num_bars=bars_verse)
                all_lines.extend(lines)
            elif section == 'hook':
                lines = self.generate_hook(theme, num_lines=bars_hook)
                all_lines.extend(lines)
        return all_lines