# tests/unit/test_project_manager.py
import pytest
from unittest.mock import MagicMock
from pathlib import Path
from core.project_manager import ProjectManager
from utils.logger import get_logger

def test_initialize_calls_git_init(tmp_path):
    mock_executor = MagicMock()
    mock_executor.execute.return_value = (True, "", "")

    with pytest.MonkeyPatch().context() as m:
        m.setattr("core.project_manager.GitExecutor", lambda: mock_executor)

        # Создаём ProjectManager во временной папке
        pm = ProjectManager(tmp_path, logger=get_logger("UnitTests"))
        pm.executor = mock_executor

        result = pm.initialize(
            repo_url="https://github.com/user/repo.git",
            name="User",
            email="user@example.com"
        )

    assert result["success"]