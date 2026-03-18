"""
Full Project Verification Script
Checks all components for Phases 1-4: Python libraries, system tools, datasets, and resources.
"""

import os
import subprocess
import sqlite3

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def print_header(text):
    print(f"\n{'-'*60}")
    print(text)
    print('-'*60)

def check_python_import(module_name, package_name=None):
    """Try importing a Python module."""
    try:
        __import__(module_name)
        print(f"{GREEN}✅ {module_name}{RESET}")
        return True
    except ImportError as e:
        pkg = package_name if package_name else module_name
        print(f"{RED}❌ {module_name} – {e}. Install with: pip install {pkg}{RESET}")
        return False

def check_command(cmd, version_flag="--version"):
    """Check if a command-line tool exists."""
    try:
        result = subprocess.run([cmd, version_flag], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            first_line = result.stdout.strip().split('\n')[0]
            print(f"{GREEN}✅ {cmd} – {first_line}{RESET}")
            return True
        else:
            print(f"{RED}❌ {cmd} – command returned error{RESET}")
            return False
    except FileNotFoundError:
        print(f"{RED}❌ {cmd} – not found in PATH{RESET}")
        return False
    except Exception as e:
        print(f"{RED}❌ {cmd} – {e}{RESET}")
        return False

def check_file(path, description):
    """Check if a file exists."""
    if os.path.exists(path):
        print(f"{GREEN}✅ {description}{RESET}")
        return True
    else:
        print(f"{RED}❌ {description} – not found at {path}{RESET}")
        return False

def check_database():
    """Check if the main database exists and has required tables."""
    db_path = os.path.join("data", "beat_lyrics.db")
    if not os.path.exists(db_path):
        print(f"{RED}❌ Database file not found at {db_path}{RESET}")
        return False
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Check for a few key tables
        tables = ["vocabulary", "markov_transitions", "artists", "songs", "lines"]
        missing = []
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not cursor.fetchone():
                missing.append(table)
        conn.close()
        if missing:
            print(f"{YELLOW}⚠️ Database missing tables: {missing}. Run init_lyrics_db.py and import scripts.{RESET}")
            return False
        else:
            print(f"{GREEN}✅ Database exists with all required tables.{RESET}")
            return True
    except Exception as e:
        print(f"{RED}❌ Database check failed: {e}{RESET}")
        return False

def main():
    print("=" * 60)
    print("BEAT & LYRICS GENERATOR – FULL INSTALLATION VERIFICATION")
    print("=" * 60)

    # ----- Python Libraries -----
    print_header("PYTHON LIBRARIES")

    # Phase 1 (Beat Generator)
    check_python_import("music21")
    check_python_import("pretty_midi")
    check_python_import("pygame")

    # Phase 2 (Lyrics Generator)
    check_python_import("vaderSentiment", "vaderSentiment")
    check_python_import("pronouncing")
    check_python_import("textblob")

    # Phase 3 (Voice Synthesis – optional but checked)
    check_python_import("torch")
    check_python_import("torchaudio")
    check_python_import("transformers")
    check_python_import("TTS", "TTS")
    check_python_import("pedalboard")
    check_python_import("librosa")
    check_python_import("soundfile")
    check_python_import("pydub")

    # Common utilities
    check_python_import("numpy")
    check_python_import("scipy")

    # ----- System Tools -----
    print_header("SYSTEM TOOLS")
    check_command("ffmpeg")
    check_command("fluidsynth")

    # ----- Database & Data -----
    print_header("DATABASE & DATASETS")
    check_database()

    # Check for Kaggle datasets (raw CSV files)
    datasets = [
        ("data/raw_lyrics/rap_lyrics/all_lyrics.csv", "Dataset 1 (all_lyrics.csv)"),
        ("data/raw_lyrics/rap_lyrics_text/", "Dataset 2 folder (rap_lyrics_text)"),
        ("data/raw_lyrics/song_lyrics/lyrics_raw.csv", "Dataset 3 (lyrics_raw.csv)"),
    ]
    for path, desc in datasets:
        if os.path.exists(path):
            print(f"{GREEN}✅ {desc}{RESET}")
        else:
            print(f"{YELLOW}⚠️ {desc} not found at {path}. (Optional if you only use database){RESET}")

    # ----- Resources (SoundFont, VSTs, LJ Speech) -----
    print_header("RESOURCES (OPTIONAL)")

    # SoundFont
    sf_path = os.path.join("resources", "SGM-v2.01-Sal-Guit-Bass-V1.3.sf2")
    check_file(sf_path, "SGM SoundFont")

    # VST Plugins
    vst_paths = [
        r"C:\Program Files\Common Files\VST3\TDR Nova.vst3",
        r"C:\Program Files\Common Files\VST3\RoughRider3.vst3"
    ]
    for vst in vst_paths:
        check_file(vst, os.path.basename(vst))

    # LJ Speech Dataset (for voice cloning)
    lj_sample = r"C:\Users\pc\Documents\LJSpeech-1.1\wavs\LJ001-0001.wav"
    if os.path.exists(lj_sample):
        print(f"{GREEN}✅ LJ Speech sample found{RESET}")
    else:
        print(f"{YELLOW}⚠️ LJ Speech sample not found at {lj_sample}. (Only needed for voice cloning){RESET}")

    print("\n" + "=" * 60)
    print("Verification complete.")
    print("Red ❌ indicates missing components that must be installed.")
    print("Yellow ⚠️ indicates optional items (may be needed for certain features).")
    print("If all required items are ✅, your environment is ready.")
    print("=" * 60)

if __name__ == "__main__":
    main()