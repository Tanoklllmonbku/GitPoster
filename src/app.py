#app.py

VERSION = "Version_0.2"
BASE_CFG_PATH = "config/user_config.json"

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from GUI import MainWindow
from utils import get_logger
from utils import FileHandler

def create_base_cfg():
    base_cfg = {
        "user.name": "",
        "user.email": "",
        "last_repo_url": ""
    }
    FileHandler.save_config(base_cfg, BASE_CFG_PATH)

def ensure_dirs():
    Path("logs").mkdir(exist_ok=True)
    Path("config").mkdir(exist_ok=True)

    if not os.path.exists(BASE_CFG_PATH):
        create_base_cfg()
    else:
        pass

def main():
    ensure_dirs()
    logger = get_logger(version=VERSION)
    logger.info("Git Manager запущен")

    app = QApplication(sys.argv)
    window = MainWindow(logger)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()