#utils/file_handler.py
import json
import os
from typing import Any, Dict


class FileHandler:
    """Универсальный обработчик файлов"""
    @staticmethod
    def save_config(data: Dict[str, Any], filepath: str):
        """Сохранение в JSON"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def load_config(filepath: str) -> Dict[str, Any]:
        """Загрузка из JSON с обработкой ошибок"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {filepath}: {e}")