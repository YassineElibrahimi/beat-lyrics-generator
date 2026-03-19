# core/tts/elevenlabs.py
"""
ElevenLabs TTS provider - makes actual API requests.
Handles errors like invalid key, out of credits, rate limits, etc.
"""

from typing import Optional
import io
import requests
import logging
from pydub import AudioSegment
from .provider import TTSProvider

logger = logging.getLogger(__name__)

class ElevenLabsTTS(TTSProvider):
    """TTS provider using ElevenLabs API."""

    # Default voice ID (Rachel – you can change later)
    DEFAULT_VOICE = "21m00Tcm4TlvDq8ikWAM"

    def __init__(self, api_key: str, base_url: str = "https://api.elevenlabs.io/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        })

    def synthesize(
        self,
        text: str,
        voice_id: Optional[str] = None,
        output_path: Optional[str] = None,
        model_id: str = "eleven_multilingual_v2",
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        **kwargs
    ) -> AudioSegment:
        """
        Synthesize speech via ElevenLabs API.

        Args:
            text: The text to speak.
            voice_id: ElevenLabs voice ID (defaults to Rachel).
            output_path: If given, save audio to this file.
            model_id: ElevenLabs model.
            stability, similarity_boost: Voice settings.
            **kwargs: Additional parameters (e.g., style, speaker_boost).

        Returns:
            AudioSegment of the generated speech.
        """
        if voice_id is None:
            voice_id = self.DEFAULT_VOICE

        url = f"{self.base_url}/text-to-speech/{voice_id}"

        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
            }
        }
        # Add any extra parameters from kwargs
        payload.update(kwargs)

        logger.info(f"ElevenLabs: synthesizing {len(text)} chars with voice {voice_id}")

        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()  # Raise exception for 4xx/5xx
        except requests.exceptions.HTTPError as e:
            self._handle_http_error(e, response)
            raise  # Re-raise after handling (or you could return fallback)
        except requests.exceptions.RequestException as e:
            logger.error(f"ElevenLabs network error: {e}")
            raise

        # Success – response.content is the audio (MP3 format)
        audio_data = response.content

        # Convert to AudioSegment (ElevenLabs returns MP3)
        try:
            audio = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
        except Exception as e:
            logger.error(f"Failed to decode audio: {e}")
            raise

        if output_path:
            audio.export(output_path, format="wav")
            logger.info(f"Saved audio to {output_path}")

        return audio

    def _handle_http_error(self, e, response):
        """Parse ElevenLabs error responses."""
        status = response.status_code
        try:
            error_json = response.json()
            error_message = error_json.get("detail", {}).get("message", str(e))
        except:
            error_message = response.text or str(e)

        if status == 401:
            logger.error("ElevenLabs: Invalid API key")
        elif status == 402:
            logger.error("ElevenLabs: Out of credits (402)")
        elif status == 429:
            logger.error("ElevenLabs: Rate limit exceeded (429)")
        elif status == 422:
            logger.error(f"ElevenLabs: Invalid parameters: {error_message}")
        else:
            logger.error(f"ElevenLabs HTTP {status}: {error_message}")