"""
Test the TTS module with the placeholder provider.
"""

import logging
from core.tts import get_tts_provider

logging.basicConfig(level=logging.INFO)

def main():
    tts = get_tts_provider("placeholder")
    audio = tts.synthesize("This is a test of the placeholder TTS.")
    audio.export("test_placeholder.wav", format="wav")
    print("Placeholder audio saved - it will be silent.")

if __name__ == "__main__":
    main()