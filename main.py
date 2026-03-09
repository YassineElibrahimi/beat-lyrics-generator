'''
Explanation:
I create a QMainWindow, set a title and size.
A central widget holds a vertical layout.
Add two buttons.
The if __name__ == "__main__": block runs the application.
'''



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