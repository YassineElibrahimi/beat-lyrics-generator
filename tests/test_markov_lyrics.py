from core.lyrics_generator import LyricsGenerator

def main():
    gen = LyricsGenerator(seed=42)
    themes = ['hard', 'melancholic', 'smooth', 'confident']
    for theme in themes:
        print(f"\n--- Theme: {theme} (Markov) ---")
        lyrics = gen.generate_verse_markov(theme, num_bars=4, rhyme_scheme='AABB')
        for line in lyrics:
            print(line)

if __name__ == '__main__':
    main()