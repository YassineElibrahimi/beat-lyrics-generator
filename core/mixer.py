# core/mixer.py

"""
Audio mixing module – combines vocal and beat tracks with optional level adjustments.
"""

from pydub import AudioSegment

def mix_tracks(vocal_path: str, beat_path: str, output_path: str,
               vocal_gain_db: float = 0.0, beat_gain_db: float = -6.0) -> None:
    """
    Mix a vocal track with a beat and export the result.

    Args:
        vocal_path: Path to vocal WAV file.
        beat_path: Path to beat WAV file.
        output_path: Path for the mixed output file.
        vocal_gain_db: Gain adjustment for vocals in dB.
        beat_gain_db: Gain adjustment for beat in dB.
    """
    vocal = AudioSegment.from_file(vocal_path)
    beat = AudioSegment.from_file(beat_path)

    # Adjust volumes
    vocal = vocal + vocal_gain_db
    beat = beat + beat_gain_db

    # Ensure same length (pad or trim as needed)
    if len(vocal) > len(beat):
        beat = beat + AudioSegment.silent(duration=len(vocal) - len(beat))
    elif len(beat) > len(vocal):
        vocal = vocal + AudioSegment.silent(duration=len(beat) - len(vocal))

    # Overlay vocals on beat
    mixed = beat.overlay(vocal)
    mixed.export(output_path, format="wav")