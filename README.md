# Beat & Lyrics Generator

Python application that generates beats and lyrics with an interactive, editable workflow.  
- Currently focused on an **English/US Hip‑hop MVP** (Moroccan Arabic 'Darija' support planned later).  
*Perfect for music producers, rappers, or anyone exploring algorithmic music creation.*

---

## Overview

**Think of the code as a car – it's fully built and ready to run.** The SoundFonts are like gasoline; without them, the engine still runs (using a pygame fallback), but with the right fuel, it will roar with professional audio quality

Beat & Lyrics Generator lets you:
- **Generate a beat** – choose genre, theme, instrument, key, and tempo, and get a complete beat with chords, melody, and drums.
- **Generate a full track** *(planned)*  – automatically produce a beat, lyrics, and vocals together.
- **Edit everything** – after generation, you can regenerate any component individually: chord progression, lead melody, drum patterns (kick, snare, hi‑hat separately), lyrics structure, and voice.
- **Save/load projects** – all generated data is stored in a local SQLite database for later retrieval.

The GUI is currently under construction; we use a **command‑line interface (CLI)** to test and validate the core modules. Once the backend is polished, the GUI will be re‑integrated.

This project started as an ambitious blueprint and has been refined into a realistic, phased development plan. I'm  currently focusing on an **English/US Hip‑hop MVP**, with plans to later add support for Moroccan Arabic (Darija) and more advanced voice synthesis.

---

## Current Features (Phase 1 – Beat Generator)

- **Chord progression generator**  
  - Roman numeral templates per genre & theme (trap, drill, old‑school).  
  - Uses `music21` to convert numerals to actual notes in any key.

- **Melody generator**  
  - Rule‑based: chord tones on strong beats, scale tones as passing notes.  
  - Avoids large leaps and immediate pitch repetitions for more natural lines.

- **Drum pattern generator**  
  - Probabilistic 16‑step patterns per genre (kick, snare, hi‑hat, open hat).  
  - Independent regeneration of each drum track.

- **MIDI export & playback**  
  - Combines chords, melody, and drums into a single MIDI file via `pretty_midi`.  
  - Two playback modes:
    - **Pygame fallback** (low quality, works out‑of‑the‑box).
    - **FluidSynth + SoundFont** (professional quality) – *code is ready; you provide the SoundFont ("gasoline").*

- **Command‑line interface**  
  - `cli.py` lets you select parameters, generate a beat, save MIDI, and play it.  
  - A temporary solution while the GUI is being refined.

---


## Technology Stack *(Planned & Current)*

| Component                | Library/Tool                          | Status |
|--------------------------|---------------------------------------|--------|
| Music theory & MIDI      | music21, pretty_midi                  | ✅     |
| Drum patterns            | Custom probabilistic grids             | ✅     |
| Audio playback (fallback)| pygame                                 | ✅     |
| High‑quality audio       | FluidSynth + custom SoundFonts         | ✅ (code ready; requires external SoundFont) |
| Lyrics acquisition       | Kaggle datasets (no API)              | ✅ (imported) |
| Vocabulary extraction      | Custom regex + frequency counting              | ✅ |
| Rhyme & generation      | pronouncing, custom Markov-inspired              | ✅ |
| Sentiment analysis       | vaderSentiment / textblob              | ⬜ (Phase 2) |
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

Run the beat generator from the command line:

```bash
python cli.py
```

You will be prompted to enter:
- **Genre**: trap / drill / old_school
- **Theme**: hard / melancholic / aggressive / smooth
- **Key**: e.g., C, D, etc.
- **Tempo**: BPM (default 140)

The program then:
- Generates chords, melody, and drums.
- Saves a MIDI file (e.g., `beat_trap_hard_C_140.mid`).
- Plays the MIDI using the best available audio method (FluidSynth if SoundFont found, otherwise pygame).

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
| 6 | MIDI export and playback (pygame + FluidSynth ready)   |*(high‑quality audio code ready, requires SoundFont)*| ✅ |
| 7 | GUI (PySide6 + QML)|  – **paused**, replaced with CLI for testing | ⬜/✅ |
| 7b | **Bug fixes and validation of Phase 1** || ✅ |
| **2: Lyrics Generator** |
| 8 | Import Kaggle lyrics datasets, build vocabulary, generate rhyming lines || ✅ |
| 9 | Vocabulary refinement (sentiment analysis, theme assignment)  || ⬜ |
| 10 | Improved line generation (Markov chains) || ⬜ |
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

**PS**: If I find a free, legal way to get data, I will mention it and use it later (like on Kaggle or other open-source platforms), or maybe I will make my own, but that will take some time. To be honest, don’t rely on that, because I have to respect the artist’s work and effort. (I have Done it ✅ *read below*)

Lyrics Data: Instead of relying on live APIs, we've integrated three curated Kaggle hip-hop lyric datasets. The data is included in the repository, so you can generate lyrics offline with zero API limits. All preprocessing and vocabulary extraction are handled by the included scripts.

---

*Happy beat making!* 🎵