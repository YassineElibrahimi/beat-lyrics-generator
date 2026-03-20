"""
Audio stretching module using librosa.
Stretches audio to a target duration without affecting pitch.
"""

import numpy as np
import librosa
from pydub import AudioSegment

def stretch_audio(audio: AudioSegment, target_duration_sec: float) -> AudioSegment:
    """
    Stretch an audio segment to exactly target_duration_seconds.
    Preserves pitch using the phase vocoder algorithm from librosa.

    Args:
        audio: AudioSegment to stretch.
        target_duration_sec: Desired duration in seconds.

    Returns:
        Stretched AudioSegment.
    """
    current_duration_sec = audio.duration_seconds
    if abs(current_duration_sec - target_duration_sec) < 0.01:
        return audio

    # Convert to numpy array (float32, mono)
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
    if audio.channels == 2:
        # Mix down to mono by averaging
        samples = samples.reshape((-1, 2)).mean(axis=1)
    # Normalize to [-1, 1]
    samples = samples / (2**(8 * audio.sample_width - 1))

    # Compute stretch ratio
    ratio = target_duration_sec / current_duration_sec
    # librosa's time_stretch uses a rate parameter: rate > 1 speeds up, rate < 1 slows down.
    # To achieve a longer duration, we need rate < 1, so rate = 1/ratio.
    stretch_rate = 1.0 / ratio

    # Stretch using librosa
    stretched = librosa.effects.time_stretch(y=samples, rate=stretch_rate)

    # Convert back to AudioSegment (int16)
    stretched_int16 = np.clip(stretched * 32767, -32768, 32767).astype(np.int16)
    stretched_audio = AudioSegment(
        data=stretched_int16.tobytes(),
        frame_rate=audio.frame_rate,
        sample_width=2,
        channels=1
    )
    return stretched_audio