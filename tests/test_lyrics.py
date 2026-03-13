from core.lyrics_generator import LyricsGenerator

def main():
    gen = LyricsGenerator(seed=42)
    theme = 'hard'
    lyrics = gen.generate_full_lyrics(theme, structure='verse-hook-verse-hook', bars_verse=8, bars_hook=4)
    for line in lyrics:
        print(line)

if __name__ == '__main__':
    main()