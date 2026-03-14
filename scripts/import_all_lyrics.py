# scripts/import_all_lyrics.py

"""
Explanation:
This script imports song lyrics from multiple sources into a structured SQLite database.
It handles three datasets: a CSV of all lyrics, a folder of text files, and a raw lyrics CSV for NLP tasks.

Key steps include:
- Cleaning lyrics using 'clean_lyrics', which removes markers like [Verse] or [Chorus] and normalizes whitespace.
- Inserting artists, songs, and individual lyric lines into the database via 'insert_song_lines', including placeholder sentiment scores and themes.
- Handling multiple file encodings when reading text files to prevent decode errors.
- Iterating through CSV rows or text files, cleaning lyrics, and storing them systematically in the database tables 'artists', 'songs', and 'lines'.

The script is executable directly; running it processes all datasets and populates the database with cleaned lyrics ready for analysis or vocabulary building.
"""

"""
*Content:
clean_lyrics()
insert_song_lines()
import_all_lyrics()
import_txt_folder()
import_lyrics_raw()
main()
"""





import csv
import os
import re
import sqlite3
from data.database import get_connection




# csv.field_size_limit(sys.maxsize)
csv.field_size_limit(2**31 - 1)   # safe for Windows
# ---------- Helper Functions ----------
def clean_lyrics(text):
    """Remove [Verse], [Chorus], etc., and normalize whitespace."""
    text    = re.sub(r'\[.*?\]', '', text)
    text    = re.sub(r'\n\s*\n', '\n', text)
    lines   = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)

def insert_song_lines(conn, artist, song, lyrics, theme='hard'):    # label all lyrics as 'hard' for now
    """Insert artist, song, and lines into database."""
    cursor = conn.cursor()
    # Artist
    cursor.execute('INSERT OR IGNORE INTO artists (name) VALUES (?)', (artist,))
    cursor.execute('SELECT id FROM artists WHERE name = ?', (artist,))
    artist_id = cursor.fetchone()['id']
    # Song
    try:
        cursor.execute('''
            INSERT INTO songs (artist_id, title) VALUES (?, ?)
        ''', (artist_id, song))
        song_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        return  # song already exists
    # Lines
    lines = lyrics.split('\n')
    for idx, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        cursor.execute('''
            INSERT INTO lines (song_id, line_number, text, sentiment_score, theme)
            VALUES (?, ?, ?, ?, ?)
        ''', (song_id, idx, line, 0.0, theme))
    conn.commit()

# ---------- Dataset 1: all_lyrics.csv (Song Lyrics) ----------
def import_all_lyrics(conn, csv_path):
    print(f"Importing {csv_path} ...")
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            artist  = row.get('artist', '').strip()
            song    = row.get('Song', '').strip()
            lyrics  = row.get('lyrics', '').strip()
            if not artist or not song or not lyrics:
                continue
            cleaned = clean_lyrics(lyrics)
            insert_song_lines(conn, artist, song, cleaned)

# ---------- Dataset 2: 38 txt files (Rap Lyrics) ----------
def import_txt_folder(conn, folder_path):
    print(f"Importing from {folder_path} ...")
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    for filename in os.listdir(folder_path):
        if not filename.endswith('.txt'):
            continue
        artist      = filename.replace('.txt', '').replace('_', ' ').title()
        filepath    = os.path.join(folder_path, filename)
        lyrics      = None
        for enc in encodings:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    lyrics = f.read()
                break
            except UnicodeDecodeError:
                continue
        if lyrics is None:
            print(f"Warning: Could not decode {filename} with any encoding, skipping.")
            continue
        cleaned = clean_lyrics(lyrics)
        insert_song_lines(conn, artist, f"Various - {filename}", cleaned)

# ---------- Dataset 3: lyrics_raw.csv (Rap Lyrics for NLP) ----------
def import_lyrics_raw(conn, csv_path):
    print(f"Importing {csv_path} ...")
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            artist  = row.get('artist', '').strip()
            track   = row.get('track_name', '').strip()
            lyrics  = row.get('raw_lyrics', '').strip()
            if not artist or not track or not lyrics:
                continue
            cleaned = clean_lyrics(lyrics)
            insert_song_lines(conn, artist, track, cleaned)

# ---------- Main ----------
def main():
    conn = get_connection()
    import_all_lyrics(conn, 'data/raw_lyrics/rap_lyrics/all_lyrics.csv')
    import_txt_folder(conn, 'data/raw_lyrics/rap_lyrics_text/')
    import_lyrics_raw(conn, 'data/raw_lyrics/song_lyrics/lyrics_raw.csv')
    conn.close()
    print("All datasets imported.")

if __name__ == '__main__':
    main()