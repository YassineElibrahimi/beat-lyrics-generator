# gui/beat_editor_widget.py
"""
Beat Editor Widget – allows generating beats and editing individual tracks.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                               QLabel, QComboBox, QSlider, QPushButton,
                               QGridLayout, QScrollArea, QFrame)
from PySide6.QtCore import Qt, Signal
from core.chord_generator import ChordGenerator
from core.melody_generator import MelodyGenerator
from core.drum_generator import DrumGenerator
from core.midi_exporter import MIDIExporter

class BeatEditorWidget(QWidget):
    """Widget for generating and editing beats."""

    # Signal emitted when a new beat is generated
    beat_updated = Signal(object)  # will pass a dict of track data

    def __init__(self):
        super().__init__()
        self.chord_gen = ChordGenerator()
        self.melody_gen = MelodyGenerator()
        self.drum_gen = DrumGenerator()
        self.current_genre = "trap"
        self.current_theme = "hard"
        self.current_key = "C"
        self.current_tempo = 140
        self.current_instrument = "piano"

        self._setup_ui()

    def _setup_ui(self):
        """Create all UI elements."""
        main_layout = QVBoxLayout(self)

        # --- Parameters Group ---
        params_group = QGroupBox("Beat Parameters")
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
        self.generate_btn = QPushButton("Generate Beat")
        self.generate_btn.clicked.connect(self.generate_beat)
        params_layout.addWidget(self.generate_btn, 3, 0, 1, 4)

        main_layout.addWidget(params_group)

        # --- Tracks Display (will show generated tracks) ---
        self.tracks_group = QGroupBox("Tracks")
        tracks_layout = QVBoxLayout(self.tracks_group)
        self.tracks_area = QScrollArea()
        self.tracks_area.setWidgetResizable(True)
        self.tracks_container = QWidget()
        self.tracks_container_layout = QVBoxLayout(self.tracks_container)
        self.tracks_area.setWidget(self.tracks_container)
        tracks_layout.addWidget(self.tracks_area)
        main_layout.addWidget(self.tracks_group)

        self.tracks_group.setVisible(False)  # hidden until first generation

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

    def generate_beat(self):
        """Generate a new beat with current parameters."""
        # Clear previous tracks display
        self._clear_tracks()

        # Generate components
        self.chords = self.chord_gen.generate(self.current_genre, self.current_theme, self.current_key)
        self.melody = self.melody_gen.generate_melody(self.chords, key_name=self.current_key, durations_per_chord=4)
        self.drum_events = self.drum_gen.get_all_events(self.current_genre)

        # Display tracks
        self._add_track_panel("Chords", self._format_chords(), self.regenerate_chords)
        self._add_track_panel("Melody", self._format_melody(), self.regenerate_melody)
        self._add_drum_panel()

        self.tracks_group.setVisible(True)
        self.beat_updated.emit({
            'chords': self.chords,
            'melody': self.melody,
            'drums': self.drum_events,
            'tempo': self.current_tempo
        })

    def _clear_tracks(self):
        """Remove all track panels."""
        for i in reversed(range(self.tracks_container_layout.count())):
            self.tracks_container_layout.itemAt(i).widget().deleteLater()

    def _add_track_panel(self, title, content, regenerate_callback):
        """Add a track panel with title, content, and regenerate button."""
        panel = QFrame()
        panel.setFrameShape(QFrame.Box)
        layout = QVBoxLayout(panel)

        # Title row
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel(f"<b>{title}</b>"))
        regenerate_btn = QPushButton("Regenerate")
        regenerate_btn.clicked.connect(regenerate_callback)
        title_layout.addWidget(regenerate_btn)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # Content
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        layout.addWidget(content_label)

        self.tracks_container_layout.addWidget(panel)

    def _add_drum_panel(self):
        """Add drum panel with separate buttons for each drum."""
        panel = QFrame()
        panel.setFrameShape(QFrame.Box)
        layout = QVBoxLayout(panel)

        # Title row
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("<b>Drums</b>"))
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # Buttons for each drum
        drum_layout = QHBoxLayout()
        drums = [
            ("Kick", self.regenerate_kick),
            ("Snare", self.regenerate_snare),
            ("Hi-hat", self.regenerate_hihat),
            ("Open Hat", self.regenerate_open_hat)
        ]
        for name, callback in drums:
            btn = QPushButton(name)
            btn.clicked.connect(callback)
            drum_layout.addWidget(btn)
        layout.addLayout(drum_layout)

        # Drum pattern display
        self.drum_display = QLabel(self._format_drums())
        self.drum_display.setWordWrap(True)
        layout.addWidget(self.drum_display)

        self.tracks_container_layout.addWidget(panel)

    def _format_chords(self):
        """Format chords as readable string."""
        return " | ".join([c.pitchedCommonName for c in self.chords])

    def _format_melody(self):
        """Format first few melody notes."""
        notes = list(self.melody.notes)
        if not notes:
            return "[no notes]"
        note_names = [n.nameWithOctave for n in notes[:8]]
        return " ".join(note_names) + ("..." if len(notes) > 8 else "")

    def _format_drums(self):
        """Format drum pattern as string."""
        if not hasattr(self.drum_gen, 'current_grid'):
            return "[no drums]"
        lines = []
        for instrument, grid in self.drum_gen.current_grid.items():
            active = [i for i, val in enumerate(grid) if val]
            lines.append(f"{instrument}: {active}")
        return "\n".join(lines)

    def regenerate_chords(self):
        """Regenerate only the chords."""
        self.chords = self.chord_gen.generate(self.current_genre, self.current_theme, self.current_key)
        # Update display
        self._clear_tracks()
        self._add_track_panel("Chords", self._format_chords(), self.regenerate_chords)
        self._add_track_panel("Melody", self._format_melody(), self.regenerate_melody)
        self._add_drum_panel()
        self.beat_updated.emit({
            'chords': self.chords,
            'melody': self.melody,
            'drums': self.drum_events,
            'tempo': self.current_tempo
        })

    def regenerate_melody(self):
        """Regenerate only the melody."""
        self.melody = self.melody_gen.generate_melody(self.chords, key_name=self.current_key, durations_per_chord=4)
        self._clear_tracks()
        self._add_track_panel("Chords", self._format_chords(), self.regenerate_chords)
        self._add_track_panel("Melody", self._format_melody(), self.regenerate_melody)
        self._add_drum_panel()
        self.beat_updated.emit({
            'chords': self.chords,
            'melody': self.melody,
            'drums': self.drum_events,
            'tempo': self.current_tempo
        })

    def regenerate_kick(self):
        self._regenerate_drum('kick')

    def regenerate_snare(self):
        self._regenerate_drum('snare')

    def regenerate_hihat(self):
        self._regenerate_drum('hihat')

    def regenerate_open_hat(self):
        self._regenerate_drum('open_hat')

    def _regenerate_drum(self, instrument):
        """Regenerate a specific drum instrument."""
        self.drum_gen.generate_pattern(self.current_genre, regenerate=[instrument])
        self.drum_events = self.drum_gen.get_all_events(self.current_genre)
        # Update display
        self.drum_display.setText(self._format_drums())
        self.beat_updated.emit({
            'chords': self.chords,
            'melody': self.melody,
            'drums': self.drum_events,
            'tempo': self.current_tempo
        })