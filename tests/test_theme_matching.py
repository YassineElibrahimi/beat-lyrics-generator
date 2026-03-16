from core.lyrics_generator import LyricsGenerator

def main():
    gen = LyricsGenerator(seed=42)
    beat_genres = ['trap', 'drill', 'old_school']
    
    print("=" * 60)
    print("THEME MATCHING TEST: Beat Genre → Lyrics Theme")
    print("=" * 60)
    
    for beat_genre in beat_genres:
        print(f"\n--- Beat Genre: {beat_genre.upper()} ---")
        
        # Get matching themes for this genre
        matching_themes = gen.get_themes_for_genre(beat_genre)
        print(f"Matching themes: {', '.join(matching_themes) if matching_themes else 'None'}")
        
        # Generate a verse using genre-based theme selection
        print(f"\nGenerated lyrics (theme auto-selected from genre):")
        lyrics = gen.generate_verse_markov(genre=beat_genre, num_bars=4, rhyme_scheme='AABB')
        for line in lyrics:
            print(f"  {line}")
        
        # Also show a few lines with each matching theme individually
        if matching_themes:
            print(f"\nIndividual theme samples:")
            for theme in matching_themes[:3]:  # show up to 3 themes
                print(f"\n  Theme: {theme}")
                sample = gen.generate_verse_markov(theme=theme, num_bars=2, rhyme_scheme='AABB')
                for line in sample:
                    print(f"    {line}")

if __name__ == '__main__':
    main()