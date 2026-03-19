# core/tts/__init__.py
"""
TTS module factory - return the appropriate provider.
"""

import logging
from .provider import TTSProvider
from .placeholder import PlaceholderTTSProvider
from .elevenlabs import ElevenLabsTTS
from .config import TTSConfig

logger = logging.getLogger(__name__)

def get_tts_provider(provider_name: str = "placeholder", **kwargs) -> TTSProvider:
    """
    Return a TTS provider instance.

    Args:
        provider_name: 'placeholder' or 'elevenlabs'
        **kwargs: Provider-specific arguments (e.g., api_key for elevenlabs)

    Returns:
        TTSProvider instance.
    """
    if provider_name == "placeholder":
        return PlaceholderTTSProvider(**kwargs)
    elif provider_name == "elevenlabs":
        # Require api_key from kwargs or config
        api_key = kwargs.get("api_key") or TTSConfig.ELEVENLABS_API_KEY
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            raise ValueError("ElevenLabs API key not provided. Set it in .env or pass api_key.")
        return ElevenLabsTTS(api_key=api_key, **kwargs)
    else:
        raise ValueError(f"Unknown TTS provider: {provider_name}")