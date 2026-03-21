# core/midi_exporter.py

"""
Explanation:
This script defines a MIDIExporter class to convert chord progressions, melodies, and drum patterns into playable MIDI files.
It supports playback through pygame or FluidSynth (with optional SoundFont), and provides methods to save MIDI files for later use.

Key functionalities include:
- '__init__': initializes a PrettyMIDI object with a specified tempo.
- 'add_chords': adds a chord track from a list of music21 Chord objects.
- 'add_melody': adds a melody track from a music21 stream.Part.
- 'add_drums': adds a drum track (MIDI channel 9) using a list of events and allows repeating bars.
- 'save': writes the MIDI data to a file.
- 'play': plays a MIDI file using pygame.mixer, optionally using a temporary file.
- 'play_with_fluidsynth': renders MIDI to audio via FluidSynth using a SoundFont and plays the resulting WAV file, with fallback to pygame if FluidSynth is unavailable.

This class enables end-to-end audio generation from symbolic music representations, supporting both standard MIDI and sampled playback.
"""

"""
*Content:
MIDIExporter.__init__()
MIDIExporter.add_chords()
MIDIExporter.add_melody()
MIDIExporter.add_drums()
MIDIExporter.save()
MIDIExporter.play()
MIDIExporter.play_with_fluidsynth()
"""

# Basically, 'program' selects the instrument sound for that track:
# program=1 refers to Acoustic Grand Piano.
# program=73 → Flute
# program=25 → Acoustic Guitar








import pretty_midi
import tempfile
import os
import subprocess




class MIDIExporter:
    def __init__(self, tempo=140):
        self.tempo = tempo
        self.midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)

    def add_chords(self, chord_progression, start_time=0, program=1):
        """Add a chord track. chord_progression: list of music21 Chord objects."""
        track = pretty_midi.Instrument(program=program, name='chords')
        time = start_time
        for chord_obj in chord_progression:
            duration = chord_obj.quarterLength
            for pitch in chord_obj.pitches:
                note = pretty_midi.Note(
                    velocity=80,
                    pitch=pitch.midi,
                    start=time,
                    end=time + duration
                )
                track.notes.append(note)
            time += duration
        self.midi.instruments.append(track)

    def add_melody(self, melody_stream, start_time=0, program=73):
        """Add a melody track from a music21 Part stream."""
        track = pretty_midi.Instrument(program=program, name='Melody')
        time = start_time
        for note_obj in melody_stream.notes:
            duration = note_obj.quarterLength
            midi_note = pretty_midi.Note(
                velocity=80,
                pitch=note_obj.pitch.midi,
                start=time,
                end=time + duration
            )
            track.notes.append(midi_note)
            time += duration
        self.midi.instruments.append(track)

    def add_drums(self, drum_events, start_time=0, step_duration=0.25, num_bars=1):
        """
        Add a drum track (channel 9) repeating the pattern for num_bars.
        drum_events : list of (time_in_beats, note, velocity) events for one bar
        step_duration: duration of each drum hit in beats (default 16th note = 0.25)
        num_bars: number of times to repeat the pattern
        """
        track = pretty_midi.Instrument(program=0, is_drum=True, name='Drums')
        for bar in range(num_bars):
            bar_start = start_time + bar * 4.0
            for time, note, vel in drum_events:
                note_obj = pretty_midi.Note(
                    velocity=vel,
                    pitch=note,
                    start=bar_start + time,
                    end=bar_start + time + step_duration
                )
                track.notes.append(note_obj)
        self.midi.instruments.append(track)

    def save(self, filename):
        self.midi.write(filename)

    def render_to_wav(self, soundfont_path, output_wav_path):
        """
        Render the current MIDI to a WAV file using FluidSynth.
        """
        fd, midi_path = tempfile.mkstemp(suffix='.mid')
        os.close(fd)
        self.save(midi_path)

        cmd = ['fluidsynth', '-F', output_wav_path, '-ni', soundfont_path, midi_path]
        print("Rendering with command:", ' '.join(cmd))

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("stdout:", result.stdout)
            print("stderr:", result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"FluidSynth rendering failed: {e.stderr}")
            raise
        finally:
            os.unlink(midi_path)