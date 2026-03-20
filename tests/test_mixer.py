"""
Test the mixer by mixing a vocal track with a generated beat.
"""

from core.mixer import mix_tracks
from pydub import AudioSegment
from pydub.generators import Sine

def main():
    # Create a simple beat (just a sine wave for testing)
    beat = Sine(60).to_audio_segment(duration=5000)  # 5 seconds
    beat.export("test_beat.wav", format="wav")

    # Use the previously generated vocal file (from pipeline)
    try:
        mix_tracks("test_vocal_stretched.wav", "test_beat.wav", "test_mixed.wav")
        print("Mixed track saved as test_mixed.wav")
    except FileNotFoundError:
        print("Please run test_full_vocal_pipeline.py first to generate vocal file.")

if __name__ == "__main__":
    main()