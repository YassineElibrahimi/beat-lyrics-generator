# core/melody_generator.py

"""
Explanation:
This script defines a MelodyGenerator class that creates melodic lines over a chord progression using the 'music21' library.
It focuses on generating musically coherent melodies by combining chord tones and scale tones, while avoiding large leaps and repeated pitches.

Key functionalities include:
- '_chord_tones': extracts MIDI pitches from a chord object.
- '_scale_tones': generates scale pitches (major or minor) around a chord’s root, within one octave, using 'music21' scales or a manual interval fallback.
- '_filter_candidates': limits pitch choices to those within a maximum interval from the previous note to avoid large leaps.
- '_choose_pitch': selects a pitch from candidates, favoring variation over immediate repetition.
- 'generate_melody': creates a 'music21' Stream for a given chord progression and key, assigning a specified number of notes per chord, prioritizing chord tones on strong beats and scale tones as passing tones.

The class allows configurable octave range and optional random seed for reproducible melodies, producing streams ready for playback or MIDI export.
"""

"""
*Content:
MelodyGenerator.__init__()
MelodyGenerator._chord_tones()
MelodyGenerator._scale_tones()
MelodyGenerator._filter_candidates()
MelodyGenerator._choose_pitch()
MelodyGenerator.generate_melody()
"""







from music21 import note, stream, key, scale, pitch
import random





class MelodyGenerator:
    def __init__(self, octave_range=4, seed=None):
        """
        octave_range: the MIDI octave to use (4 = middle C octave).
        seed: optional random seed for reproducibility.
        """
        self.octave = octave_range
        if seed is not None:
            random.seed(seed)

    def _chord_tones(self, chord_obj):
        """Return a list of MIDI pitches for the CHORD tones (sorted)."""
        return sorted([p.midi for p in chord_obj.pitches])

    def _scale_tones(self, key_obj, chord_obj):
        """
        Return a list of MIDI pitches for the SCALE (within one octave of the chord's root).
        Uses music21's scale methods; falls back to interval-based generation if needed
        """
        # Get the chord's root as a pitch; fallback to middle C if no root
        root_midi   = chord_obj.root().midi if chord_obj.root() else 60
        root_pitch  = pitch.Pitch(root_midi)

        # Determine major or minor scale based on key
        if key_obj.mode == 'minor':
            scale_obj = scale.MinorScale(key_obj.tonic)
            intervals = [2, 1, 2, 2, 1, 2, 2]  # natural minor intervals
        else:
            scale_obj = scale.MajorScale(key_obj.tonic)
            intervals = [2, 2, 1, 2, 2, 2, 1]  # major scale intervals

        try:
            # Try music21's getPitches method (some versions may not support maxPitches)
            scale_pitches = scale_obj.getPitches(root_pitch, direction='ascending', maxPitches=8)
            return [p.midi for p in scale_pitches]
        except Exception:
            # Manual fallback: generate scale pitches using intervals
            pitches = [root_midi]
            current = root_midi
            for interval in intervals:
                current += interval
                if current <= root_midi + 12:  # stay within one octave
                    pitches.append(current)
            return pitches

    def _filter_candidates(self, candidates, prev_pitch, max_interval=7):
        """
        Return candidates that are within max_interval (semitones) of prev_pitch.
        If no candidates satisfy, return all candidates.
        """
        if prev_pitch is None or not candidates:
            return candidates

        for interval in range(max_interval, 13, 1):  # expand up to octave to avoid repeated pitches later
            filtered = [p for p in candidates if abs(p - prev_pitch) <= interval]
            if filtered:
                return filtered
        return candidates           # fallback (should not happen)

    def _choose_pitch(self, candidates, prev_pitch):
        """Choose a pitch from candidates, trying to avoid repeating the previous pitch."""
        if not candidates:
            return None

        if prev_pitch is None or len(candidates) == 1:
            return random.choice(candidates)

        # 70% chance to avoid immediate repeat if possible
        if prev_pitch in candidates and len(candidates) > 1 and random.random() < 0.7:
            others = [p for p in candidates if p != prev_pitch]
            return random.choice(others)

        return random.choice(candidates)

    def generate_melody(self, chord_progression, key_name='C', durations_per_chord=4):
        """
        1. Generate a melody as a music21 Stream.
        2. chord_progression: list of music21 Chord objects (or RomanNumeral objects).
        3. key_name: string, (e.g., 'C', 'Am').
        4. durations_per_chord: how many notes to generate per chord (e.g., 4 = quarter notes).
        """
        key_obj         = key.Key(key_name)
        melody_stream   = stream.Part()
        melody_stream.append(key_obj)   # Optional, but I add it for context

        prev_pitch = None               # track last note for leap avoidance ('prev_pitch' stands for 'previous pitch')

        for chord_obj in chord_progression:
            chord_duration  = chord_obj.quarterLength
            note_duration   = chord_duration / durations_per_chord
            chord_tones     = self._chord_tones(chord_obj)
            scale_tones     = self._scale_tones(key_obj, chord_obj)

            # Generate notes for this chord
            for i in range(durations_per_chord):
                # On the first beat (i==0), always pick a chord tone for stability.
                # Otherwise, 70% chord tone, 30% passing tone.
                if i == 0 or random.random() < 0.7:
                    candidates = chord_tones
                else:
                    # Passing tone: scale tone not in chord
                    passing_options = [p for p in scale_tones if p not in chord_tones]
                    candidates = passing_options if passing_options else chord_tones

                # Avoid large leaps: filter candidates based on previous pitch
                candidates = self._filter_candidates(candidates, prev_pitch)

                # Choose pitch with repeat avoidance
                chosen_pitch = self._choose_pitch(candidates, prev_pitch)
                if chosen_pitch is None:
                    chosen_pitch = random.choice(chord_tones)  # ultimate fallback

                # Create note object
                n = note.Note(chosen_pitch)    # 'n' stands for 'note' 
                n.duration.quarterLength = note_duration
                melody_stream.append(n)

                prev_pitch = chosen_pitch      # update for next note

        return melody_stream