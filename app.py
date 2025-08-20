#app.py
import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from GUI import MainWindow
from utils.logger import get_logger

def ensure_dirs():
    Path("logs").mkdir(exist_ok=True)
    Path("config").mkdir(exist_ok=True)

def main():
    ensure_dirs()
    logger = get_logger()
    logger.info("Git Manager запущен")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()