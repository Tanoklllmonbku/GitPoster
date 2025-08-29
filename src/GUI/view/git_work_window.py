# gui/git_work_window.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QLineEdit, QPushButton, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt

from src.core import ProjectManager


class GitWorkWindow(QWidget):
    def __init__(self, main_window, logger):
        super().__init__()
        self.main_window = main_window
        self.logger = logger
        self.project_manager = None
        self.setup_ui()

    def setup_ui(self):
        """Создаёт интерфейс основной рабочей зоны"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Путь к проекту
        self.path_label = QLabel("Папка не выбрана")
        self.path_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(self.path_label)

        btn_select = QPushButton("📁 Выбрать проект")
        btn_select.setMinimumHeight(40)
        btn_select.clicked.connect(self.select_folder)
        layout.addWidget(btn_select)

        # Статус Git
        self.status_label = QLabel("Git: не инициализирован")
        self.status_label.setStyleSheet("color: red; font-size: 14px;")
        layout.addWidget(self.status_label)

        # Изменённые файлы
        layout.addWidget(QLabel("Изменённые файлы:", styleSheet="font-weight: bold;"))

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.file_list.setStyleSheet("font-family: Consolas, monospace;")
        layout.addWidget(self.file_list, 1)  # Растягиваем

        # Сообщение коммита
        layout.addWidget(QLabel("Сообщение коммита:", styleSheet="font-weight: bold;"))
        self.commit_msg = QLineEdit()
        self.commit_msg.setPlaceholderText("Например: feat: добавил GUI")
        self.commit_msg.setMinimumHeight(40)
        layout.addWidget(self.commit_msg)

        # Кнопки действий
        btn_layout = QHBoxLayout()

        self.btn_refresh = QPushButton("🔄 Обновить")
        self.btn_refresh.setMinimumHeight(40)
        btn_layout.addWidget(self.btn_refresh)

        self.btn_commit = QPushButton("💾 Commit")
        self.btn_commit.setMinimumHeight(40)
        btn_layout.addWidget(self.btn_commit)

        self.btn_push = QPushButton("✅ Commit & Push")
        self.btn_push.setMinimumHeight(40)
        btn_layout.addWidget(self.btn_push)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # Изначально кнопки отключены
        self.btn_commit.setEnabled(False)
        self.btn_push.setEnabled(False)

        # Привязка обработчиков
        self.btn_refresh.clicked.connect(self.refresh_status)
        self.btn_commit.clicked.connect(lambda: self.commit_and_push(False))
        self.btn_push.clicked.connect(lambda: self.commit_and_push(True))

    def select_folder(self):
        """Выбор папки проекта"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку проекта",
            "",
            QFileDialog.Option.ShowDirsOnly
        )

        if folder:
            try:
                self.project_manager = ProjectManager(folder, self.logger)
                self.path_label.setText(folder)
                self.refresh_status()
                self.logger.info(f"Выбрана папка проекта: {folder}")
            except Exception as e:
                self.logger.error(f"Ошибка инициализации ProjectManager: {e}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить проект:\n{str(e)}")

    def refresh_status(self):
        """Обновление статуса репозитория"""
        if not self.project_manager:
            self.logger.error("Папка проекта не выбрана")
            self.status_label.setText("Git: не инициализирован")
            self.status_label.setStyleSheet("color: red;")
            self.btn_commit.setEnabled(False)
            self.btn_push.setEnabled(False)
            self.file_list.clear()
            self.file_list.addItem("Репозиторий не инициализирован")
            return

        try:
            # Проверяем, инициализирован ли репозиторий
            if not self.project_manager.is_git_repo():
                self.status_label.setText("Git: не инициализирован")
                self.status_label.setStyleSheet("color: red;")
                self.btn_commit.setEnabled(False)
                self.btn_push.setEnabled(False)
                self.file_list.clear()
                self.file_list.addItem("Репозиторий не инициализирован. Перейдите на вкладку 'Инициализация'")
                return

            # Получаем статус репозитория
            status_lines = self.project_manager.get_status()

            # Обновляем интерфейс
            self.status_label.setText("Git: инициализирован")
            self.status_label.setStyleSheet("color: green;")
            self.btn_commit.setEnabled(True)
            self.btn_push.setEnabled(True)

            self.file_list.clear()
            if not status_lines or (len(status_lines) == 1 and not status_lines[0]):
                self.file_list.addItem("Нет изменённых файлов")
            else:
                for line in status_lines:
                    self.file_list.addItem(line)

            self.logger.debug("Статус репозитория обновлён")

        except Exception as e:
            self.logger.error(f"Ошибка обновления статуса: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить статус:\n{str(e)}")

    def commit_and_push(self, push: bool):
        """Выполнение коммита и (опционально) пуша"""
        if not self.project_manager:
            self.logger.error("Папка проекта не выбрана")
            QMessageBox.critical(self, "Ошибка", "Выберите папку проекта")
            return

        msg = self.commit_msg.text().strip()
        if not msg:
            self.logger.warning("Сообщение коммита не заполнено")
            QMessageBox.warning(self, "Внимание", "Введите сообщение коммита")
            return

        selected_items = self.file_list.selectedItems()
        if not selected_items:
            self.logger.warning("Файлы для коммита не выбраны")
            QMessageBox.warning(self, "Внимание", "Выберите файлы для коммита")
            return

        # Подготавливаем список файлов
        files_to_commit = []
        for item in selected_items:
            text = item.text().strip()
            if text.startswith(("A ", "M ", "D ", "??")):
                filename = text.split(" ", 1)[1]
                files_to_commit.append(filename)

        try:
            # Выполняем коммит
            commit_result = self.project_manager.commit_files(files_to_commit, msg)
            if not commit_result["success"]:
                raise Exception(commit_result["error"])

            # Выполняем push (если нужно)
            if push:
                push_result = self.project_manager.push()
                if not push_result["success"]:
                    raise Exception(push_result["error"])

            self.logger.info("Коммит выполнен успешно")
            QMessageBox.information(self, "Готово", "Коммит выполнен!")
            self.refresh_status()

        except Exception as e:
            self.logger.error(f"Ошибка коммита: {e}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить коммит:\n{str(e)}")