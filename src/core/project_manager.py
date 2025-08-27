# core/project_manager.py
import subprocess
import os
from pathlib import Path
import logging

from .commands import push, commit, init, remote, add, status
from .git_exec import GitExecutor
from src.utils import create_gitignore

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

    def __init__(self, project_dir: Path, logger: logging.Logger):
        self.project_dir = Path(project_dir)
        self.executor = GitExecutor()
        self.logger = logger

    def is_git_repo(self) -> bool:
        cmd, cwd = status.git_status_porcelain(self.project_dir)
        success, _, _ = self.executor.execute(cmd, cwd)
        return success

    def initialize(self, repo_url: str, name: str, email: str) -> dict:
        self.logger.info(f"Инициализация репозитория: {self.project_dir}")

        # 1. git init
        cmd, cwd = init.git_init(self.project_dir)
        success, out, err = self.executor.execute(cmd, cwd)
        if not success:
            self.logger.error(f"❌ git init failed: {err}")
            return {"success": False, "error": err}
        self.logger.info("✅ git init — успешно")

        # 2. Создаём README.md
        readme_path = self.project_dir / "README.md"
        if not readme_path.exists():
            readme_path.write_text("# " + self.project_dir.name, encoding='utf-8')
            self.logger.info("✅ README.md создан")

        # 3. Создаём .gitignore
        gitignore_path = self.project_dir / ".gitignore"
        print(gitignore_path, self.project_dir)
        if not gitignore_path.exists():
            create_gitignore(gitignore_path)
            self.logger.info("✅ .gitignore создан")

        # 4. Настройка пользователя
        self._run_silent(["git", "config", "user.name", name])
        self._run_silent(["git", "config", "user.email", email])
        self.logger.info(f"✅ Настроены: {name} <{email}>")

        # 5. git add README.md
        cmd, cwd = add.git_add_files(["README.md"], self.project_dir)
        success, out, err = self.executor.execute(cmd, cwd)
        if not success:
            self.logger.error(f"❌ git add failed: {err}")
            return {"success": False, "error": err}
        self.logger.info("✅ README.md добавлен")

        # 6. git commit
        cmd, cwd = commit.git_commit("first commit", self.project_dir)
        success, out, err = self.executor.execute(cmd, cwd)
        if not success:
            self.logger.error(f"❌ git commit failed: {err}")
            return {"success": False, "error": err}
        self.logger.info("✅ Коммит: first commit")

        # 7. git branch -M main
        cmd, cwd = ["git", "branch", "-M", "main"], self.project_dir
        success, out, err = self.executor.execute(cmd, cwd)
        if not success:
            self.logger.error(f"❌ git branch -M main failed: {err}")
            return {"success": False, "error": err}
        self.logger.info("✅ Ветка переименована в main")

        # 8. git remote add origin {url}
        if repo_url.strip():
            cmd, cwd = remote.git_remote_add_origin(repo_url.strip(), self.project_dir)
            success, out, err = self.executor.execute(cmd, cwd)
            if not success:
                self.logger.warning(f"⚠️ Не удалось добавить remote: {err}")
            else:
                self.logger.info(f"✅ Привязан к: {repo_url}")

        # 9. git push -u origin main
        if repo_url.strip():
            cmd, cwd = ["git", "push", "-u", "origin", "main"], self.project_dir
            success, out, err = self.executor.execute(cmd, cwd)
            if not success:
                self.logger.error(f"❌ git push failed: {err}")
                return {"success": False, "error": err}
            self.logger.info("✅ Первая загрузка на GitHub — успешна")

        return {"success": True}
    def get_status(self) -> list:
        cmd, cwd = status.git_status_porcelain(self.project_dir)
        success, stdout, stderr = self.executor.execute(cmd, cwd)
        if not success:
            error_msg = f"git status failed: {stderr}"
            self.logger.error(error_msg)
            return [f"Ошибка: {stderr}"]
        self.logger.info("✅ Статус обновлён")
        return stdout.split('\n') if stdout else []

    def commit_files(self, files: list, message: str) -> dict:
        # git add
        cmd, cwd = add.git_add_files(files, self.project_dir)
        success, out, err = self.executor.execute(cmd, cwd)
        if not success:
            self.logger.error(f"❌ git add failed: {err}")
            return {"success": False, "error": err}
        self.logger.info(f"✅ Добавлено файлов: {len(files)}")

        # git commit
        cmd, cwd = commit.git_commit(message, self.project_dir)
        success, out, err = self.executor.execute(cmd, cwd)
        if not success:
            self.logger.error(f"❌ git commit failed: {err}")
            return {"success": False, "error": err}
        self.logger.info(f"✅ Коммит: {message}")

        return {"success": True}

    def push(self) -> dict:
        cmd, cwd = push.git_push(self.project_dir)
        success, out, err = self.executor.execute(cmd, cwd)
        if not success:
            self.logger.error(f"❌ git push failed: {err}")
            return {"success": False, "error": err}
        self.logger.info("✅ git push — успешно")
        return {"success": True}

    def _run_silent(self, cmd: list):
        """Выполняет команду без логирования (для служебных операций)"""
        self.executor.execute(cmd, self.project_dir)