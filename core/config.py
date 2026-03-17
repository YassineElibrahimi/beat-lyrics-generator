# core/config.py
"""
Centralized configuration for the Beat & Lyrics Generator.
"""

import os

# Database configuration
DB_PATH = os.path.join('data', 'beat_lyrics.db')

# Markov tokens
START_TOKEN = "__START__"
END_TOKEN = "__END__"

# Theme configuration file path
THEME_CONFIG_PATH = os.path.join('data', 'theme_config.json')

# Default theme fallback
DEFAULT_THEME = "hard"