# Beat & Lyrics Generator

Python application that generates beats and lyrics with an interactive, editable workflow.  
- Currently focused on an **English/US Hip‑hop MVP** (Moroccan Arabic 'Darija' support planned later).  
*Perfect for music producers, rappers, or anyone exploring algorithmic music creation.*

---

## Overview

#### **For beat generation:**  
**Think of the code as a car – it's fully built and ready to run.** 
The SoundFonts are like gasoline; without them, the engine still runs, but with the right fuel, it will roar with professional audio quality.  

**For lyrics generation & voice generation:**  
The same concept applies **(Car & Gas)** – build the engine first, add the fuel (data) later.

#### Beat & Lyrics Generator lets you:
- **Generate a beat** – choose genre, theme, instrument, key, and tempo, and get a complete beat with chords, melody, and drums.
- **Generate a full track** – automatically produce a beat, lyrics, and vocals together.
- **Edit everything** – after generation, you can regenerate any component individually: chord progression, lead melody, drum patterns (kick, snare, hi‑hat separately), lyrics structure, and voice.
- **Save/load projects** – all generated data is stored in a local SQLite database for later retrieval.

- A modern GUI built with **PySide6** provides interactive control over all aspects.

#### **Future Improvment:**  
This project started as an ambitious blueprint and has been refined into a realistic, phased development plan  
I'm currently focusing on an **English/US Hip‑hop MVP**, with plans to later add support for Moroccan Arabic (Darija) and more advanced voice synthesis.

---

## Current Features (Phases 1–4 Completed)

### Beat Generator (Phase 1)
- **Chord progression generator** – Roman numeral templates per genre & theme (trap, drill, old‑school).  
   - Uses `music21` to convert numerals to actual notes in any key.
- **Melody generator** – Rule‑based: chord tones on strong beats, scale tones as passing notes.  
   -Avoids large leaps and pitch repetitions.
- **Drum pattern generator** – Probabilistic 16‑step patterns per genre (kick, snare, hi‑hat, open hat) with independent regeneration.
- **MIDI export & rendering** – Exports MIDI and renders to high‑quality WAV using **FluidSynth** + a SoundFont (you provide the SoundFont – the "gasoline").

### Lyrics Generator (Phase 2)
- **Lyrics acquisition** – Three curated Kaggle hip‑hop datasets (no API limits, fully offline).
- **Vocabulary extraction** – Theme‑based word frequency tables.
- **Theme assignment** – Combined VADER sentiment + keyword scoring to classify lines into 8 themes (hard, melancholic, reflective, smooth, confident, inspirational, playful, street love).
- **Markov chain generation** – Bigram/trigram models with weighted sampling produce coherent, theme‑aligned lyrics with rhyme support.

### Voice Synthesis (Phase 3)
- **Flexible TTS architecture** – Abstract provider interface allows easy swapping of TTS engines (ElevenLabs, Google, etc.).
- **ElevenLabs integration** – Professional, emotionally expressive TTS with support for voice cloning and multiple languages.
- **Placeholder provider** – Simulates TTS for testing without an API key (returns silent audio).
- **Error handling** – Gracefully manages API errors (invalid key, out of credits, rate limits) and network issues.
- **Tier‑agnostic design** – The same code works with any ElevenLabs subscription (Free, Starter, Creator, etc.).

### Full Track & Polish (Phase 4)
- **Full track generation** – Combines beat, lyrics, and voice into a final WAV file.
- **Save/load projects** – Save and restore entire project state (parameters, generated data) via JSON files.
- **GUI** – Fully functional PySide6 interface with separate tabs for beat editing and full track creation.
- **Individual track controls** – Regenerate chords, melody, or individual drums (kick, snare, hi‑hat, open hat) on the fly.

---


## Technology Stack

| Component                | Library/Tool                          | Status |
|--------------------------|---------------------------------------|--------|
| Music theory & MIDI      | music21, pretty_midi                  | ✅ |
| Drum patterns            | Custom probabilistic grids             | ✅ |
| High‑quality audio       | FluidSynth + custom SoundFonts         | ✅ (requires external SoundFont) |
| Lyrics acquisition       | Kaggle datasets (no API)              | ✅ |
| Vocabulary extraction    | Custom regex + frequency counting      | ✅ |
| Rhyme & generation       | pronouncing, Markov models             | ✅ |
| Sentiment/Theme          | VADER sentiment + keyword matching     | ✅ |
| Voice Synthesis          | Custom TTS module (ElevenLabs)         | ✅ (API key required) |
| GUI                      | PySide6                               | ✅ |
| Database                 | SQLite3                               | ✅ |

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

3. **Place the SoundFont** in the `resources/` folder and rename it to `default_soundfont.sf2` (or modify the path in `core/config.py`).

If the SoundFont is present, the application will use it automatically.


---

## Usage

### Starting the GUI
```bash
python -m gui.main_window
```

The main window has two tabs:

- **Beat Editor** – adjust parameters, generate a beat, and individually regenerate chords, melody, or each drum track. Save/load projects as `.beatproj` files.
- **Full Track** – generate a complete track (beat + lyrics + voice). Select parameters, choose TTS engine (placeholder or ElevenLabs), and click "Generate Full Track". You can also regenerate individual components (beat, lyrics, voice, chords, melody, all drums, or single drums). Save/load projects as `.trackproj` files.

### Command‑Line (for testing)
If you still want to use the command line, you can generate a beat as a WAV file:

```bash
python cli.py
```

Follow the prompts; the beat will be saved as a `.wav` file (no automatic playback). For lyrics testing, run:

```bash
python -m tests.test_markov_lyrics
```

---

## Project Structure

```
beat-lyrics-generator/
├── core/                             # Core logic modules
│   ├── __init__.py
│   ├── chord_generator.py
│   ├── drum_generator.py
│   ├── lyrics_generator.py
│   ├── melody_generator.py
│   ├── midi_exporter.py
│   ├── tts/                          # TTS module
│   │   ├── __init__.py
│   │   ├── provider.py
│   │   ├── placeholder.py
│   │   ├── elevenlabs.py
│   │   └── config.py
│   ├── alignment.py
│   ├── stretcher.py
│   ├── mixer.py
│   ├── project_manager.py
│   └── config.py                     # Common configuration (SoundFont path, etc.)
├── gui/                              # GUI code
│   ├── main_window.py
│   ├── beat_editor_widget.py
│   └── full_track_widget.py
├── data/                             # Database and data files
│   ├── raw_lyrics/                   # Kaggle datasets
│   ├── templates/                    # JSON seed files
│   ├── beat_lyrics.db
│   ├── database.py
│   └── theme_config.json
├── resources/                        # SoundFonts go here
│   └── default_soundfont.sf2
├── scripts/                          # Utility scripts (import, build, etc.)
├── tests/                            # Unit tests
├── .env.example
├── .gitignore
├── cli.py
├── init_db.py
├── init_lyrics_db.py
├── main.py
├── requirements.txt
├── run_tests.py
└── README.md
```

---

## Development Status & Roadmap

This project follows a **checkpoint‑based development plan**. Each checkpoint is a self‑contained feature. Below is the current progress (✅ = completed, ⬜ = pending).

| Phase | Checkpoint | Description | Status |
|-------|------------|------------|--------|
| **1: Beat Generator** |
| 1 | Project setup, virtual environment, basic PySide6 window with two buttons || ✅ |
| 2 | SQLite database setup, seed from JSON | tables for genres, themes, instruments, chord progressions, drum patterns | ✅ |
| 3 | Chord progression engine using music21 |  (Roman numeral → notes)  | ✅ |
| 4 | Rule‑based melody generator | (chord tones + passing notes) | ✅ |
| 5 | Probabilistic drum pattern generator | generate per genre | ✅ |
| 6 | MIDI export and FluidSynth rendering |*(high‑quality audio code ready, requires SoundFont)*| ✅ |
| 7 | GUI (PySide6 + QML)|  – **paused**, replaced with CLI for testing | ✅ |
| 7b | **Bug fixes and validation of Phase 1** || ✅ |
| **2: Lyrics Generator** |
| 8 | Import Kaggle lyrics datasets, build vocabulary, generate rhyming lines || ✅ |
| 9 | Vocabulary refinement | (sentiment analysis/theme assignment) | ✅ |
| 10 | Markov chain bigram model for improved line generation | using (bigram/trigram) | ✅ |
| 11 | Lyrics structure UI | (bars, hook, intro/outro, etc.) | ✅ |
| 12 | Theme matching between beat and lyrics || ✅ |
| 12b | Polish & Refinements | I have make a checklist *(check Notes/checkpoint12b)*| ✅ |
| **3: Voice Synthesis** |
| 13 | Flexible TTS architecture + ElevenLabs integration || ✅ |
| 14 | Syllabification and beat alignment || ✅ |
| 15 | Time‑stretching audio to fit beat durations || ✅ |
| 16 | Mixing beat and vocals, full track playback || ✅ |
| **4: Full Track & Polish** |
| 17 | Random full track generation || ✅ |
| 18 | Save/load project functionality || ✅ |
| 19 | UI/UX improvements | (progress bars, better layout) *check Notes/GUIchecklist*| ✅ |
| 20 | Testing, documentation, final polish || ✅ (current) |
| 20b |  Polish & Refinements | There is a lot to do | ✅ (current) |

---

## Acknowledgements

- [music21](http://web.mit.edu/music21/)
- [pretty_midi](https://github.com/craffel/pretty-midi)
- [FluidSynth](http://www.fluidsynth.org/)
- [VADER Sentiment](https://github.com/cjhutto/vaderSentiment)
- [pronouncing](https://github.com/aparrish/pronouncingpy)
- [ElevenLabs](https://elevenlabs.io/)
- All open‑source contributors and Kaggle dataset providers

---

**Note:** The GUI is now fully functional. No command‑line fallback is needed for daily use.

**Lyrics Data:** Instead of relying on live APIs, I've integrated three curated Kaggle hip-hop lyric datasets.  
The data is included in the repository, so you can generate lyrics offline with zero API limits.  
All preprocessing and vocabulary extraction are handled by the included scripts.
(You will find the datasets info with providers names in *'resources/lyrics_datasets_resources'*)

---

*Happy beat making!* 🎵

If you have feedback, feel free to contact me! I always try to do my best. Thanks!