"""
Test the audio stretcher on a simple tone.
"""

from pydub import AudioSegment
from pydub.generators import Sine
from core.stretcher import stretch_audio

def main():
    # Generate a 440 Hz tone of 2 seconds
    tone = Sine(440).to_audio_segment(duration=2000)  # 2000 ms = 2 sec

    # Stretch to 3 seconds
    stretched = stretch_audio(tone, target_duration_sec=3.0)

    # Save both
    tone.export("test_tone_original.wav", format="wav")
    stretched.export("test_tone_stretched.wav", format="wav")
    print("Original duration: {:.2f}s".format(tone.duration_seconds))
    print("Stretched duration: {:.2f}s".format(stretched.duration_seconds))

if __name__ == "__main__":
    main()