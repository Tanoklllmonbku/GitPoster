# tests/unit/test_project_manager.py
import pytest
from unittest.mock import MagicMock
from core.project_manager import ProjectManager
from utils.logger import get_logger

# Создаём тестовый логгер
logger = get_logger("Tests")


def test_project_manager_init(tmp_path):
    pm = ProjectManager(tmp_path, logger=logger)
    assert pm.project_dir == tmp_path


def test_initialize_calls_git_init(tmp_path):
    # Используем временную папку
    mock_executor = MagicMock()
    mock_executor.execute.return_value = (True, "", "")

    # Подменяем GitExecutor
    with pytest.MonkeyPatch().context() as m:
        m.setattr("core.project_manager.GitExecutor", lambda: mock_executor)

        # Создаём ProjectManager в реальной существующей папке
        pm = ProjectManager(tmp_path, logger=logger)
        pm.executor = mock_executor

        # Выполняем инициализацию
        result = pm.initialize(
            repo_url="https://github.com/user/repo.git",
            name="User",
            email="user@example.com"
        )

    # Проверяем, что всё прошло без ошибок
    assert result["success"]

    # Проверяем, что README.md создан
    readme_path = tmp_path / "README.md"
    assert readme_path.exists()
    assert readme_path.read_text(encoding='utf-8').startswith("# ")

    # Проверяем, что git init был вызван
    mock_executor.execute.assert_called()