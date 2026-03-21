# gui/full_track_widget.py
"""
Full Track Widget - generates beat, lyrics, and voice, with individual track controls.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                                QLabel, QComboBox, QSlider, QPushButton,
                                QGridLayout, QScrollArea, QFrame, QTextEdit,
                                QSplitter, QFileDialog, QMessageBox, QApplication)
from PySide6.QtCore import Qt, Signal
from core.chord_generator import ChordGenerator
from core.melody_generator import MelodyGenerator
from core.drum_generator import DrumGenerator
from core.midi_exporter import MIDIExporter
from core.lyrics_generator import LyricsGenerator
from core.alignment import VocalAligner
from core.tts import get_tts_provider
from core.stretcher import stretch_audio
from core.mixer import mix_tracks
from pydub import AudioSegment
import os
import random
from datetime import datetime
from core.project_manager import ProjectManager
from core.config import SOUNDFONT_PATH


class FullTrackWidget(QWidget):
    """Widget for generating full tracks (beat + lyrics + voice)."""

    track_generated = Signal(str)  # emits path to final WAV

    def __init__(self):
        super().__init__()
        self.chord_gen = ChordGenerator()
        self.melody_gen = MelodyGenerator()
        self.drum_gen = DrumGenerator()
        self.lyrics_gen = LyricsGenerator()

        # Current data
        self.current_genre = "trap"
        self.current_theme = "hard"
        self.current_key = "C"
        self.current_tempo = 140
        self.current_instrument = "piano"
        self.current_lyrics = []
        self.current_beat_data = {}
        self.current_vocal_path = None
        self.current_beat_wav = None
        self.button_layout = None

        self._setup_ui()

    def _setup_ui(self):
        """Create all UI elements."""
        main_layout = QVBoxLayout(self)

        # Add Save/Load buttons
        toolbar = QHBoxLayout()
        self.save_btn = QPushButton("Save Project")
        self.save_btn.clicked.connect(self.save_project)
        self.load_btn = QPushButton("Load Project")
        self.load_btn.clicked.connect(self.load_project)
        toolbar.addWidget(self.save_btn)
        toolbar.addWidget(self.load_btn)
        toolbar.addStretch()
        main_layout.addLayout(toolbar)

        # --- Parameters Group ---
        params_group = QGroupBox("Track Parameters")
        params_layout = QGridLayout(params_group)

        # Genre
        params_layout.addWidget(QLabel("Genre:"), 0, 0)
        self.genre_combo = QComboBox()
        self.genre_combo.addItems(["trap", "drill", "old_school"])
        self.genre_combo.currentTextChanged.connect(self._on_genre_changed)
        params_layout.addWidget(self.genre_combo, 0, 1)

        # Theme
        params_layout.addWidget(QLabel("Theme:"), 0, 2)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["hard", "melancholic", "aggressive", "smooth"])
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        params_layout.addWidget(self.theme_combo, 0, 3)

        # Lead Instrument
        params_layout.addWidget(QLabel("Lead Instrument:"), 1, 0)
        self.instrument_combo = QComboBox()
        self.instrument_combo.addItems(["piano", "brass", "flute", "violin", "synth_lead", "bass"])
        self.instrument_combo.currentTextChanged.connect(self._on_instrument_changed)
        params_layout.addWidget(self.instrument_combo, 1, 1)

        # Key
        params_layout.addWidget(QLabel("Key:"), 1, 2)
        self.key_combo = QComboBox()
        self.key_combo.addItems(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])
        self.key_combo.setCurrentText("C")
        self.key_combo.currentTextChanged.connect(self._on_key_changed)
        params_layout.addWidget(self.key_combo, 1, 3)

        # Tempo
        params_layout.addWidget(QLabel("Tempo (BPM):"), 2, 0)
        self.tempo_slider = QSlider(Qt.Horizontal)
        self.tempo_slider.setRange(60, 200)
        self.tempo_slider.setValue(140)
        self.tempo_slider.valueChanged.connect(self._on_tempo_changed)
        params_layout.addWidget(self.tempo_slider, 2, 1, 1, 2)
        self.tempo_label = QLabel("140")
        params_layout.addWidget(self.tempo_label, 2, 3)

        # Generate button
        self.generate_btn = QPushButton("Generate Full Track")
        self.generate_btn.clicked.connect(self.generate_full_track)
        params_layout.addWidget(self.generate_btn, 3, 0, 1, 4)

        main_layout.addWidget(params_group)

        # --- Splitter for Beat, Lyrics, and Voice controls ---
        splitter = QSplitter(Qt.Horizontal)

        # Beat Panel
        self.beat_panel = self._create_beat_panel()
        splitter.addWidget(self.beat_panel)

        # Lyrics Panel
        self.lyrics_panel = self._create_lyrics_panel()
        splitter.addWidget(self.lyrics_panel)

        # Voice Panel
        self.voice_panel = self._create_voice_panel()
        splitter.addWidget(self.voice_panel)

        main_layout.addWidget(splitter)

    def _create_beat_panel(self):
        """Create panel for beat controls."""
        panel = QGroupBox("Beat")
        layout = QVBoxLayout(panel)

        self.beat_status = QLabel("Not generated")
        layout.addWidget(self.beat_status)

        # Regenerate buttons
        btn_layout = QHBoxLayout()
        self.regenerate_beat_btn = QPushButton("Regenerate Beat")
        self.regenerate_beat_btn.clicked.connect(self.regenerate_beat)
        self.regenerate_beat_btn.setEnabled(False)
        btn_layout.addWidget(self.regenerate_beat_btn)

        layout.addLayout(btn_layout)

        # Placeholder for individual track buttons (will be populated after generation)
        self.beat_tracks_layout = QVBoxLayout()
        layout.addLayout(self.beat_tracks_layout)

        return panel

    def _create_lyrics_panel(self):
        """Create panel for lyrics display and controls."""
        panel = QGroupBox("Lyrics")
        layout = QVBoxLayout(panel)

        self.lyrics_text = QTextEdit()
        self.lyrics_text.setReadOnly(True)
        layout.addWidget(self.lyrics_text)

        btn_layout = QHBoxLayout()
        self.regenerate_lyrics_btn = QPushButton("Regenerate Lyrics")
        self.regenerate_lyrics_btn.clicked.connect(self.regenerate_lyrics)
        self.regenerate_lyrics_btn.setEnabled(False)
        btn_layout.addWidget(self.regenerate_lyrics_btn)

        layout.addLayout(btn_layout)

        return panel

    def _create_voice_panel(self):
        """Create panel for voice synthesis controls."""
        panel = QGroupBox("Voice")
        layout = QVBoxLayout(panel)

        # TTS Provider selection (placeholder vs ElevenLabs)
        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("TTS Engine:"))
        self.tts_provider_combo = QComboBox()
        self.tts_provider_combo.addItems(["placeholder", "elevenlabs"])
        provider_layout.addWidget(self.tts_provider_combo)
        layout.addLayout(provider_layout)

        self.voice_status = QLabel("Not generated")
        layout.addWidget(self.voice_status)

        self.regenerate_voice_btn = QPushButton("Regenerate Voice")
        self.regenerate_voice_btn.clicked.connect(self.regenerate_voice)
        self.regenerate_voice_btn.setEnabled(False)
        layout.addWidget(self.regenerate_voice_btn)

        return panel

    def _on_genre_changed(self, genre):
        self.current_genre = genre

    def _on_theme_changed(self, theme):
        self.current_theme = theme

    def _on_instrument_changed(self, instrument):
        self.current_instrument = instrument

    def _on_key_changed(self, key):
        self.current_key = key

    def _on_tempo_changed(self, value):
        self.current_tempo = value
        self.tempo_label.setText(str(value))

    def generate_full_track(self):
        """Generate a complete track: beat, lyrics, voice, mix."""
        self.generate_beat()
        self.generate_lyrics()
        self.generate_voice()
        self.mix_track()

    def generate_beat(self):
        """Generate the beat (same as in beat editor)."""
        self.beat_status.setText("Generating beat...")

        # Generate components
        self.current_chords = self.chord_gen.generate(self.current_genre, self.current_theme, self.current_key)
        self.current_melody = self.melody_gen.generate_melody(self.current_chords, key_name=self.current_key, durations_per_chord=4)
        self.current_drum_events = self.drum_gen.get_all_events(self.current_genre)

        # Store for later use
        self.current_beat_data = {
            'chords': self.current_chords,
            'melody': self.current_melody,
            'drums': self.current_drum_events,
            'tempo': self.current_tempo
        }

        # Export MIDI
        exporter = MIDIExporter(tempo=self.current_tempo)
        exporter.add_chords(self.current_chords, program=1)
        exporter.add_melody(self.current_melody, program=73)
        exporter.add_drums(self.current_drum_events)

        midi_filename = f"temp_beat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mid"
        exporter.save(midi_filename)

        # Render to WAV using FluidSynth
        beat_wav = f"temp_beat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        exporter.render_to_wav(SOUNDFONT_PATH, beat_wav)
        self.current_beat_wav = beat_wav

        total_beats = sum(c.quarterLength for c in self.current_chords)
        total_seconds = total_beats * (60.0 / self.current_tempo)
        self.beat_status.setText(f"Beat generated ({total_seconds:.1f}s)")
        self.regenerate_beat_btn.setEnabled(True)
        self._populate_beat_tracks()

    def _populate_beat_tracks(self):
        """Populate individual track buttons for beat regeneration."""
        # Remove existing button layout if present
        if hasattr(self, 'button_layout') and self.button_layout:
            # Clear all widgets from the layout
            while self.button_layout.count():
                child = self.button_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            # Remove the layout from the parent
            self.beat_tracks_layout.removeItem(self.button_layout)
            self.button_layout.deleteLater()

        # Create a vertical container for button rows
        self.button_layout = QVBoxLayout()

        # Row 1: Chords, Melody, All Drums
        row1 = QHBoxLayout()
        chords_btn = QPushButton("Regenerate Chords")
        chords_btn.clicked.connect(self.regenerate_chords)
        melody_btn = QPushButton("Regenerate Melody")
        melody_btn.clicked.connect(self.regenerate_melody)
        drums_btn = QPushButton("Regenerate All Drums")
        drums_btn.clicked.connect(self.regenerate_drums)
        row1.addWidget(chords_btn)
        row1.addWidget(melody_btn)
        row1.addWidget(drums_btn)
        self.button_layout.addLayout(row1)

        # Row 2: Individual drum buttons
        row2 = QHBoxLayout()
        kick_btn = QPushButton("Kick")
        kick_btn.clicked.connect(self.regenerate_kick)
        snare_btn = QPushButton("Snare")
        snare_btn.clicked.connect(self.regenerate_snare)
        hihat_btn = QPushButton("Hi‑hat")
        hihat_btn.clicked.connect(self.regenerate_hihat)
        openhat_btn = QPushButton("Open Hat")
        openhat_btn.clicked.connect(self.regenerate_open_hat)
        row2.addWidget(kick_btn)
        row2.addWidget(snare_btn)
        row2.addWidget(hihat_btn)
        row2.addWidget(openhat_btn)
        self.button_layout.addLayout(row2)

        self.beat_tracks_layout.addLayout(self.button_layout)

    def generate_lyrics(self):
        """Generate lyrics based on theme."""
        self.lyrics_text.setText("Generating lyrics...")
        self.current_lyrics = self.lyrics_gen.generate_verse_markov(theme=self.current_theme, num_bars=8, rhyme_scheme='AABB')
        self.lyrics_text.setText("\n".join(self.current_lyrics))
        self.regenerate_lyrics_btn.setEnabled(True)

    def generate_voice(self):
        """Synthesize voice from lyrics."""
        self.voice_status.setText("Generating voice...")
        QApplication.processEvents()  # Force UI update

        provider_name = self.tts_provider_combo.currentText()
        try:
            tts = get_tts_provider(provider_name)
        except Exception as e:
            self.voice_status.setText(f"Error: {e}")
            QMessageBox.critical(self, "TTS Error", str(e))
            return

        # Align syllables to beat
        aligner = VocalAligner(tempo_bpm=self.current_tempo)
        events = aligner.align_lyrics(self.current_lyrics, rest_duration_beats=1.0)

        # Synthesize each syllable
        syllable_duration = 0.25  # 16th note
        vocal_tracks = []
        try:
            for _, syllable in events:
                syl_audio = tts.synthesize(syllable, apply_vst=False)
                stretched = stretch_audio(syl_audio, target_duration_sec=syllable_duration)
                vocal_tracks.append(stretched)
        except Exception as e:
            self.voice_status.setText(f"Synthesis failed: {e}")
            QMessageBox.critical(self, "Voice Synthesis Error", str(e))
            return

        if vocal_tracks:
            final_vocal = vocal_tracks[0]
            for track in vocal_tracks[1:]:
                final_vocal += track
            self.current_vocal_path = f"temp_vocal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            final_vocal.export(self.current_vocal_path, format="wav")
            self.voice_status.setText(f"Voice generated ({len(events)} syllables)")
        else:
            self.voice_status.setText("Voice generation failed")
            return

        self.regenerate_voice_btn.setEnabled(True)

    def mix_track(self):
        """Mix beat and voice into final track."""
        if not self.current_beat_wav or not self.current_vocal_path:
            self.voice_status.setText("Need both beat and voice to mix")
            return

        output_file = f"full_track_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        mix_tracks(self.current_vocal_path, self.current_beat_wav, output_file, vocal_gain_db=0, beat_gain_db=-6)
        self.track_generated.emit(output_file)
        self.voice_status.setText(f"Mixed track saved: {output_file}")

    # --- Helper to rebuild drum events from current grid ---
    def _rebuild_drum_events_from_grid(self):
        """Rebuild self.current_drum_events from self.drum_gen.current_grid."""
        events = []
        for inst, grid in self.drum_gen.current_grid.items():
            note = self.drum_gen.DRUM_NOTES.get(inst)
            if note is None:
                continue
            for step, active in enumerate(grid):
                if active:
                    time_in_beats = step * 0.25
                    events.append((time_in_beats, note, 100))
        events.sort(key=lambda x: x[0])
        self.current_drum_events = events

    # --- Individual drum regeneration methods ---
    def regenerate_kick(self):
        self._regenerate_single_drum('kick')

    def regenerate_snare(self):
        self._regenerate_single_drum('snare')

    def regenerate_hihat(self):
        self._regenerate_single_drum('hihat')

    def regenerate_open_hat(self):
        self._regenerate_single_drum('open_hat')

    def _regenerate_single_drum(self, instrument):
        """Regenerate a specific drum instrument and update the track."""
        self.drum_gen.generate_pattern(self.current_genre, regenerate=[instrument])
        self._rebuild_drum_events_from_grid()
        self._update_beat_from_current()
        self.generate_voice()
        self.mix_track()

    # --- Existing regeneration methods ---
    def regenerate_beat(self):
        self.generate_beat()
        self.generate_voice()
        self.mix_track()

    def regenerate_lyrics(self):
        self.generate_lyrics()
        self.generate_voice()
        self.mix_track()

    def regenerate_voice(self):
        self.generate_voice()
        self.mix_track()

    def regenerate_chords(self):
        # Regenerate only chords, keep melody and drums
        self.current_chords = self.chord_gen.generate(self.current_genre, self.current_theme, self.current_key)
        self.current_melody = self.melody_gen.generate_melody(self.current_chords, key_name=self.current_key, durations_per_chord=4)
        # Drums remain unchanged – no need to regenerate
        self._update_beat_from_current()
        self.generate_voice()
        self.mix_track()

    def regenerate_melody(self):
        # Regenerate only melody
        self.current_melody = self.melody_gen.generate_melody(self.current_chords, key_name=self.current_key, durations_per_chord=4)
        self._update_beat_from_current()
        self.generate_voice()
        self.mix_track()

    def regenerate_drums(self):
        # Regenerate all drums
        self.current_drum_events = self.drum_gen.get_all_events(self.current_genre)
        self._update_beat_from_current()
        self.generate_voice()
        self.mix_track()

    def _update_beat_from_current(self):
        """Update beat WAV after regenerating a component."""
        exporter = MIDIExporter(tempo=self.current_tempo)
        exporter.add_chords(self.current_chords, program=1)
        exporter.add_melody(self.current_melody, program=73)
        exporter.add_drums(self.current_drum_events)

        midi_filename = f"temp_beat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mid"
        exporter.save(midi_filename)

        # Render to WAV using FluidSynth
        beat_wav = f"temp_beat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        exporter.render_to_wav(SOUNDFONT_PATH, beat_wav)
        self.current_beat_wav = beat_wav

        total_beats = sum(c.quarterLength for c in self.current_chords)
        total_seconds = total_beats * (60.0 / self.current_tempo)
        self.beat_status.setText(f"Beat updated ({total_seconds:.1f}s)")

    def get_project_data(self):
        """Collect current project data for saving."""
        return {
            'type': 'full_track',
            'genre': self.current_genre,
            'theme': self.current_theme,
            'key': self.current_key,
            'tempo': self.current_tempo,
            'instrument': self.current_instrument,
            'lyrics': self.current_lyrics,
            'tts_provider': self.tts_provider_combo.currentText(),
            'beat_data': {
                'chords': [c.pitchedCommonName for c in self.current_chords] if hasattr(self, 'current_chords') else [],
                'melody_notes': [n.nameWithOctave for n in list(self.current_melody.notes)[:20]] if hasattr(self, 'current_melody') else [],
                'drum_patterns': self.drum_gen.current_grid if hasattr(self.drum_gen, 'current_grid') else {}
            }
        }

    def load_project_data(self, data):
        """Load project data and restore state."""
        if data.get('type') != 'full_track':
            return False

        # Restore parameters
        self.genre_combo.setCurrentText(data.get('genre', 'trap'))
        self.theme_combo.setCurrentText(data.get('theme', 'hard'))
        self.key_combo.setCurrentText(data.get('key', 'C'))
        self.tempo_slider.setValue(data.get('tempo', 140))
        self.instrument_combo.setCurrentText(data.get('instrument', 'piano'))
        self.tts_provider_combo.setCurrentText(data.get('tts_provider', 'placeholder'))

        # Restore lyrics
        self.current_lyrics = data.get('lyrics', [])
        if self.current_lyrics:
            self.lyrics_text.setText("\n".join(self.current_lyrics))

        # Regenerate beat and voice
        self.generate_beat()
        self.generate_voice()
        self.mix_track()
        return True

    def save_project(self):
        """Save current project to a JSON file."""
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Full Track Project", "", "Full Track Project (*.trackproj);;All Files (*)"
        )
        if filepath:
            data = self.get_project_data()
            ProjectManager.save_project(filepath, data)
            QMessageBox.information(self, "Save Project", f"Project saved to {filepath}")

    def load_project(self):
        """Load a project from a JSON file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Load Full Track Project", "", "Full Track Project (*.trackproj);;All Files (*)"
        )
        if filepath:
            try:
                data = ProjectManager.load_project(filepath)
                self.load_project_data(data)
                QMessageBox.information(self, "Load Project", f"Project loaded from {filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Load Error", f"Failed to load project: {e}")