# gui/initialize_git_window.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog, QMessageBox
)
import os
import json
from src.core import ProjectManager
from src.utils import get_logger, FileHandler


class InitializeWindow(QWidget):
    def __init__(self, main_window, logger):
        super().__init__()
        self.main_window = main_window
        self.logger = logger
        self.current_config_path = None
        self.setup_ui()
        self.load_main_config_if_exists()

    def setup_ui(self):
        """Создаёт интерфейс окна инициализации"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Поля ввода
        self.setup_config_controls(layout)
        self.setup_git_fields(layout)
        self.setup_init_button(layout)

        self.setLayout(layout)

    def setup_config_controls(self, parent_layout):
        """Контролы для управления конфигурацией"""
        config_layout = QHBoxLayout()

        self.btn_select_config = QPushButton("📁 Выбрать")
        self.btn_select_config.setMinimumHeight(40)
        self.btn_select_config.clicked.connect(self.select_config)
        config_layout.addWidget(self.btn_select_config)

        self.btn_create_config = QPushButton("🆕 Создать")
        self.btn_create_config.setMinimumHeight(40)
        self.btn_create_config.clicked.connect(self.create_config)
        config_layout.addWidget(self.btn_create_config)

        self.btn_set_main = QPushButton("⭐ Основной")
        self.btn_set_main.setMinimumHeight(40)
        self.btn_set_main.setEnabled(False)
        self.btn_set_main.clicked.connect(self.set_main_config)
        config_layout.addWidget(self.btn_set_main)

        parent_layout.addLayout(config_layout)

        # Статус конфига
        self.config_status = QLabel("Конфигурация не выбрана")
        self.config_status.setStyleSheet("color: #E53E3E; font-style: italic;")
        parent_layout.addWidget(self.config_status)

    def setup_git_fields(self, parent_layout):
        """Поля для настроек Git"""
        # Имя
        parent_layout.addWidget(QLabel("Имя:", styleSheet="font-weight: bold;"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ваше имя (для Git)")
        self.name_input.setMinimumHeight(40)
        parent_layout.addWidget(self.name_input)

        # Email
        parent_layout.addWidget(QLabel("Email:", styleSheet="font-weight: bold;"))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ваш email (для Git)")
        self.email_input.setMinimumHeight(40)
        parent_layout.addWidget(self.email_input)

        # URL репозитория
        parent_layout.addWidget(QLabel("Ссылка на репозиторий:", styleSheet="font-weight: bold;"))
        self.repo_url_input = QLineEdit()
        self.repo_url_input.setPlaceholderText("https://github.com/user/repo.git")
        self.repo_url_input.setMinimumHeight(40)
        parent_layout.addWidget(self.repo_url_input)

    def setup_init_button(self, parent_layout):
        """Кнопка инициализации"""
        self.btn_init = QPushButton("🚀 Инициализировать Git")
        self.btn_init.setMinimumHeight(50)
        self.btn_init.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.btn_init.clicked.connect(self.initialize_git)
        parent_layout.addWidget(self.btn_init)

    def get_main_config_path_file(self):
        """Возвращает путь к файлу основного конфига"""
        appdata = os.getenv('APPDATA') or os.path.expanduser('~/.config')
        config_dir = os.path.join(appdata, "GitPoster")
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "main_config_path.json")

    def load_main_config_if_exists(self):
        """Загружает основной конфиг при старте"""
        main_config_file = self.get_main_config_path_file()

        if not os.path.exists(main_config_file):
            return

        try:
            with open(main_config_file, 'r') as f:
                data = json.load(f)
                main_path = data.get("main_config_path", "")

            if os.path.exists(main_path):
                self.load_config(main_path)
                self.current_config_path = main_path
                self.btn_set_main.setEnabled(False)
                self.logger.info(f"Загружен основной конфиг: {main_path}")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки основного конфига: {e}")

    def select_config(self):
        """Выбор существующего конфига"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите конфигурационный файл",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if not file_path:
            return

        try:
            self.load_config(file_path)
            self.current_config_path = file_path
            self.btn_set_main.setEnabled(True)
            self.logger.info(f"Конфиг выбран: {file_path}")
        except Exception as e:
            self.logger.error(f"Не удалось загрузить конфиг: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить конфиг:\n{str(e)}")

    def create_config(self):
        """Создание нового конфига"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Создать конфигурацию",
            "",
            "JSON Files (*.json)"
        )

        if not file_path:
            return

        default_config = {
            "user.name": "",
            "user.email": "",
            "last_repo_url": ""
        }

        try:
            FileHandler.save_config(default_config, file_path)
            self.load_config(file_path)
            self.current_config_path = file_path
            self.btn_set_main.setEnabled(True)
            self.logger.info(f"Новый конфиг создан: {file_path}")
        except Exception as e:
            self.logger.error(f"Не удалось создать конфиг: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать конфиг:\n{str(e)}")

    def set_main_config(self):
        """Установка текущего конфига как основного"""
        if not self.current_config_path:
            QMessageBox.warning(self, "Внимание", "Сначала выберите или создайте конфиг")
            return

        try:
            main_config_file = self.get_main_config_path_file()
            with open(main_config_file, 'w') as f:
                json.dump({"main_config_path": self.current_config_path}, f, indent=2)

            self.btn_set_main.setEnabled(False)
            self.logger.info(f"Основной конфиг установлен: {self.current_config_path}")
            QMessageBox.information(self, "Готово", "Конфиг установлен как основной")
        except Exception as e:
            self.logger.error(f"Ошибка установки основного конфига: {e}")
            QMessageBox.critical(self, "Ошибка", "Не удалось установить основной конфиг")

    def load_config(self, config_path):
        """Загрузка конфига в интерфейс"""
        try:
            config = FileHandler.load_config(config_path)

            # Валидация обязательных полей
            required = {"user.name", "user.email", "last_repo_url"}
            if not all(k in config for k in required):
                raise ValueError("Конфиг повреждён: отсутствуют обязательные поля")

            # Загрузка значений
            self.name_input.setText(config["user.name"])
            self.email_input.setText(config["user.email"])
            self.repo_url_input.setText(config["last_repo_url"])

            # Обновление статуса
            self.config_status.setText(f"Конфиг: {os.path.basename(config_path)}")
            self.config_status.setStyleSheet("color: #38A169; font-weight: bold;")
            self.current_config_path = config_path

        except Exception as e:
            self.config_status.setText(f"Ошибка: {str(e)}")
            self.config_status.setStyleSheet("color: #E53E3E; font-weight: bold;")
            raise

    def initialize_git(self):
        """Инициализация репозитория"""
        if not self.current_config_path:
            QMessageBox.warning(self, "Внимание", "Сначала выберите или создайте конфиг")
            return

        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        repo_url = self.repo_url_input.text().strip()

        if not name or not email:
            QMessageBox.warning(self, "Внимание", "Введите имя и email")
            return

        # Получаем путь к проекту из основного окна
        project_path = self.main_window.git_work_window.path_label.text()
        if project_path == "Папка не выбрана" or not os.path.exists(project_path):
            QMessageBox.critical(self, "Ошибка", "Сначала выберите папку проекта")
            return

        try:
            # Инициализируем репозиторий
            project_manager = ProjectManager(project_path, self.logger)
            result = project_manager.initialize(repo_url, name, email)

            if result["success"]:
                # Сохранение в текущий конфиг
                config = {
                    "user.name": name,
                    "user.email": email,
                    "last_repo_url": repo_url
                }
                FileHandler.save_config(config, self.current_config_path)

                self.logger.info(f"Конфиг сохранён: {self.current_config_path}")
                QMessageBox.information(self, "Готово", "Репозиторий инициализирован!")

                # Переключаемся на вкладку работы с Git
                self.main_window.switch_content(0)
                self.main_window.git_work_window.refresh_status()
            else:
                raise Exception(result["error"])

        except Exception as e:
            self.logger.error(f"Ошибка инициализации репозитория: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось инициализировать репозиторий:\n{str(e)}")