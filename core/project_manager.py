# core/project_manager.py
import subprocess
import os
from pathlib import Path

from commands import init, status, add, commit, push, remote
from .git_exec import GitExecutor
from utils.gitignore_temp import get_default_gitignore
from utils import get_logger
from utils import FileHandler

logger = get_logger()

CONFIG_PATH = "config/user_config.json"
ON_WINDOWS = os.name == "nt"

def create_startupinfo():
    """Скрывает окно консоли при использовании subprocess на Windows"""
    if ON_WINDOWS:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        return startupinfo
    return None


class ProjectManager:
    """Управление Git-проектом"""

    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.executor = GitExecutor()

    def is_git_repo(self) -> bool:
        cmd, cwd = status.git_status_porcelain(self.project_dir)
        success, _, _ = self.executor.execute(cmd, cwd)
        return success

    def initialize(self, repo_url: str = "") -> dict:
        logger.info(f"Инициализация репозитория: {self.project_dir}")

        # Загружаем конфиг
        config = FileHandler.load_config(CONFIG_PATH)
        name = config.get("default_name", "User")
        email = config.get("default_email", "user@example.com")

        # git init
        cmd, cwd = init.git_init(self.project_dir)
        success, out, err = self.executor.execute(cmd, cwd)
        if not success:
            error_msg = f"git init failed: {err}"
            logger.error(error_msg)
            return {"success": False, "error": err}
        logger.info("✅ git init — успешно")

        # .gitignore
        gitignore = self.project_dir / '.gitignore'
        if not gitignore.exists():
            gitignore.write_text(get_default_gitignore(), encoding='utf-8')
            logger.info("✅ .gitignore создан")

        # Настройка пользователя
        self._run_silent(["git", "config", "user.name", name])
        self._run_silent(["git", "config", "user.email", email])
        logger.info(f"✅ Настроены: {name} <{email}>")

        # Добавляем и коммитим всё
        cmd, cwd = add.git_add_files(['.'], self.project_dir)
        self.executor.execute(cmd, cwd)
        cmd, cwd = commit.git_commit("docs: initial commit", self.project_dir)
        self.executor.execute(cmd, cwd)
        logger.info("✅ Все файлы добавлены и закоммичены")

        # Привязка к удалённому репозиторию
        if repo_url.strip():
            cmd, cwd = remote.git_remote_add_origin(repo_url.strip(), self.project_dir)
            success, out, err = self.executor.execute(cmd, cwd)
            if success:
                logger.info(f"✅ Привязан к удалённому репозиторию: {repo_url}")
            else:
                logger.warning(f"⚠️ Не удалось привязать к репозиторию: {err}")

        return {"success": True}

    def get_status(self) -> list:
        cmd, cwd = status.git_status_porcelain(self.project_dir)
        success, stdout, stderr = self.executor.execute(cmd, cwd)
        if not success:
            error_msg = f"git status failed: {stderr}"
            logger.error(error_msg)
            return [f"Ошибка: {stderr}"]
        logger.info("✅ Статус обновлён")
        return stdout.split('\n') if stdout else []

    def commit_files(self, files: list, message: str) -> dict:
        # git add
        cmd, cwd = add.git_add_files(files, self.project_dir)
        success, out, err = self.executor.execute(cmd, cwd)
        if not success:
            logger.error(f"❌ git add failed: {err}")
            return {"success": False, "error": err}
        logger.info(f"✅ Добавлено файлов: {len(files)}")

        # git commit
        cmd, cwd = commit.git_commit(message, self.project_dir)
        success, out, err = self.executor.execute(cmd, cwd)
        if not success:
            logger.error(f"❌ git commit failed: {err}")
            return {"success": False, "error": err}
        logger.info(f"✅ Коммит: {message}")

        return {"success": True}

    def push(self) -> dict:
        cmd, cwd = push.git_push(self.project_dir)
        success, out, err = self.executor.execute(cmd, cwd)
        if not success:
            logger.error(f"❌ git push failed: {err}")
            return {"success": False, "error": err}
        logger.info("✅ git push — успешно")
        return {"success": True}

    def _run_silent(self, cmd: list):
        """Выполняет команду без логирования (для служебных операций)"""
        self.executor.execute(cmd, self.project_dir)