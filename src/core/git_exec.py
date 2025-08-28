# core/git_exec.py
import subprocess
from typing import List, Tuple
import os
from src.utils import FileHandler
from commands.AbsClass import CommandFormat

ON_WINDOWS = os.name == "nt"

class GitExecutor:
    """Выполняет Git-команды и возвращает результат"""

    def execute(self, command: List[str], cwd) -> Tuple[bool, str, str]:
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                cwd=cwd,
                startupinfo=self.create_startupinfo()
            )
            success = result.returncode == 0
            return success, result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            return False, "", str(e)

    @staticmethod
    def create_startupinfo():
        """Скрывает консольное окно на Windows"""
        if ON_WINDOWS:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            return startupinfo
        return None

    @staticmethod
    def from_json(data: dict) -> CommandFormat:
        pass

    @staticmethod
    def to_json(data: CommandFormat) -> dict:
        pass
