# Комманды для запуска тестов

````bash
# Установка зависимостей
pip install pytest pytest-mock
# Активация .venv
.venv\Scripts\activate.bat
# Запустить все тесты
python -m pytest

# Только юнит-тесты
python -m pytest tests/unit/

# Только интеграционные
python -m pytest tests/integration/
````