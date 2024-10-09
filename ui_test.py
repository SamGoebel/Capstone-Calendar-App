import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

# Define a basic window
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("PyQt5 Example")

        # Create label and button
        self.label = QLabel("Click the button", self)
        self.button = QPushButton("Click me", self)
        self.button.clicked.connect(self.button_clicked)

        # Arrange layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def button_clicked(self):
        self.label.setText("Button clicked!")

# Run the application
app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
