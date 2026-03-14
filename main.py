"""
Explanation:
This script creates a simple GUI for the beat and lyrics generator using PySide6.
It defines a main application window with a vertical layout containing two primary buttons.

Key functionalities include:
- 'MainWindow.__init__': initializes the QMainWindow, sets the window title and minimum size, and adds a central QWidget with a QVBoxLayout.
- Adds two buttons: "Generate Beat" and "Generate Full Track", with minimum height styling for better visibility.
- The layout ensures buttons are stacked vertically and the central widget hosts the layout.
- The script also contains the standard PySide6 application startup logic under '__main__', creating the QApplication, showing the main window, and executing the event loop.

This GUI provides a foundation for user interaction, where button clicks can later be connected to music generation functions.
"""

"""
*Content:
MainWindow.__init__()
"""






import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout,QWidget



# Set a title and size.
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beat & Lyrics Generator")      # Title
        self.setMinimumSize(400, 200)                       # Window size (width/height)

        # Create central widget and layout
        central_widget = QWidget()                          # A central widget holds a vertical layout.
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create buttons
        self.btn_generate_beat = QPushButton("Generate Beat")
        self.btn_generate_full = QPushButton("Generate Full Track")

        # Add buttons to layout
        layout.addWidget(self.btn_generate_beat)
        layout.addWidget(self.btn_generate_full)

        # Style buttons a bit
        self.btn_generate_beat.setMinimumHeight(50)         # button size height
        self.btn_generate_full.setMinimumHeight(50)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())