from core.chord_generator import ChordGenerator
from core.melody_generator import MelodyGenerator
from core.drum_generator import DrumGenerator
from core.midi_exporter import MIDIExporter




def main():
    # Parameters
    genre = 'trap'
    theme = 'hard'
    key = 'C'
    tempo = 140

    print("Generating chord progression...")
    chord_gen = ChordGenerator()
    chords = chord_gen.generate(genre, theme, key_name=key)
    print(f"Generated {len(chords)} chords.")

    print("Generating melody...")
    melody_gen = MelodyGenerator(seed=42)
    melody = melody_gen.generate_melody(chords, key_name=key, durations_per_chord=4)

    print("Generating drums...")
    drum_gen = DrumGenerator(seed=42)
    drum_events = drum_gen.get_all_events(genre)

    print("Creating MIDI file...")
    exporter = MIDIExporter(tempo=tempo)

    # Add tracks
    exporter.add_chords(chords, program=1)   # piano
    exporter.add_melody(melody, program=73)  # flute
    exporter.add_drums(drum_events)

    # Save MIDI
    output_file = 'test_output.mid'
    exporter.save(output_file)
    print(f"MIDI saved as {output_file}")

if __name__ == '__main__':
    main()