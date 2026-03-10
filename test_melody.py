from core.chord_generator import ChordGenerator
from core.melody_generator import MelodyGenerator

def main():
    # First, get a chord progression
    chord_gen = ChordGenerator()
    chords = chord_gen.generate(genre='trap', theme='hard', key='C')
    print(f"Generated {len(chords)} chords.")

    # Now generate a melody
    melody_gen = MelodyGenerator(seed=42)  # fixed seed for repeatability
    melody = melody_gen.generate_melody(chords, key_name='C', durations_per_chord=4)

    # Print first few notes
    notes = list(melody.notes)
    print(f"Generated {len(notes)} melody notes.")
    for i, n in enumerate(notes[:8]):  # show first 8
        print(f"Note {i+1}: {n.nameWithOctave} ({n.pitch.midi}) duration={n.quarterLength}")

if __name__ == '__main__':
    main()