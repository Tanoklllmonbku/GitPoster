# gui/settings_window.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton
)


class SettingsWindow(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setWindowTitle("Настройки")
        self.setFixedSize(320, 180)
        self.setup_ui()

    def setup_ui(self):
        """Создаёт интерфейс окна настроек"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Заголовок
        layout.addWidget(QLabel("Настройки приложения",
                                styleSheet="font-weight: bold; font-size: 16px;"))

        # Тема
        layout.addWidget(QLabel("Цветовая тема",
                                styleSheet="font-weight: bold;"))

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Светлая", "Тёмная"])
        self.theme_combo.setCurrentText("Тёмкая" if self.main_window.current_theme == "dark" else "Светлая")
        self.theme_combo.setMinimumHeight(35)
        layout.addWidget(self.theme_combo)

        # Кнопки
        btn_layout = QHBoxLayout()

        btn_apply = QPushButton("Применить")
        btn_apply.setMinimumHeight(40)
        btn_apply.clicked.connect(self.apply_settings)
        btn_layout.addWidget(btn_apply)

        btn_cancel = QPushButton("Отмена")
        btn_cancel.setMinimumHeight(40)
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def apply_settings(self):
        """Применяет выбранные настройки"""
        theme_name = self.theme_combo.currentText()
        theme_map = {"Светлая": "light", "Тёмкая": "dark"}

        self.main_window.apply_theme(theme_map[theme_name])
        self.accept()
        self.main_window.logger.info(f"Тема изменена на: {theme_name}")