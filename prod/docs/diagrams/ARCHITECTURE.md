
# 🏗️ Архитектура GitManager

Документ описывает структуру и принципы работы приложения `GitManager` — графического инструмента для управления Git без знания терминала.

---

## 🧩 Общая архитектура

`GitManager` построен по принципу **чистой архитектуры (Clean Architecture)** с чётким разделением ответственности:

- +------------------+
- | GUI | ← Представление (View)
- +------------------+
- ↓
- +------------------+
- | Core / API | ← Бизнес-логика (Controller)
- +------------------+
- ↓
- +------------------+
- | Commands | ← Git-команды как данные
- +------------------+
- ↓
- +------------------+
- | subprocess | ← Внешняя система (Git CLI)
- +------------------+

---
## 📁 Структура проекта
- gitposter/
- │
- ├── src/                    ← Исходный код
- │   ├── core/
- │   │   ├── project_manager.py
- │   │   ├── git_executor.py
- │   │   └── environment.py
- │   ├── commands/
- │   │   ├── init.py
- │   │   ├── status.py
- │   │   ├── commit.py
- │   │   ├── add.py
- │   │   ├── push.py
- │   │   ├── remote.py
- │   │   └── __init__.py
- │   ├── GUI/
- │   │   ├── main_window.py
- │   │   └── Icons
- │   │   │   ├── import_icons.py
- │   │   │   └── icon.ico
- │   ├── utils/
- │   │   ├── logger.py
- │   │   ├── gitignore_temp.py
- │   │   └── file_handler.py
- │   ├── config/
- │   │   └── template.json     
- │   └── app.py                
- │
- ├── dev/                    ← Инструменты разработки и тестирования
- │   ├── tests/
- │   │   ├── unit/
- │   │   ├── integration/
- │   │   └── e2e/
- │   ├── scripts/
- │   │   ├── build_dev.py      
- │   │   └── test_runner.py
- │   ├── requirements.txt
- │   └── .gitignore
- │
- ├── prod/                   ← Готовые продукты для пользователей
- │   ├── dist/
- │   │   └── GitPoster.exe 
- │   ├── installer/
- │   │   ├── GitPoster_Setup.exe
- │   │   └── portable/
- │   │       └── git/          ← вшитый PortableGit
- │   ├── docs/
- │   │   ├── USER_GUIDE.md     ← инструкция для пользователя
- │   │   └── screenshots/
- │   └── releases/             ← релизы (v0.2, v0.3...)
- │       ├── GitPoster_v0.2.exe
- │       └── GitPoster_v0.2_Setup.exe
- │
- ├── embedded/               ← Ресурсы для встраивания (одинаковы для dev/prod)
- │   ├── portable_git.7z
- │   └── config_template.json
- │
- ├── old_exe/
- │   ├── V0.2....
- ├── logs/                   ← Логи (runtime, .gitignore)
- │
- ├── config/                 ← Конфигурация (runtime, .gitignore)
- │
- └── pyproject.toml          ← метаданные, зависимости (вместо requirements.txt)
---
## 🧠 Ключевые принципы

### 1. **Единая точка инициализации**
- Логгер создаётся **только в `app.py`**
- Передаётся по цепочке в `MainWindow` → `ProjectManager`
- Исключает дублирование хендлеров

### 2. **Команды как данные**
- Каждая Git-команда — функция, возвращающая `(cmd, cwd)`
- Позволяет тестировать логику без вызова `subprocess`

### 3. **Иммутабельность конфигурации**
- Конфиг (`config/user_config.json`) загружается один раз при старте
- Изменяется только через `SettingsDialog`
- Сохраняется через `FileHandler.save_json`

### 4. **Безопасность GUI**
- `subprocess` запускается с `startupinfo` — **окно консоли не появляется**
- Все пути нормализуются и валидируются
- Игнорируемые файлы (`__pycache__`, `.pyc`) фильтруются

---

## 🔗 Поток управления

1. Пользователь выбирает папку проекта
2. `MainWindow` создаёт `ProjectManager(project_dir, logger)`
3. При действии (например, "Commit") вызывается:
   - `ProjectManager.commit_files(files, msg)`
   - → `git add` + `git commit`
4. Результат логируется и отображается в GUI
5. При `push`:
   - Сначала `git pull` (если нужно)
   - Затем `git push`

---

## 📦 Зависимости

- **PyQt6** — GUI
- **Python 3.10+** — основной интерпретатор
- **Git CLI** — внешняя зависимость (должна быть в `PATH`)

> ⚠️ Приложение **не заменяет Git**, а **является обёрткой** вокруг `git` команд.

---

## 🧪 Тестируемость

- `ProjectManager` можно тестировать без GUI
- `commands/*.py` — чистые функции, легко мокать
- Логгер можно заменить на `MockLogger` в тестах

---

## 📈 Планы на будущее

- Поддержка веток (`git branch`, `git checkout`)
- Интеграция с `git stash`
- Поддержка SSH-ключей
- Автообновление
- Поддержка `git clone`