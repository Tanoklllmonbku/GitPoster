# tests/unit/test_file_handler.py
import pytest
import os
from utils import FileHandler
from pathlib import Path

def test_save_and_load_json(tmp_path):
    data = {"name": "Test", "value": 42}
    filepath = tmp_path / "test.json"

    FileHandler.save_config(data, str(filepath))
    loaded = FileHandler.load_config(str(filepath))

    assert loaded == data

def test_load_json_file_not_found():
    with pytest.raises(FileNotFoundError):
        FileHandler.load_config("nonexistent.json")

def test_load_json_invalid_json(tmp_path):
    filepath = tmp_path / "broken.json"
    filepath.write_text("{invalid json}", encoding="utf-8")
    with pytest.raises(ValueError):
        FileHandler.load_config(str(filepath))