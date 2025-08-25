# tests/integration/test_git_flow.py
import pytest
import subprocess
import shutil
from pathlib import Path
from core.project_manager import ProjectManager
from utils import FileHandler
from utils import get_logger

logger = get_logger("PyIntregrTests")

@pytest.fixture
def temp_repo(tmp_path):
    repo_dir = tmp_path / "test_repo"
    repo_dir.mkdir()
    return repo_dir

@pytest.fixture
def remote_repo(tmp_path):
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", str(remote)], check=True)
    return remote

def test_full_git_initialization_flow(temp_repo, remote_repo):
    # Создаём локальный репозиторий через ProjectManager
    pm = ProjectManager(temp_repo, logger)

    # URL в формате file:// для теста
    remote_url = f"file://{remote_repo}"

    result = pm.initialize(
        repo_url=remote_url,
        name="Test User",
        email="test@example.com"
    )

    assert result["success"]

    # Проверим, что push прошёл
    remote_count = subprocess.run(
        ["git", "ls-remote", str(remote_repo), "main"],
        capture_output=True,
        text=True
    )
    assert "main" in remote_count.stdout