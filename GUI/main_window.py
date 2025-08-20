# gui/main_window.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QLineEdit, QListWidget,
    QTabWidget, QMessageBox
)
from PyQt6.QtGui import QIcon
from core.project_manager import ProjectManager
from utils.logger import get_logger
from utils import FileHandler
from .Icons.import_icons import icon_path

logger = get_logger()

# 📁 Путь к конфигу
CONFIG_PATH = "config/user_config.json"


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.project_manager: ProjectManager = None
        self.setWindowIcon(QIcon(icon_path))
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Git Manager — Умный контроль версий")
        self.resize(700, 550)

        layout = QVBoxLayout()

        tab_widget = QTabWidget()
        main_tab = QWidget()
        init_tab = QWidget()

        # --- Основная вкладка ---
        main_layout = QVBoxLayout()
        self.path_label = QLabel("Папка не выбрана")
        btn_select = QPushButton("📁 Выбрать проект")
        btn_select.clicked.connect(self.select_folder)
        main_layout.addWidget(self.path_label)
        main_layout.addWidget(btn_select)

        self.status_label = QLabel("Git: не инициализирован")
        self.status_label.setStyleSheet("color: red;")
        main_layout.addWidget(self.status_label)

        main_layout.addWidget(QLabel("Изменённые файлы:"))
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        main_layout.addWidget(self.file_list)

        main_layout.addWidget(QLabel("Сообщение коммита:"))
        self.commit_msg = QLineEdit()
        self.commit_msg.setPlaceholderText("Например: feat: добавил GUI")
        main_layout.addWidget(self.commit_msg)

        btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("🔄 Обновить")
        self.btn_refresh.clicked.connect(self.refresh_status)
        self.btn_commit_only = QPushButton("💾 Commit")
        self.btn_commit_only.clicked.connect(lambda: self.commit_and_push(push=False))
        self.btn_commit_push = QPushButton("✅ Commit & Push")
        self.btn_commit_push.clicked.connect(lambda: self.commit_and_push(push=True))

        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_commit_only)
        btn_layout.addWidget(self.btn_commit_push)
        main_layout.addLayout(btn_layout)

        main_tab.setLayout(main_layout)

        # --- Вкладка: Инициализация ---
        init_layout = QVBoxLayout()
        init_layout.addWidget(QLabel("Ссылка на репозиторий (опционально):"))
        self.repo_url_input = QLineEdit()
        self.repo_url_input.setPlaceholderText("https://github.com/ваш-юзер/репозиторий.git")

        # ✅ Загружаем последнюю ссылку через FileHandler
        try:
            config = FileHandler.load_config(CONFIG_PATH)
            last_url = config.get("last_repo_url", "")
        except Exception as e:
            logger.warning(f"Не удалось загрузить конфиг: {e}")
            last_url = ""
        self.repo_url_input.setText(last_url)

        init_layout.addWidget(self.repo_url_input)

        self.btn_init = QPushButton("🚀 Инициализировать Git")
        self.btn_init.clicked.connect(self.initialize_git)
        init_layout.addWidget(self.btn_init)

        init_tab.setLayout(init_layout)
        tab_widget.addTab(main_tab, "Работа с Git")
        tab_widget.addTab(init_tab, "Инициализация")
        layout.addWidget(tab_widget)

        self.setLayout(layout)
        self.btn_commit_push.setEnabled(False)
        self.btn_commit_only.setEnabled(False)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку проекта")
        if folder:
            self.project_manager = ProjectManager(folder)
            self.path_label.setText(folder)
            self.refresh_status()

    def refresh_status(self):
        if not self.project_manager:
            logger.error("Папка проекта не выбрана")
            return

        if not self.project_manager.is_git_repo():
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

        status_lines = self.project_manager.get_status()
        self.file_list.clear()
        if not status_lines or (len(status_lines) == 1 and not status_lines[0]):
            self.file_list.addItem("Нет изменённых файлов")
        else:
            for line in status_lines:
                self.file_list.addItem(line)

    def initialize_git(self):
        if not self.project_manager:
            QMessageBox.critical(self, "Ошибка", "Выберите папку проекта")
            return

        repo_url = self.repo_url_input.text().strip()

        # ✅ Сохраняем URL через FileHandler
        if repo_url:
            try:
                FileHandler.save_config({"last_repo_url": repo_url}, CONFIG_PATH)
                logger.info(f"Конфиг сохранён: {repo_url}")
            except Exception as e:
                logger.error(f"Не удалось сохранить конфиг: {e}")

        result = self.project_manager.initialize(repo_url)

        if result["success"]:
            QMessageBox.information(self, "Готово", "Репозиторий инициализирован!")
            logger.info("Репозиторий инициализирован успешно")
            self.refresh_status()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось инициализировать репозиторий")
            logger.error("Ошибка инициализации репозитория")

    def commit_and_push(self, push: bool):
        if not self.project_manager:
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

        files_to_commit = []
        for item in selected_items:
            text = item.text().strip()
            if text.startswith(("A ", "M ", "D ", "??")):
                filename = text.split(" ", 1)[1]
                files_to_commit.append(filename)

        result = self.project_manager.commit_files(files_to_commit, msg)
        if not result["success"]:
            QMessageBox.critical(self, "Ошибка", f"Ошибка коммита:\n{result['error']}")
            return

        if push:
            result = self.project_manager.push()
            if not result["success"]:
                QMessageBox.critical(self, "Ошибка", f"Ошибка push:\n{result['error']}")
                return

        QMessageBox.information(self, "Готово", "Коммит выполнен!")
        self.refresh_status()