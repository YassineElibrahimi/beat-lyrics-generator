# core/midi_exporter.py

"""
Explanation:
The MIDI exporter combines chords, melody, and drums into a single MIDI file and plays it using pygame.

*Content:
add_chords()
add_melody()
add_drums()
save()
play()
"""

# Basically, 'program' selects the instrument sound for that track:
# program=1 refers to Acoustic Grand Piano.
# program=73 → Flute
# program=25 → Acoustic Guitar


import pretty_midi
import pygame
import tempfile
import os






class MIDIExporter:
    def __init__(self, tempo=140):
        self.tempo  = tempo     #BPM
        self.midi   = pretty_midi.PrettyMIDI(initial_tempo=tempo)

    def add_chords(self, chord_progression, start_time=0, program=1):
        """Add a chord track. chord_progression: list of music21 Chord objects."""
        track   = pretty_midi.Instrument(program=program, name='chords')
        time    = start_time

        for chord_obj in chord_progression:
            duration = chord_obj.quarterLength
            for pitch in chord_obj.pitches:
                note = pretty_midi.Note(
                    velocity    =80,
                    pitch       =pitch.midi,
                    start       =time,
                    end         =time + duration
                )
                track.notes.append(note)
            time += duration
        self.midi.instruments.append(track)

    def add_melody(self, melody_stream, start_time=0, program=73):
        """Add a melody track from a music21 Part stream."""
        track   = pretty_midi.Instrument(program=program, name='Melody')
        time    = start_time

        for note_obj in melody_stream.notes:
            duration    = note_obj.quarterLength
            midi_note        = pretty_midi.Note(
                velocity    = 80,
                pitch       = note_obj.pitch.midi,
                start       = time,
                end         = time + duration
            )
            track.notes.append(midi_note)
            time += duration
        self.midi.instruments.append(track)

    def add_drums(self, drum_events, start_time=0, step_duration=0.25):
        """
        Add a drum track (channel 9).
        drum_events : list of (time_in_beats, note, velocity) events
        step_duration: duration of each drum hit in beats (default 16th note = 0.25)
        """
        track = pretty_midi.Instrument(program=0, is_drum=True, name='Drums')
        for time, note, vel in drum_events:
            # Each drum hit is a 16th note duration (0.25 beats) by default.
            note_obj = pretty_midi.Note(
                velocity    = vel,
                pitch       = note,
                start       = start_time + time,
                end         = start_time + time + step_duration
            )
            track.notes.append(note_obj)
        self.midi.instruments.append(track)

    def save(self, filename):
        self.midi.write(filename)

    def play(self, filename=None):
        """Write to a temp file and play using pygame.mixer.music."""
        if filename is None :
            fd, path = tempfile.mkstemp(suffix='.mid')
            os.close(fd)
            self.save(path)
        else:
            path = filename
            self.save(path)

        # Initialize pygame mixer if not already
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except pygame.error as e:
            print(f"Warning: pygame mixer could not initialize: {e}")
            return  # Skip playback if no audio device

        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

        # Wait for playback to finish (optional but I will add it)
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)

        # Clean up temp file
        if filename is None:
            os.unlink(path)







# This Note is 'FOR ME'; NO NEED to READ it.
"""
---
fd, path = tempfile.mkstemp(suffix='.mid')  # fd stands for file descriptor.
---

# What a file descriptor is:
it's just a number that represents the open file.
it handles the os.
it used to reference an open file.
Instead of working with a Python file object.

# For example, mkstemp() returns two things:
1. fd    → the file descriptor (an integer like 3, 4, etc.)
2. path  → the full path to the temporary file that was created

# Why os.close(fd) is used
Right after creating the file:
---
os.close(fd)
---

The code closes the file descriptor because:
• tempfile.mkstemp() creates and opens the file.
• The code only needs the file path, not the open descriptor.
• The program will reopen/write to it later using:
---
self.save(path)
---

# Flow of the code
1. Create temporary file
2. Get (fd, path)
3. Close the low-level file descriptor
4. Use path to save the MIDI file

# Simplified version:
---
fd, path = tempfile.mkstemp(suffix='.mid')  # create temp file
os.close(fd)                                # close descriptor
self.save(path)                             # write to the file
---

# Quick analogy
Think of:
• file descriptor (fd) → ticket number for an open file 🎟️
• path → the address of the file 📁
The code throws away the ticket and just keeps the address.
"""