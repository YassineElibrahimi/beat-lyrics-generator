# Beat & Lyrics Generator

Python application that generates beats and lyrics with an interactive, editable workflow.  
- Currently focused on an **English/US Hip‑hop MVP** (Moroccan Arabic 'Darija' support planned later).  
*Perfect for music producers, rappers, or anyone exploring algorithmic music creation.*

---

## Overview

#### **For beat generation:**  
**Think of the code as a car – it's fully built and ready to run.** 
The SoundFonts are like gasoline; without them, the engine still runs (using a pygame fallback), but with the right fuel, it will roar with professional audio quality.  

**For lyrics generation & voice generation:**  
Like beat generation, The same concept applies – build the engine first, add the fuel (data) later.

#### Beat & Lyrics Generator lets you:
- **Generate a beat** – choose genre, theme, instrument, key, and tempo, and get a complete beat with chords, melody, and drums.
- **Generate a full track** *(planned)* – automatically produce a beat, lyrics, and vocals together.
- **Edit everything** – after generation, you can regenerate any component individually: chord progression, lead melody, drum patterns (kick, snare, hi‑hat separately), lyrics structure, and voice.
- **Save/load projects** – all generated data is stored in a local SQLite database for later retrieval.

The GUI is currently under construction; we use a **command‑line interface (CLI)** to test and validate the core modules. Once the backend is polished, the GUI will be re‑integrated.

This project started as an ambitious blueprint and has been refined into a realistic, phased development plan. I'm currently focusing on an **English/US Hip‑hop MVP**, with plans to later add support for Moroccan Arabic (Darija) and more advanced voice synthesis.

---

## Current Features (Phase 1 & 2 Completed)

### Beat Generator
- **Chord progression generator** – Roman numeral templates per genre & theme (trap, drill, old‑school). Uses `music21` to convert numerals to actual notes in any key.
- **Melody generator** – Rule‑based: chord tones on strong beats, scale tones as passing notes. Avoids large leaps and pitch repetitions.
- **Drum pattern generator** – Probabilistic 16‑step patterns per genre (kick, snare, hi‑hat, open hat) with independent regeneration.
- **MIDI export & playback** – Combines all tracks into a single MIDI file. Two playback modes:
  - **Pygame fallback** (low quality, works out‑of‑the‑box).
  - **FluidSynth + SoundFont** (professional quality) – code ready; you provide the SoundFont ("gasoline").

### Lyrics Generator
- **Lyrics acquisition** – Three curated Kaggle hip‑hop datasets (no API limits, fully offline).
- **Vocabulary extraction** – Theme‑based word frequency tables.
- **Theme assignment** – Combined VADER sentiment + keyword scoring to classify lines into 8 themes (hard, melancholic, reflective, smooth, confident, inspirational, playful, street love).
- **Markov chain generation** – Bigram model with weighted sampling produces coherent, theme‑aligned lyrics with rhyme support.

---


## Technology Stack *(Planned & Current)*

| Component                | Library/Tool                          | Status |
|--------------------------|---------------------------------------|--------|
| Music theory & MIDI      | music21, pretty_midi                  | ✅     |
| Drum patterns            | Custom probabilistic grids             | ✅     |
| Audio playback (fallback)| pygame                                 | ✅     |
| High‑quality audio       | FluidSynth + custom SoundFonts         | ✅ (code ready; requires external SoundFont) |
| Lyrics acquisition       | Kaggle datasets (no API)              | ✅  |
| Vocabulary extraction      | Custom regex + frequency counting              | ✅ |
| Rhyme & generation      | pronouncing, custom Markov-inspired              | ✅ |
| Sentiment analysis/Theme assignment       | VADER sentiment + keyword matching              | ✅ |
| Text‑to‑Speech           | gTTS / Amazon Polly                     | ⬜ (Phase 3) |
| GUI                      | PySide6 + QML (paused)                  | ⬜ (will resume after core is solid) |
| Database                 | SQLite3                                | ✅     |

---

## Audio Setup (Getting the "Gasoline")

To enjoy professional audio quality, you need:

1. **Install FluidSynth**  
   - Windows: Download from [fluidsynth.org](http://www.fluidsynth.org/)  
   - Linux: `sudo apt install fluidsynth`  
   - macOS: `brew install fluidsynth`

2. **Download a SoundFont** (`.sf2` file)  
   Recommended free SoundFonts for hip‑hop:
   - **SGM‑V2.01** – [Internet Archive](https://archive.org/details/sgm-v2.01-soundfont)  
   - **FluidR3 GM** – [MuseScore](https://musescore.org/en/handbook/soundfonts-and-sfz-files#fluid-soundfont)

3. **Place the SoundFont** in the `resources/` folder and rename it to `default_soundfont.sf2` (or modify the path in `cli.py`).

Once the SoundFont is present, the CLI will automatically use FluidSynth for playback. If not, it falls back to pygame (lower quality).


---

## Usage (Current CLI)

### Beat Generation :

Run the beat generator from the command line:

```bash
python cli.py
```

Follow the prompts to enter genre, theme, key, and tempo. The program will generate a MIDI file and play it.  

You will be prompted to enter:
- **Genre**: trap / drill / old_school
- **Theme**: hard / melancholic / aggressive / smooth
- **Key**: e.g., C, D, etc.
- **Tempo**: BPM (default 140)

The program then:
- Generates chords, melody, and drums.
- Saves a MIDI file (e.g., `beat_trap_hard_C_140.mid`).
- Plays the MIDI using the best available audio method (FluidSynth if SoundFont found, otherwise pygame).

### Lyrics Generation (test mode) :

Run the lyrics generator from the command line:

```bash
python -m tests.test_markov_lyrics
```

This will output sample lyrics for different themes using the Markov generator.

---

## Project Structure *(Planned & Current)*

```
beat-lyrics-generator/
├── core/                             # Core logic modules
│   ├── __init__.py
│   ├── chord_generator.py
│   ├── drum_generator.py
│   ├── lyrics_generator.py
│   ├── melody_generator.py
│   └── midi_exporter.py              # MIDI creation and playback
│
├── gui/                              # GUI related code
│   ├── main_window.py                # Main window setup (PySide6)
│   ├── qml/                          # QML UI components
│   │   ├── BeatEditor.qml
│   │   ├── FullTrackView.qml
│   │   └── ...
│   └── controllers/                  # Controllers to connect UI and core
│       ├── beat_controller.py
│       ├── lyrics_controller.py
│       └── ...
│
├── data/                             # Database and data files mangement
│   ├── raw_lyrics/                   # Kaggle datasets
│   │   ├── rap_lyrics
│   │   │   └── all_lyrics.csv
│   │   ├── rap_lyrics_text
│   │   │   └── 38 text file
│   │   └── song_lyrics
│   │       └── lyrics_raw.csv
│   ├── templates/                    # JSON seed files
│   │   ├── chord_progressions.json
│   │   ├── drum_patterns.json
│   │   └── instruments.json
│   ├── __init__.py
│   ├── beat_lyrics.db                # SQLite database
│   ├── database.py                   # SQLite connection and queries
│   ├── models.py
│   ├── stopwords.txt                 # Stopwords (I didn't use it yet)
│   └── theme_config.json             # theme config (hard, street love, etc.)
│
├── Notes/                            # NO NEED TO READ (Just a bunch of notes)
│
├── resources/                        # SoundFonts, icons, etc.
│   ├── lyrics_datasets_resources
│   └── README.md                     # Instructions for obtaining SoundFonts
│
├── scripts/                          # Utility scripts
│   ├── assign_themes.py
│   ├── build_markov.py
│   ├── build_vocabulary.py
│   └── import_all_lyrics.py
│
├── tests/                            # Unit tests
│   ├── __init__.py
│   ├── test_chords.py
│   ├── test_drums.py
│   ├── test_lyrics.py
│   ├── test_markov_lyrics.py
│   ├── test_melody.py
│   └── test_midi.py
│   
├── .env.example
├── .gitignore
├── cli.py                            # Command‑line beat generator
├── init_db.py
├── init_lyrics_db.py
├── main.py                           # (placeholder for future GUI)
├── requirements.txt                  # Python dependencies
├── run_test.py                       # Run the (Unit tests)
└── README.md                         # This file
```

---

## Development Status & Roadmap

This project follows a **checkpoint‑based development plan**. Each checkpoint is a self‑contained feature. Below is the current progress (✅ = completed, ⬜ = pending).

| Phase | Checkpoint | Description | Status |
|-------|------------|------------|--------|
| **1: Beat Generator** |
| 1 | Project setup, virtual environment, basic PySide6 window with two buttons || ✅ |
| 2 | SQLite database setup, tables for genres, themes, instruments, chord progressions, drum patterns; seed from JSON || ✅ |
| 3 | Chord progression engine using music21 (Roman numeral → notes) || ✅ |
| 4 | Rule‑based melody generator (chord tones + passing notes) || ✅ |
| 5 | Probabilistic drum pattern generator per genre || ✅ |
| 6 | MIDI export and playback (pygame + FluidSynth ready)   |*(high‑quality audio code ready, requires SoundFont)*| ✅ |
| 7 | GUI (PySide6 + QML)|  – **paused**, replaced with CLI for testing | ⬜/✅ |
| 7b | **Bug fixes and validation of Phase 1** || ✅ |
| **2: Lyrics Generator** |
| 8 | Import Kaggle lyrics datasets, build vocabulary, generate rhyming lines || ✅ |
| 9 | Vocabulary refinement (sentiment analysis/theme assignment)  || ✅ |
| 10 | Markov chain bigram model for improved line generation || ✅ |
| 11 | Lyrics structure UI (bars, hook, intro/outro, etc.) || ⬜ |
| 12 | Theme matching between beat and lyrics || ⬜ |
| **3: Voice Synthesis** |
| 13 | TTS integration (gTTS) with male/female toggle || ⬜ |
| 14 | Syllabification and beat alignment || ⬜ |
| 15 | Time‑stretching audio to fit beat durations || ⬜ |
| 16 | Mixing beat and vocals, full track playback || ⬜ |
| **4: Full Track & Polish** |
| 17 | Random full track generation || ⬜ |
| 18 | Save/load project functionality || ⬜ |
| 19 | UI/UX improvements (progress bars, better layout) || ⬜ |
| 20 | Testing, documentation, final polish || ⬜ |

---

## Acknowledgements

- [music21](http://web.mit.edu/music21/)
- [pretty_midi](https://github.com/craffel/pretty-midi)
- [FluidSynth](http://www.fluidsynth.org/)
- [VADER Sentiment](https://github.com/cjhutto/vaderSentiment)
- [pronouncing](https://github.com/aparrish/pronouncingpy)
- All open‑source contributors and Kaggle dataset providers

---

**Note:** The GUI is temporarily on hold to focus on core functionality and audio quality. The CLI ensures we can test and use the generator while the UI matures.

**Note**: This project will uses the Genius API to fetch lyrics. Please respect their [terms of service](https://genius.com/static/terms) and rate limits (free tier ~50 requests/day). For larger usage, consider caching results or using alternative lyric datasets.

**PS**: If I find a free, legal way to get data, I will mention it and use it later (like on Kaggle or other open-source platforms), or maybe I will make my own, but that will take some time. To be honest, don’t rely on that, because I have to respect the artist’s work and effort. (Update: I have Done it ✅ *read below*)

**Lyrics Data:** Instead of relying on live APIs, I've integrated three curated Kaggle hip-hop lyric datasets. The data is included in the repository, so you can generate lyrics offline with zero API limits. All preprocessing and vocabulary extraction are handled by the included scripts.
(you will find the datasets info with providers name in *'resources/lyrics_datasets_resources'*)

---

*Happy beat making!* 🎵