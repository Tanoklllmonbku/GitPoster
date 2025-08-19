# gui/git_manager.py
import subprocess
from pathlib import Path
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QFileDialog, QLineEdit,
    QListWidget, QMessageBox, QTabWidget
)

from GUI.Icons.import_icons import icon_path

class GitManager(QWidget):
    def __init__(self):
        super().__init__()
        self.project_dir = None
        self.setWindowIcon(QIcon(icon_path))
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Git Manager — Умный контроль версий")
        self.resize(700, 550)

        layout = QVBoxLayout()

        # --- Tab 1: Основное управление ---
        tab_widget = QTabWidget()
        main_tab = QWidget()
        init_tab = QWidget()

        # --- Основная вкладка ---
        main_layout = QVBoxLayout()

        # Выбор папки
        path_layout = QHBoxLayout()
        self.path_label = QLabel("Папка не выбрана")
        btn_select = QPushButton("📁 Выбрать проект")
        btn_select.clicked.connect(self.select_folder)
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(btn_select)
        main_layout.addLayout(path_layout)

        # Статус
        self.status_label = QLabel("Git: не инициализирован")
        self.status_label.setStyleSheet("color: red;")
        main_layout.addWidget(self.status_label)

        # Изменённые файлы
        main_layout.addWidget(QLabel("Изменённые файлы:"))
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        main_layout.addWidget(self.file_list)

        # Сообщение коммита
        main_layout.addWidget(QLabel("Сообщение коммита:"))
        self.commit_msg = QLineEdit()
        self.commit_msg.setPlaceholderText("Например: feat: добавил GUI для диаграмм")
        main_layout.addWidget(self.commit_msg)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("🔄 Обновить статус")
        self.btn_refresh.clicked.connect(self.refresh_status)
        self.btn_commit_push = QPushButton("✅ Commit & Push")
        self.btn_commit_push.clicked.connect(lambda: self.commit_and_push())
        self.btn_commit_only = QPushButton("💾 Commit (без push)")
        self.btn_commit_only.clicked.connect(lambda: self.commit_and_push(push=False))

        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_commit_only)
        btn_layout.addWidget(self.btn_commit_push)
        main_layout.addLayout(btn_layout)

        # Лог
        main_layout.addWidget(QLabel("Лог:"))
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        main_layout.addWidget(self.log)

        main_tab.setLayout(main_layout)

        # --- Вкладка: Инициализация ---
        init_layout = QVBoxLayout()

        init_layout.addWidget(QLabel("Имя:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ваше имя")
        init_layout.addWidget(self.name_input)

        init_layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ваш email")
        init_layout.addWidget(self.email_input)

        self.btn_init = QPushButton("🚀 Инициализировать Git")
        self.btn_init.clicked.connect(self.initialize_git)
        init_layout.addWidget(self.btn_init)

        init_tab.setLayout(init_layout)

        # --- Добавляем вкладки ---
        tab_widget.addTab(main_tab, "Работа с Git")
        tab_widget.addTab(init_tab, "Инициализация")
        layout.addWidget(tab_widget)

        self.setLayout(layout)

        # --- Инициализация ---
        self.btn_commit_push.setEnabled(False)
        self.btn_commit_only.setEnabled(False)

    def log_message(self, text, level="info"):
        prefix = {"info": "✅", "warning": "⚠️", "error": "❌"}.get(level, "📌")
        self.log.append(f"{prefix} {text}")

    def run_command(self, cmd, cwd=None):
        if not cwd:
            cwd = self.project_dir
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                cwd=cwd
            )
            success = result.returncode == 0
            return success, result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            return False, "", str(e)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку проекта")
        if folder:
            self.project_dir = Path(folder)
            self.path_label.setText(str(self.project_dir))
            self.refresh_status()

    def refresh_status(self):
        if not self.project_dir:
            self.log_message("❌ Папка не выбрана", "error")
            return

        # Проверяем, Git ли это
        success, _, _ = self.run_command(['git', 'rev-parse', '--is-inside-work-tree'], cwd=self.project_dir)
        if not success:
            self.status_label.setText("Git: не инициализирован")
            self.status_label.setStyleSheet("color: red;")
            self.btn_commit_push.setEnabled(False)
            self.btn_commit_only.setEnabled(False)
            self.file_list.clear()
            self.file_list.addItem("Репозиторий не инициализирован. Перейдите на вкладку 'Инициализация'")
            return

        self.status_label.setText("Git: инициализирован")
        self.status_label.setStyleSheet("color: green;")
        self.btn_commit_push.setEnabled(True)
        self.btn_commit_only.setEnabled(True)

        # Получаем статус
        success, stdout, stderr = self.run_command(['git', 'status', '--porcelain'], cwd=self.project_dir)
        if not success:
            self.log_message(f"❌ Ошибка Git: {stderr}", "error")
            return

        self.file_list.clear()
        if not stdout.strip():
            self.file_list.addItem("Нет изменённых файлов")
            return

        for line in stdout.strip().split('\n'):
            self.file_list.addItem(line)

    def initialize_git(self):
        if not self.project_dir:
            QMessageBox.critical(self, "Ошибка", "Выберите папку проекта")
            return

        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        if not name or not email:
            QMessageBox.warning(self, "Внимание", "Введите имя и email")
            return

        if (self.project_dir / '.git').exists():
            QMessageBox.warning(self, "Внимание", "Репозиторий уже инициализирован")
            return

        self.log.clear()
        self.log_message(f"Инициализация в: {self.project_dir}")

        # git init
        success, out, err = self.run_command(['git', 'init'])
        if not success:
            self.log_message(f"❌ Ошибка: {err}", "error")
            return
        self.log_message("✅ git init — успешно")

        # .gitignore
        gitignore = self.project_dir / '.gitignore'
        if not gitignore.exists():
            with open(gitignore, 'w', encoding='utf-8') as f:
                f.write(self.get_default_gitignore())
            self.log_message("✅ .gitignore создан")

        # Настройка пользователя
        self.run_command(['git', 'config', 'user.name', name])
        self.run_command(['git', 'config', 'user.email', email])
        self.log_message("✅ Настроены user.name и user.email")

        # Добавляем и коммитим
        self.run_command(['git', 'add', '.'])
        self.run_command(['git', 'commit', '-m', 'docs: initial commit with project structure'])

        self.log_message("🎉 Репозиторий инициализирован!")
        QMessageBox.information(self, "Готово", "Репозиторий инициализирован. Перейдите на вкладку 'Работа с Git'")

        self.refresh_status()

    def get_default_gitignore(self):
        return """
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.py[cod]
*$py.class
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg
.pytest_cache/
.coverage
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pyre/
.pytype/
.coverage.*
.cache
.pytest_cache

# Виртуальные окружения
venv/
env/
.venv/
ENV/
.ENV/

# Логи
logs/
*.log
.DS_Store
.DS_Store?

# Jupyter
.ipynb_checkpoints/
*.ipynb.gz

# PyInstaller
/dist/
/build/
*.spec

# IDE
.idea/
.vscode/
*.swp
*.swo

# Системные
Thumbs.db
.DS_Store
        """.strip()

    def commit_and_push(self, push=True):
        if not self.project_dir:
            QMessageBox.critical(self, "Ошибка", "Выберите папку проекта")
            return

        msg = self.commit_msg.text().strip()
        if not msg:
            QMessageBox.warning(self, "Внимание", "Введите сообщение коммита")
            return

        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Внимание", "Выберите файлы для коммита")
            return

        # Извлекаем имена файлов из строк вида "M file.py"
        files_to_commit = []
        for item in selected_items:
            text = item.text().strip()
            if text.startswith(("A ", "M ", "D ", "??")):
                filename = text.split(" ", 1)[1]
                files_to_commit.append(filename)

        self.log.clear()
        self.log_message("🔄 Выполняю...")

        # git add выбранных файлов
        success, out, err = self.run_command(['git', 'add'] + files_to_commit)
        if not success:
            self.log_message(f"❌ Ошибка git add: {err}", "error")
            return
        self.log_message(f"✅ Добавлено файлов: {len(files_to_commit)}")

        # git commit
        success, out, err = self.run_command(['git', 'commit', '-m', msg])
        if not success:
            self.log_message(f"❌ Ошибка коммита: {err}", "error")
            return
        self.log_message(f"✅ Коммит: {msg}")

        # git push
        if push:
            success, out, err = self.run_command(['git', 'push'])
            if not success:
                self.log_message(f"❌ Ошибка push: {err}", "error")
                return
            self.log_message("✅ git push")
        else:
            self.log_message("ℹ️ Push пропущен")

        self.log_message("🎉 Готово!")
        self.refresh_status()


def main():
    app = QApplication([])
    window = GitManager()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()