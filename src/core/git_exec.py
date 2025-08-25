# core/git_exec.py
import subprocess
from typing import List, Tuple
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

class GitExecutor:
    """Выполняет Git-команды и возвращает результат"""

    @staticmethod
    def execute(command: List[str], cwd) -> Tuple[bool, str, str]:
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                cwd=cwd,
                startupinfo=create_startupinfo()
            )
            success = result.returncode == 0
            return success, result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            return False, "", str(e)