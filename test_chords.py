# tests/test_chords.py


from core.chord_generator import ChordGenerator






def main():
    gen = ChordGenerator()
    try:
        chords = gen.generate(genre='trap', theme='hard', key='C')
        print("Generated chord progression:")
        for i, c in enumerate(chords):
            print(f"  Chord {i+1}: {c.pitchedCommonName} ({c})")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()