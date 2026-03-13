import sqlite3
import os

DB_PATH = os.path.join('data', 'beat_lyrics.db')

def init_lyrics_tables():
    """Create lyrics-related tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Artists table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Songs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            year INTEGER,
            FOREIGN KEY (artist_id) REFERENCES artists(id),
            UNIQUE(artist_id, title)
        )
    ''')

    # Lines table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            song_id INTEGER NOT NULL,
            line_number INTEGER,
            text TEXT NOT NULL,
            sentiment_score REAL,
            theme TEXT,
            FOREIGN KEY (song_id) REFERENCES songs(id)
        )
    ''')

    # Vocabulary table (theme-based keywords)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vocabulary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            theme TEXT NOT NULL,
            word TEXT NOT NULL,
            frequency INTEGER DEFAULT 1,
            UNIQUE(theme, word)
        )
    ''')

    conn.commit()
    conn.close()
    print("Lyrics tables created (if they didn't exist).")

if __name__ == '__main__':
    init_lyrics_tables()