"""
End-to-end test: generate lyrics, align syllables, synthesize each syllable with TTS,
stretch to fit timings, and concatenate.
"""

from core.lyrics_generator import LyricsGenerator
from core.alignment import VocalAligner
from core.tts import get_tts_provider
from core.stretcher import stretch_audio
from pydub import AudioSegment

def main():
    # 1. Generate a short verse of lyrics (Markov chain)
    print("Generating lyrics...")
    gen = LyricsGenerator(seed=42)
    lyrics_lines = gen.generate_verse_markov(theme='hard', num_bars=2)
    print("Lyrics lines:")
    for line in lyrics_lines:
        print(f"  {line}")

    # 2. Align syllables to a musical grid (tempo 140 BPM)
    print("\nAligning syllables...")
    aligner = VocalAligner(tempo_bpm=140)
    events = aligner.align_lyrics(lyrics_lines, rest_duration_beats=1.0)

    print(f"Total syllables: {len(events)}")
    for t, syl in events:
        print(f"  {t:.3f}s: {syl}")

    # 3. Initialize TTS provider (use placeholder for now – silent audio)
    tts = get_tts_provider("placeholder")

    # 4. Synthesize and stretch each syllable
    print("\nSynthesizing and stretching syllables...")
    vocal_tracks = []
    # For this test, we stretch each syllable to a fixed duration (e.g., 0.25s)
    # In a real pipeline you'd compute the target duration from the alignment events.
    target_dur_per_syllable = 0.25  # seconds

    for idx, (_, syllable) in enumerate(events):
        # Synthesize the syllable (returns AudioSegment)
        syl_audio = tts.synthesize(syllable, apply_vst=False)

        # Stretch to target duration
        stretched = stretch_audio(syl_audio, target_duration_sec=target_dur_per_syllable)

        # Add to track list
        vocal_tracks.append(stretched)
        print(f"  Processed syllable {idx+1}: '{syllable}'")

    # 5. Concatenate all syllables into one vocal track
    print("\nConcatenating vocal tracks...")
    if vocal_tracks:
        final_vocal = vocal_tracks[0]
        for track in vocal_tracks[1:]:
            final_vocal += track
    else:
        final_vocal = AudioSegment.silent(1000)

    # 6. Save the result
    output_file = "test_vocal_stretched.wav"
    final_vocal.export(output_file, format="wav")
    print(f"\nSaved final vocal track to {output_file}")

if __name__ == "__main__":
    main()