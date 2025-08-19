# В основном файле app.py
from GUI.git_manager import GitManager
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication([])
    window = GitManager()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()