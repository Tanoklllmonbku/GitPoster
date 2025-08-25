# core/env.py
import os
import shutil
from pathlib import Path

def find_git():
    """Ищет git.exe: сначала в PATH, потом в embedded, потом предлагает установить"""

    if shutil.which("git"):
        return "git"  # можно вызывать напрямую

    embedded_git = Path("embedded/portable_git/bin/git.exe")
    if embedded_git.exists():
        return str(embedded_git)

    local_git = Path.home() / "GitPoster" / "git" / "bin" / "git.exe"
    if local_git.exists():
        return str(local_git)

    return None

def is_git_ready():
    """Проверяет, можно ли использовать git"""
    return find_git() is not None