# core/tts/config.py
"""
TTS configuration - loads API key from environment.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class TTSConfig:
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "YOUR_API_KEY_HERE")
    # You can add other settings like default voice, model, etc.
    DEFAULT_VOICE = "21m00Tcm4TlvDq8ikWAM"
    DEFAULT_MODEL = "eleven_multilingual_v2"