# core/tts/placeholder.py
"""
Placeholder TTS provider - logs the call and generates a silent audio file.
Useful for testing the pipeline before integrating a real API.
"""

import logging
import numpy as np
from pydub import AudioSegment
from .provider import TTSProvider

logger = logging.getLogger(__name__)

class PlaceholderTTSProvider(TTSProvider):
    """Dummy TTS provider that logs and returns silent audio."""

    def __init__(self, duration_sec: float = 2.0, sample_rate: int = 24000):
        self.duration_sec = duration_sec
        self.sample_rate = sample_rate

    def synthesize(
        self,
        text: str,
        voice_id: str = None,
        output_path: str = None,
        **kwargs
    ) -> AudioSegment:
        logger.info(f"PlaceholderTTS: would synthesize '{text[:50]}...' with voice {voice_id}")

        # Generate silent audio
        samples = np.zeros(int(self.duration_sec * self.sample_rate), dtype=np.float32)
        audio = AudioSegment(
            data=samples.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=4,          # float32
            channels=1
        )

        if output_path:
            audio.export(output_path, format="wav")
            logger.info(f"Saved silent placeholder audio to {output_path}")

        return audio