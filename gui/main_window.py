# gui/main_window.
"""
Main window for Beat & Lyrics Generator GUI.
"""

import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget,
                                QApplication)
from gui.beat_editor_widget import BeatEditorWidget

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

        # Full Track Tab (placeholder for now)
        self.full_track_tab = QWidget()
        self.tabs.addTab(self.full_track_tab, "Full Track")

        # Connect signals if needed
        self.beat_editor.beat_updated.connect(self.on_beat_updated)

    def on_beat_updated(self, beat_data):
        """Handle beat updates (e.g., for preview or passing to full track tab)."""
        print("Beat updated:", beat_data['tempo'])  # placeholder

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()