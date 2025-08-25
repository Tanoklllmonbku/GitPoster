# tests/conf_test.py
import pytest
import os
import subprocess

@pytest.fixture(autouse=True)
def ensure_git_available():
    result = subprocess.run(["git", "--version"], capture_output=True)
    if result.returncode != 0:
        pytest.skip("Git not available")