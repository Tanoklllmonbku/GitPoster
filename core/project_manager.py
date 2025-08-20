# core/project_manager.py
import subprocess
from pathlib import Path

import os
ON_WINDOWS = os.name == "nt"

def create_startupinfo():
    """Скрывает консольное окно на Windows"""
    if ON_WINDOWS:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        return startupinfo
    return None