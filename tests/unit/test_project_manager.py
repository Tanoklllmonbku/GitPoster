# tests/unit/test_project_manager.py
import pytest
from unittest.mock import MagicMock
from pathlib import Path
from core import ProjectManager
from utils import get_logger

logger = get_logger("PyTests")

class MockExecutor:
    def execute(self, cmd, cwd):
        # Имитируем успешный результат
        return True, "", ""

def test_project_manager_init():
    pm = ProjectManager(Path("/test"), logger)
    assert pm.project_dir == Path("/test")

def test_is_git_repo(tmp_path, monkeypatch):
    pm = ProjectManager(tmp_path, logger)
    pm.executor = MockExecutor()
    # Просто проверяем, что метод не падает
    result = pm.is_git_repo()
    # В реальности — можно мокнуть результат
    assert isinstance(result, bool)

def test_initialize_calls_git_init(monkeypatch):
    mock_executor = MagicMock()
    mock_executor.execute.return_value = (True, "", "")

    with monkeypatch.context() as m:
        m.setattr("core.project_manager.GitExecutor", lambda: mock_executor)
        pm = ProjectManager(Path("/test"), logger)
        pm.executor = mock_executor
        result = pm.initialize("https://github.com/user/repo.git", "User", "user@example.com")

    assert result["success"]
    assert mock_executor.execute.called