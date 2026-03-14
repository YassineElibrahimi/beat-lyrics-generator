"""
Explanation:
This script provides a command-line interface (CLI) for generating beats, melodies, and drum patterns,
exporting them to MIDI, and playing the result. It integrates the core generators and MIDI exporter.

Key functionalities include:
- 'print_header': prints a decorative CLI header.
- 'get_user_choices': prompts the user to select genre, theme, key, and tempo, providing defaults.
- 'play_beat': attempts to play the generated MIDI using FluidSynth with a SoundFont if available, otherwise falls back to pygame.
- 'generate_and_play': orchestrates the music generation process:
    1. Generates chord progression using ChordGenerator.
    2. Generates melody over chords using MelodyGenerator.
    3. Generates drum patterns using DrumGenerator.
    4. Exports chords, melody, and drums to MIDI using MIDIExporter.
    5. Saves the MIDI to a file and plays it.
- 'main': entry point; prints header, gathers user choices, and calls 'generate_and_play', handling KeyboardInterrupt and other exceptions gracefully.

This script effectively turns the core music generation modules into an interactive CLI tool for producing and listening to procedurally generated beats.
"""

"""
*Content:
print_header()
get_user_choices()
play_beat()
generate_and_play()
main()
"""









import os
import sys
import pygame
from core.chord_generator import ChordGenerator
from core.melody_generator import MelodyGenerator
from core.drum_generator import DrumGenerator
from core.midi_exporter import MIDIExporter




SOUNDFONT_PATH = os.path.join('resources', 'default_soundfont.sf2')

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

def play_beat(exporter, filename):
    """Try to play with FluidSynth if SoundFont exist, else fallback to pygame."""
    if os.path.exists(SOUNDFONT_PATH):
        print("Using FluidSynth with SoundFont...")
        exporter.play_with_fluidsynth(SOUNDFONT_PATH, filename)
    else:
        print("SoundFont not found. Using pygame fallback (low quality).")
        exporter.play(filename)

def generate_and_play(genre, theme, key, tempo):
    print(f"\nGenerating beat: {genre}, {theme}, {key}, {tempo} BPM...")

    # Chord generator
    chord_gen = ChordGenerator()
    chords = chord_gen.generate(genre, theme, key)
    print(f"  - Generated {len(chords)} chords")

    total_beats = sum(c.quarterLength for c in chords)
    num_bars = int(total_beats / 4)  # assume 4/4 time

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
    exporter.add_drums(drum_events, num_bars=num_bars)

    # Save midi
    filename = f"beat_{genre}_{theme}_{key}_{tempo}.mid"
    exporter.save(filename)
    print(f"  - Saved MIDI to {filename}")

    # Play the MIDI
    print("\nPlaying beat... (press Ctrl+C to stop)")
    play_beat(exporter, filename)
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