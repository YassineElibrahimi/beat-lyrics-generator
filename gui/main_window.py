# gui/main_window.
"""
Main window for Beat & Lyrics Generator GUI.
"""

import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget,
                                QApplication, QMessageBox)
from gui.beat_editor_widget import BeatEditorWidget
from gui.full_track_widget import FullTrackWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beat & Lyrics Generator")
        self.setMinimumSize(900, 700)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Beat Editor Tab
        self.beat_editor = BeatEditorWidget()
        self.tabs.addTab(self.beat_editor, "Beat Editor")

        # Full Track Tab
        self.full_track = FullTrackWidget()
        self.tabs.addTab(self.full_track, "Full Track")
        self.full_track.track_generated.connect(self.on_track_generated)

    def on_track_generated(self, path):
        """Show a notification when a full track is ready."""
        QMessageBox.information(self, "Track Ready", f"Full track saved to:\n{path}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()