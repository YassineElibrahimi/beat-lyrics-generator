"""
Explanation:
Command-line interface for Beat & Lyrics Generator.
Allows generating a beat with selected parameters.

*Content:
print_header()
get_user_choices()
generate_and_play()
main()
"""

import sys
import pygame
from core.chord_generator import ChordGenerator
from core.melody_generator import MelodyGenerator
from core.drum_generator import DrumGenerator
from core.midi_exporter import MIDIExporter


def print_header():
    print("=" * 50)
    print(" ------------ BEAT & LYRICS GENERATOR ------------ ")
    print("=" * 50)

def get_user_choices():
    print("\nAvailable genres: trap, drill")
    genre = input("- Enter Genre (trap/drill): ").strip() or "trap"

    print("\nAvailable themes: hard, melancholic")
    theme = input("- Enter Theme (hard/melancholic): ").strip() or "hard"

    print("\nAvailable keys: C, C#, D, D#, E, F, F#, G, G#, A, A#, B")
    key = input("- Enter Key (C): ").strip() or "C"

    tempo_str = input("- Enter Tempo BPM (140): ").strip()
    tempo = int(tempo_str) if tempo_str else 140

    return genre, theme, key, tempo

def generate_and_play(genre, theme, key, tempo):
    print(f"\nGenerating beat: {genre}, {theme}, {key}, {tempo} BPM...")

    # Chord generator
    chord_gen = ChordGenerator()
    chords = chord_gen.generate(genre, theme, key)
    print(f"  - Generated {len(chords)} chords")

    # Melody generator
    melody_gen = MelodyGenerator(seed=42)
    melody = melody_gen.generate_melody(chords, key_name=key, durations_per_chord=4)
    notes = list(melody.notes)
    print(f"  - Generated {len(notes)} melody notes")

    # Drum generator
    drum_gen = DrumGenerator(seed=42)
    drum_events = drum_gen.get_all_events(genre)
    print(f"  - Generated drum patterns")

    # Export to MIDI
    exporter = MIDIExporter(tempo=tempo)
    exporter.add_chords(chords, program=1)   # piano
    exporter.add_melody(melody, program=73)  # flute
    exporter.add_drums(drum_events)

    filename = f"beat_{genre}_{theme}_{key}_{tempo}.mid"
    exporter.save(filename)
    print(f"  - Saved MIDI to {filename}")

    # Play the MIDI
    print("\nPlaying beat... (press Ctrl+C to stop)")
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)

def main():
    print_header()
    genre, theme, key_name, tempo = get_user_choices()
    try:
        generate_and_play(genre, theme, key_name, tempo)
    except KeyboardInterrupt:
        print("\nStopped.")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()