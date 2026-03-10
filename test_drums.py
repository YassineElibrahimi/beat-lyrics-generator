from core.drum_generator import DrumGenerator

def main():
    # Create generator
    drum_gen = DrumGenerator(seed=42)  # fixed seed for reproducibility

    # Test generating all patterns for trap
    print("=== Trap Drums ===")
    patterns = drum_gen.generate_pattern('trap')
    for instrument, events in patterns.items():
        print(f"{instrument}: {[e[0] for e in events]}")  # show step indices

    # Test regenerating only kick
    print("\n=== Regenerate Kick ===")
    new_patterns = drum_gen.regenerate_kick('trap')
    for instrument, events in new_patterns.items():
        print(f"{instrument}: {[e[0] for e in events]}")

    # Test get_all_events
    print("\n=== All Events (flat) ===")
    all_events = drum_gen.get_all_events('drill')
    for time, note, vel in all_events[:8]:  # show first 8
        print(f"Time: {time:.2f}, Note: {note}, Vel: {vel}")

if __name__ == '__main__':
    main()