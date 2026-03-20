"""
Test the vocal aligner with sample lyrics.
"""

from core.alignment import VocalAligner

def main():
    lyrics = [
        "This is a test",
        "Of the aligner",
        "It should work well"
    ]

    aligner = VocalAligner(tempo_bpm=140)  # 140 BPM
    events = aligner.align_lyrics(lyrics)

    print(f"Tempo: {aligner.tempo} BPM")
    print(f"Syllable duration: {aligner.syllable_duration:.3f} seconds\n")
    for time, syl in events:
        print(f"{time:.3f}s: {syl}")

if __name__ == "__main__":
    main()