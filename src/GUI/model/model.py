from pathlib import Path
import logging

from src.core.git_exec import GitExecutor
from src.utils import create_gitignore

from src.core.commands.BaseCommands import *
from src.core.commands import return_base_command

CONFIG_PATH = "config/user_config.json"


class ProjectManagerModel:
    """Managing Git-project"""
    command_name: str

    def __init__(self, project_dir: Path, logger: logging.Logger):
        self.project_dir = Path(project_dir)
        self.executor = GitExecutor()
        self.logger = logger

    def add(self, files:list):
        self.logger.debug("Adding files")
        cmd, cwd = return_base_command("add", {"files": files, "cwd": self.project_dir})
        success, out, err = self.executor.execute(cmd, cwd)
        if not success:
            self.logger.error(f"git add failed: {err}")
            return {"success": False, "error": err}

    def clone(self, url):
        cmd, cwd = return_base_command("clone", {"url": url, "cwd": self.project_dir})
        success, out, err = self.executor.execute(cmd, cwd)
        if not success:
            self.logger.error(f"git clone failed: {err}")
            return {"success": False, "error": err}
        self.logger.info(f"Cloned repository from: {url}")

    def commit(self, message):
        pass

    # def is_git_repo(self) -> bool:
    #     self.logger.info(f"Getting status of repository in: {self.project_dir}")
    #     cmd, cwd = return_base_command("status", {"cwd": self.project_dir})
    #     success, _, _ = self.executor.execute(cmd, cwd)
    #     return success
    #
    # def initialize(self, repo_url: str, name: str, email: str) -> dict:
    #     self.logger.info(f"Инициализация репозитория: {self.project_dir}")
    #     cmd, cwd = return_base_command("init", {"cwd": self.project_dir})
    #     success, out, err = self.executor.execute(cmd, cwd)
    #     if not success:
    #         self.logger.error(f"❌ git init failed: {err}")
    #         return {"success": False, "error": err}
    #     self.logger.info("✅ git init — успешно")
    #
    #     readme_path = self.project_dir / "README.md"
    #     if not readme_path.exists():
    #         readme_path.write_text("# " + self.project_dir.name, encoding='utf-8')
    #         self.logger.info("✅ README.md создан")
    #
    #     gitignore_path = self.project_dir / ".gitignore"
    #     print(gitignore_path, self.project_dir)
    #     if not gitignore_path.exists():
    #         create_gitignore(gitignore_path)
    #         self.logger.info("✅ .gitignore создан")
    #
    #     self._run_silent(["git", "config", "user.name", name])
    #     self._run_silent(["git", "config", "user.email", email])
    #     self.logger.info(f"✅ Настроены: {name} <{email}>")
    #
    #     cmd, cwd = return_base_command("add", {"cwd": self.project_dir, "files": ["README.md"]})
    #     success, out, err = self.executor.execute(cmd, cwd)
    #     if not success:
    #         self.logger.error(f"❌ git add failed: {err}")
    #         return {"success": False, "error": err}
    #     self.logger.info("✅ README.md добавлен")
    #
    #     cmd, cwd = return_base_command("commit", {"message": "first commit","cwd": self.project_dir})
    #     success, out, err = self.executor.execute(cmd, cwd)
    #     if not success:
    #         self.logger.error(f"❌ git commit failed: {err}")
    #         return {"success": False, "error": err}
    #     self.logger.info("✅ Коммит: first commit")
    #
    #     cmd, cwd = ["git", "branch", "-M", "main"], self.project_dir
    #     success, out, err = self.executor.execute(cmd, cwd)
    #     if not success:
    #         self.logger.error(f"❌ git branch -M main failed: {err}")
    #         return {"success": False, "error": err}
    #     self.logger.info("✅ Ветка переименована в main")
    #
    #     if repo_url.strip():
    #         cmd, cwd = return_base_command("remote_add_origin", {"url": repo_url.strip(),"cwd": self.project_dir})
    #         success, out, err = self.executor.execute(cmd, cwd)
    #         if not success:
    #             self.logger.warning(f"⚠️ Не удалось добавить remote: {err}")
    #         else:
    #             self.logger.info(f"✅ Привязан к: {repo_url}")
    #
    #     if repo_url.strip():
    #         cmd, cwd = ["git", "push", "-u", "origin", "main"], self.project_dir
    #         success, out, err = self.executor.execute(cmd, cwd)
    #         if not success:
    #             self.logger.error(f"❌ git push failed: {err}")
    #             return {"success": False, "error": err}
    #         self.logger.info("✅ Первая загрузка на GitHub — успешна")
    #
    #     return {"success": True}
    # def get_status(self) -> list:
    #     cmd, cwd = return_base_command("status", {"cwd": self.project_dir})
    #     success, stdout, stderr = self.executor.execute(cmd, cwd)
    #     if not success:
    #         error_msg = f"git status failed: {stderr}"
    #         self.logger.error(error_msg)
    #         return [f"Ошибка: {stderr}"]
    #     self.logger.info("✅ Статус обновлён")
    #     return stdout.split('\n') if stdout else []
    #
    # def commit_files(self, files: list, message: str) -> dict:
    #     # git add
    #     cmd, cwd = return_base_command("add", {"files": files, "cwd": self.project_dir})
    #     success, out, err = self.executor.execute(cmd, cwd)
    #     if not success:
    #         self.logger.error(f"❌ git add failed: {err}")
    #         return {"success": False, "error": err}
    #     self.logger.info(f"✅ Добавлено файлов: {len(files)}")
    #
    #     # git commit
    #     cmd, cwd = return_base_command("commit", {"message": message, "cwd": self.project_dir})
    #     success, out, err = self.executor.execute(cmd, cwd)
    #     if not success:
    #         self.logger.error(f"❌ git commit failed: {err}")
    #         return {"success": False, "error": err}
    #     self.logger.info(f"✅ Коммит: {message}")
    #
    #     return {"success": True}
    #
    # def push(self) -> dict:
    #     cmd, cwd = return_base_command("push", {"cwd": self.project_dir})
    #     success, out, err = self.executor.execute(cmd, cwd)
    #     if not success:
    #         self.logger.error(f"❌ git push failed: {err}")
    #         return {"success": False, "error": err}
    #     self.logger.info("✅ git push — успешно")
    #     return {"success": True}
    #
    # def _run_silent(self, cmd: list):
    #     """Выполняет команду без логирования (для служебных операций)"""
    #     self.executor.execute(cmd, self.project_dir)