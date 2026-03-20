# core/alignment.py

"""
Vocal alignment module: splits lyrics into syllables and assigns timings based on tempo.
"""

import pyphen

class VocalAligner:
    """
    Converts lyrics into timed syllable events for alignment with a beat.
    """

    def __init__(self, tempo_bpm: float = 140, syllable_duration_beats: float = 0.25):
        """
        Args:
            tempo_bpm: Beats per minute.
            syllable_duration_beats: Duration of each syllable in beats (e.g., 0.25 = 16th note).
        """
        self.tempo = tempo_bpm
        self.beat_duration = 60.0 / tempo_bpm  # seconds per quarter note
        self.syllable_duration = self.beat_duration * syllable_duration_beats
        self.dic = pyphen.Pyphen(lang='en_US')  # English hyphenation

    def syllabify_line(self, line: str):
        """
        Split a line of lyrics into a list of syllables.
        """
        words = line.split()
        syllables = []
        for word in words:
            # Pyphen inserts hyphens between syllables
            hyphenated = self.dic.inserted(word).split('-')
            # If hyphenated returns the original word (no hyphens), treat as single syllable
            syllables.extend([s for s in hyphenated if s])
        return syllables

    def align_lyrics(self, lyrics_lines, add_rest_between_lines=True, rest_duration_beats=1.0):
        """
        Convert a list of lyric lines into a list of (start_time, syllable) events.

        Args:
            lyrics_lines: List of strings (each line of lyrics).
            add_rest_between_lines: If True, insert a rest after each line.
            rest_duration_beats: Duration of rest in beats.

        Returns:
            List of (start_time_in_seconds, syllable_text) events.
        """
        events = []
        current_time = 0.0

        for line in lyrics_lines:
            syllables = self.syllabify_line(line)
            for syl in syllables:
                events.append((current_time, syl))
                current_time += self.syllable_duration

            if add_rest_between_lines:
                current_time += rest_duration_beats * self.beat_duration

        return events