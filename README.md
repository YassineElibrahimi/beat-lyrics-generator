# Beat & Lyrics Generator

Python application that generates beats and lyrics with an interactive, editable workflow. Built with **PySide6 + QML** for a modern GUI, **music21** for music theory, and various NLP tools for lyrics generation.
Perfect for music producers, rappers, or anyone exploring algorithmic music creation.

---

## Overview

Beat & Lyrics Generator lets you:
- **Generate a beat** – choose genre, theme, instrument, key, and tempo, then create a complete beat with chords, melody, and drums.
- **Generate a full track** – let the app randomly select a genre and theme, then automatically produce a beat, lyrics, and vocal track.
- **Edit everything** – after generation, you can regenerate any component individually: chord progression, lead melody, drum patterns (kick, snare, hi‑hat separately), lyrics structure, and voice.
- **Save/load projects** – all generated data is stored in a local SQLite database for later retrieval.

This project started as an ambitious blueprint and has been refined into a realistic, phased development plan. I'm  currently focusing on an **English/US Hip‑hop MVP**, with plans to later add support for Moroccan Arabic (Darija) and more advanced voice synthesis.

---

## Features (MVP)

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

## Technology Stack

| Component                | Library/Tool                          |
|--------------------------|---------------------------------------|
| GUI                      | PySide6 + QML                         |
| Music theory & MIDI      | music21, pretty_midi                  |
| Drum patterns            | Custom probabilistic grids             |
| Audio playback           | pygame (MIDI), FluidSynth (rendering)  |
| Audio editing/mixing     | pydub, librosa, audiostretchy         |
| Lyrics acquisition       | lyricsgenius (Genius API)              |
| Sentiment analysis       | vaderSentiment / textblob              |
| Rhyme & syllables        | pronouncing, pyphen                    |
| Text‑to‑Speech           | gTTS (or Amazon Polly)                 |
| Database                 | SQLite3                                |

## Usage

Run the application:
```bash
python main.py
```

### Main Window
- **GENERATE BEAT** – Opens the beat editor where you can customize parameters and generate a beat.
- **GENERATE FULL TRACK** – Randomly picks genre and theme, then generates a complete track (beat + lyrics + vocals).

### Beat Editor
- Dropdowns for genre, theme, lead instrument, key, and tempo slider.
- Click **Generate** to create the beat.
- After generation, three panels appear: **Chords**, **Melody**, **Drums**. Each has a **Regenerate** button to re‑roll that component individually.
- A **Play** button lets you hear the current beat.

### Full Track View
- Displays the beat, lyrics, and vocals side‑by‑side.
- Lyrics section: choose bars, toggle hook, add intro/outro, and regenerate lyrics.
- Voice section: toggle male/female, regenerate vocal alignment.
- **Play Full Track** mixes everything and plays it.

### Saving & Loading
- Use **File → Save Project** to store the current track in the database.
- **File → Load Project** opens a list of previously saved projects.

---

## Project Structure

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

| Phase | Checkpoint | Status |
|-------|------------|--------|
| **1: Beat Generator** |
| 1 | Project setup, virtual environment, basic PySide6 window with two buttons | ✅ |
| 2 | SQLite database setup, tables for genres, themes, instruments, chord progressions, drum patterns; seed from JSON | ✅ |
| 3 | Chord progression engine using music21 (Roman numeral → notes) | ✅ |
| 4 | Rule‑based melody generator (chord tones + passing notes) | ✅ |
| 5 | Probabilistic drum pattern generator per genre | ⬜ |
| 6 | MIDI export and playback (pygame or FluidSynth) | ⬜ |
| 7 | Beat editor UI with regenerate buttons for each track | ⬜ |
| **2: Lyrics Generator** |
| 8 | Lyrics database tables, Genius API client with caching | ⬜ |
| 9 | Vocabulary extraction and sentiment tagging of lines | ⬜ |
| 10 | Rhyme‑aware line generator (AABB) using pronouncing | ⬜ |
| 11 | Lyrics structure UI (bars, hook, intro/outro) | ⬜ |
| 12 | Theme matching between beat and lyrics | ⬜ |
| **3: Voice Synthesis** |
| 13 | TTS integration (gTTS) with male/female toggle | ⬜ |
| 14 | Syllabification (pyphen) and beat grid mapping | ⬜ |
| 15 | Time‑stretching audio to fit beat durations | ⬜ |
| 16 | Mixing beat and vocals, full track playback | ⬜ |
| **4: Full Track & Polish** |
| 17 | Random full track generation | ⬜ |
| 18 | Save/load project functionality | ⬜ |
| 19 | UI/UX improvements (progress bars, better layout) | ⬜ |
| 20 | Testing, documentation, final polish | ⬜ |

---

## Acknowledgements

- [music21](http://web.mit.edu/music21/) – Toolkit for computer‑aided musicology.
- [lyricsgenius](https://github.com/johnwmillr/LyricsGenius) – Python wrapper for the Genius API.
- [pronouncing](https://github.com/aparrish/pronouncingpy) – English pronunciation and rhyme.
- [gTTS](https://github.com/pndurette/gTTS) – Google Text‑to‑Speech.
- [PySide6](https://wiki.qt.io/Qt_for_Python) – Official Python bindings for Qt.
- [FluidSynth](http://www.fluidsynth.org/) – Real‑time software synthesizer.
- All the open‑source contributors whose libraries made this project possible.

---

**Note**: This project uses the Genius API to fetch lyrics. Please respect their [terms of service](https://genius.com/static/terms) and rate limits (free tier ~50 requests/day). For larger usage, consider caching results or using alternative lyric datasets.

**PS**: If I find a free, legal way to get data, I will mention it and use it later (like on Kaggle or other open-source platforms), or maybe I will make my own, but that will take some time. To be honest, don’t rely on that, because I have to respect the artist’s work and effort.

---

*Happy beat making!* 🎵