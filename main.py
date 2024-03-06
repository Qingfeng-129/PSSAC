from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel
from PySide6.QtCore import Qt


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PSSAC2.0")


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()