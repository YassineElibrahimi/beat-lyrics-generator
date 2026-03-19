# core/tts/provider.py
"""
Abstract base class for any TTS provider.
All providers must implement the synthesize method.
"""

from abc import ABC, abstractmethod
from typing import Optional
from pydub import AudioSegment

class TTSProvider(ABC):
    """All TTS providers must implement synthesize()."""

    @abstractmethod
    def synthesize(
        self,
        text: str,
        voice_id: Optional[str] = None,
        output_path: Optional[str] = None,
        **kwargs
    ) -> AudioSegment:
        """
        Convert text to speech and return an AudioSegment.

        Args:
            text: The text to speak.
            voice_id: Optional voice identifier.
            output_path: If given, save the audio to this file.
            **kwargs: Provider-specific parameters (e.g., stability, emotion).

        Returns:
            AudioSegment containing the synthesized speech.
        """
        pass