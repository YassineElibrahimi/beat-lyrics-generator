"""
Edge case tests for the LyricsGenerator.
Uses a temporary database and mock configurations to test robustness.
"""

import os
import shutil
import tempfile
import time
import gc
import unittest
import sqlite3
import json
from unittest.mock import patch
from core.lyrics_generator import LyricsGenerator
from core.config import DB_PATH, THEME_CONFIG_PATH, START_TOKEN, END_TOKEN

class TestEdgeCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary directory for test files
        cls.test_dir = tempfile.mkdtemp()

    def setUp(self):
        # Generate a unique temporary database file for each test
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix='.db', dir=self.test_dir)
        os.close(self.temp_db_fd)  # Close the file descriptor so we can use sqlite

    def tearDown(self):
        # Delete the generator reference to help release any connections
        if hasattr(self, 'gen'):
            del self.gen
        # Force garbage collection to close any lingering connections
        gc.collect()
        # Attempt to remove the temporary database file with retries
        for attempt in range(10):
            try:
                if os.path.exists(self.temp_db_path):
                    os.unlink(self.temp_db_path)
                break
            except PermissionError:
                if attempt == 9:
                    # If still failing after 10 attempts, raise
                    raise
                time.sleep(0.2)  # wait a bit and retry

    @classmethod
    def tearDownClass(cls):
        # Ensure all generators are gone and files released
        gc.collect()
        time.sleep(0.5)
        shutil.rmtree(cls.test_dir)

    # ---------- Missing Database ----------
    def test_missing_database(self):
        """Test behavior when the database file does not exist."""
        # Use a nonexistent path
        self.gen = LyricsGenerator(db_path=os.path.join(self.test_dir, 'nonexistent.db'))
        words = self.gen.get_theme_words('hard')
        self.assertEqual(words, [])
        # Generate a line should fallback to placeholder
        line = self.gen.generate_line([])
        self.assertEqual(line, "[no words available]")

    # ---------- Empty vocabulary ----------
    def test_empty_vocabulary(self):
        """Test when get_theme_words returns empty list."""
        # Create a database with the vocabulary table but no data
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE vocabulary (
                theme TEXT,
                word TEXT,
                frequency INTEGER
            )
        ''')
        conn.commit()
        conn.close()
        self.gen = LyricsGenerator(db_path=self.temp_db_path)
        words = self.gen.get_theme_words('hard')
        self.assertEqual(words, [])
        line = self.gen.generate_line(words)
        self.assertEqual(line, "[no words available]")

    # ---------- Missing Markov tables ----------
    def test_missing_markov_tables(self):
        """Test Markov generation when tables are missing."""
        # Create a database with only vocabulary table (no markov tables)
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE vocabulary (
                theme TEXT,
                word TEXT,
                frequency INTEGER
            )
        ''')
        conn.commit()
        conn.close()
        self.gen = LyricsGenerator(db_path=self.temp_db_path)
        # Should fall back to vocabulary generation, which is empty
        line = self.gen.generate_line_markov('hard')
        self.assertEqual(line, "[no words available]")

    # ---------- Invalid theme config ----------
    def test_invalid_theme_config(self):
        """Test when theme_config.json is missing or invalid."""
        # Use a temporary invalid config file
        invalid_config = os.path.join(self.test_dir, 'invalid_config.json')
        with open(invalid_config, 'w') as f:
            f.write("{ invalid json")
        # Monkeypatch THEME_CONFIG_PATH to point to invalid file
        with patch('core.config.THEME_CONFIG_PATH', invalid_config):
            self.gen = LyricsGenerator(db_path=self.temp_db_path)
            # Should load default config
            config = self.gen._load_theme_config()
            self.assertIn('themes', config)
            self.assertIn('default_theme', config)
            self.assertEqual(config['default_theme'], 'hard')

    # ---------- Empty dataset (no lines) ----------
    def test_empty_dataset(self):
        """Test with a database that has no lines/vocabulary."""
        # Use empty database (no tables at all)
        conn = sqlite3.connect(self.temp_db_path)
        conn.close()
        self.gen = LyricsGenerator(db_path=self.temp_db_path)
        words = self.gen.get_theme_words('hard')
        self.assertEqual(words, [])
        line = self.gen.generate_line(words)
        self.assertEqual(line, "[no words available]")
        # Markov should also fall back
        line2 = self.gen.generate_line_markov('hard')
        self.assertEqual(line2, "[no words available]")

    # ---------- Missing start tokens in Markov ----------
    def test_missing_start_tokens(self):
        """Test Markov generation when START_TOKEN has no transitions."""
        # Create a database with markov_transitions but no START_TOKEN entry
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE markov_transitions (
                theme TEXT,
                prev_word TEXT,
                next_word TEXT,
                count INTEGER
            )
        ''')
        # Insert a transition that does not start with START_TOKEN
        cursor.execute('''
            INSERT INTO markov_transitions (theme, prev_word, next_word, count)
            VALUES (?, ?, ?, ?)
        ''', ('hard', 'word1', 'word2', 5))
        conn.commit()
        conn.close()
        self.gen = LyricsGenerator(db_path=self.temp_db_path)
        # Should fall back to vocabulary generation (which is empty because no vocab table)
        line = self.gen.generate_line_markov('hard')
        self.assertEqual(line, "[no words available]")

if __name__ == '__main__':
    unittest.main()