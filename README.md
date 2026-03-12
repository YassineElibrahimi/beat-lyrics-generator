# Beat & Lyrics Generator

Python application that generates beats and lyrics with an interactive, editable workflow. Built with:
**PySide6 + QML** for a modern GUI.
**music21** for music theory.
**SQLite** for data storage.
And various NLP tools for lyrics generation.
Currently focused on an English/US Hip‑hop MVP (Moroccan Arabic 'Darija' support planned later).
The project follows a checkpoint‑based development – see the roadmap below.
Perfect for music producers, rappers, or anyone exploring algorithmic music creation.

---

## Overview

Beat & Lyrics Generator lets you:
- **Generate a beat** – choose genre, theme, instrument, key, and tempo, and get a complete beat with chords, melody, and drums.
- **Generate a full track** *(planned)*  – automatically produce a beat, lyrics, and vocals together.
- **Edit everything** – after generation, you can regenerate any component individually: chord progression, lead melody, drum patterns (kick, snare, hi‑hat separately), lyrics structure, and voice.
- **Save/load projects** – all generated data is stored in a local SQLite database for later retrieval.

The GUI is currently under construction; we use a **command‑line interface (CLI)** to test and validate the core modules. Once the backend is polished, the GUI will be re‑integrated.

This project started as an ambitious blueprint and has been refined into a realistic, phased development plan. I'm  currently focusing on an **English/US Hip‑hop MVP**, with plans to later add support for Moroccan Arabic (Darija) and more advanced voice synthesis.

---

## Features (MVP) *(Planned & Current)*

- **Beat Generator**  
  - Select genre (trap, drill, old school), theme (hard, melancholic, aggressive, smooth), lead instrument, key, and tempo.  
  - Chord progressions based on Roman numeral templates (loaded from SQLite).  
  - Rule‑based melody generation using chord tones and scale passing notes.  
  - Probabilistic drum patterns per genre (kick, snare, hi‑hat, open hat) with independent regeneration.  
  - Export to MIDI and playback via system synthesizer.

- **Lyrics Generator (English)**  
  - Fetch lyrics from Genius API (with caching) or use a pre‑collected corpus.  
  - Extract theme‑based vocabulary using sentiment analysis (VADER/TextBlob).  
  - Generate rhyming lines (AABB scheme) with `pronouncing` library.  
  - Customizable structure: number of bars (8/16/32/64), toggle hook, add intro/outro ad‑libs.

- **Voice Synthesis (Simplified)**  
  - Text‑to‑speech using gTTS (or optionally Amazon Polly) for English vocals.  
  - Syllable‑to‑beat alignment: syllabify lyrics, map to 16th‑note grid, time‑stretch audio to fit.  
  - Mix vocals with beat (rendered via FluidSynth) and play the full track.

- **Full Track Mode**  
  - Randomly selects genre and theme, then generates beat, lyrics, and vocals together.  
  - Displays all components with dedicated edit buttons.

- **Project Persistence**  
  - All user projects and generated content saved in SQLite.  
  - Load previous projects to continue editing.

---

## Technology Stack *(Planned & Current)*

| Component                | Library/Tool                          | Status |
|--------------------------|---------------------------------------|--------|
| Music theory & MIDI      | music21, pretty_midi                  | ✅     |
| Drum patterns            | Custom probabilistic grids             | ✅     |
| Audio playback (current) | pygame                                 | ⚠️ (will be replaced) |
| High‑quality audio       | FluidSynth + custom SoundFonts         | ⬜ (planned) |
| Lyrics acquisition       | lyricsgenius (Genius API)              | ⬜ (Phase 2) |
| Sentiment analysis       | vaderSentiment / textblob              | ⬜ (Phase 2) |
| Rhyme & syllables        | pronouncing, pyphen                    | ⬜ (Phase 2) |
| Text‑to‑Speech           | gTTS / Amazon Polly                     | ⬜ (Phase 3) |
| GUI                      | PySide6 + QML (paused)                  | ⬜ (will resume after core is solid) |
| Database                 | SQLite3                                | ✅     |


---

## Usage (Current CLI)

Run the beat generator from the command line:

```bash
python cli.py
```

You will be prompted to enter:
- **Genre**: trap / drill / old_school
- **Theme**: hard / melancholic / aggressive / smooth
- **Key**: e.g., C, Dm, etc.
- **Tempo**: BPM (default 140)

The program then:
- Generates chords, melody, and drums.
- Saves a MIDI file (e.g., `beat_trap_hard_C_140.mid`).
- Plays the MIDI using pygame (temporary; audio quality will improve).

---

## Project Structure *(Planned & Current)*

```
beat-lyrics-generator/
├── main.py                      # Application entry point
├── core/                         # Core logic modules
│   ├── beat_generator.py         # Beat generation (chords, melody, drums)
│   ├── lyrics_generator.py       # Lyrics generation and structure
│   ├── voice_synthesizer.py      # TTS, alignment, mixing
│   └── midi_exporter.py          # MIDI creation and playback
├── gui/                           # GUI related code
│   ├── main_window.py             # Main window setup (PySide6)
│   ├── qml/                       # QML UI components
│   │   ├── BeatEditor.qml
│   │   ├── FullTrackView.qml
│   │   └── ...
│   └── controllers/               # Controllers to connect UI and core
│       ├── beat_controller.py
│       ├── lyrics_controller.py
│       └── ...
├── data/                           # Data management
│   ├── database.py                 # SQLite connection and queries
│   ├── models.py                   # Python data classes (Project, Beat, etc.)
│   └── templates/                   # JSON seed files
│       ├── chord_progressions.json
│       ├── drum_patterns.json
│       └── instruments.json
├── scripts/                         # Utility scripts
│   ├── init_db.py                   # Create tables and seed data
│   ├── fetch_lyrics.py              # Genius API lyric fetcher
│   └── export_midi.py               # Example MIDI export
├── resources/                        # SoundFonts, icons, etc.
│   └── default_soundfont.sf2
├── tests/                             # Unit tests
│   ├── test_beat_generator.py
│   ├── test_lyrics_generator.py
│   └── ...
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
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
| 6 | MIDI export and playback (pygame)  |✅ *(audio quality to be improved)* | ✅ |
| 7 | GUI (PySide6 + QML) – **paused**, replaced with CLI for testing | ⬜/✅ |
| 7b | **Bug fixes and validation of Phase 1** ||⬜|
| **2: Lyrics Generator** |
| 8 | Lyrics database tables, Genius API client with caching || ⬜ |
| 9 | Vocabulary extraction and sentiment tagging  || ⬜ |
| 10 | Rhyme‑aware line generator (AABB) using pronouncing || ⬜ |
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
- [FluidSynth](http://www.fluidsynth.org/) *(planned)*
- All open‑source contributors

---

**Note:** The GUI is temporarily on hold to focus on core functionality and audio quality. The CLI ensures we can test and use the generator while the UI matures.

**Note**: This project uses the Genius API to fetch lyrics. Please respect their [terms of service](https://genius.com/static/terms) and rate limits (free tier ~50 requests/day). For larger usage, consider caching results or using alternative lyric datasets.

**PS**: If I find a free, legal way to get data, I will mention it and use it later (like on Kaggle or other open-source platforms), or maybe I will make my own, but that will take some time. To be honest, don’t rely on that, because I have to respect the artist’s work and effort.

---

*Happy beat making!* 🎵