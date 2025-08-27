# gui/main_window.py
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QFrame, QPushButton
)
from .git_work_window import GitWorkWindow
from .initialize_git_window import InitializeWindow
from .settings_window import SettingsWindow


class MainWindow(QWidget):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.current_theme = "dark"
        self.config_path = None
        self.setup_ui()
        self.apply_theme(self.current_theme)

    def setup_ui(self):
        """Создаёт структуру окна: левая панель, контент, верхняя панель"""
        self.setWindowTitle("GitPoster — Управление версиями для завода")
        self.resize(1000, 650)

        # Основной макет без отступов
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # Левая панель инструментов (20% ширины)
        self.setup_tool_panel(main_layout)

        # Правая область: верх + контент
        self.setup_content_area(main_layout)

    def setup_tool_panel(self, parent_layout):
        """Левая панель с иконками-инструментами"""
        tool_panel = QFrame()
        tool_panel.setFixedWidth(180)
        tool_panel.setObjectName("tool_panel")

        tool_layout = QVBoxLayout(tool_panel)
        tool_layout.setContentsMargins(0, 10, 0, 10)
        tool_layout.setSpacing(5)

        # Кнопки-инструменты
        self.btn_git_work = self.create_tool_button("🛠️", "Работа с Git")
        self.btn_initialize = self.create_tool_button("🚀", "Инициализация")

        tool_layout.addWidget(self.btn_git_work)
        tool_layout.addWidget(self.btn_initialize)
        tool_layout.addStretch()

        parent_layout.addWidget(tool_panel)

        # Привязка кнопок
        self.btn_git_work.clicked.connect(lambda: self.switch_content(0))
        self.btn_initialize.clicked.connect(lambda: self.switch_content(1))
        self.btn_git_work.setChecked(True)

    def setup_content_area(self, parent_layout):
        """Правая область: верхняя панель + контент"""
        content_wrapper = QWidget()
        content_layout = QVBoxLayout(content_wrapper)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Верхняя панель (настройки)
        top_bar = self.create_top_bar()
        content_layout.addWidget(top_bar)

        # Контент (вкладки)
        self.content_stack = QStackedWidget()
        self.git_work_window = GitWorkWindow(self, self.logger)
        self.initialize_window = InitializeWindow(self, self.logger)

        self.content_stack.addWidget(self.git_work_window)
        self.content_stack.addWidget(self.initialize_window)

        content_layout.addWidget(self.content_stack)
        parent_layout.addWidget(content_wrapper)

    def create_top_bar(self):
        """Верхняя панель с настройками"""
        top_bar = QFrame()
        top_bar.setFixedHeight(40)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 0, 10, 0)
        top_layout.addStretch()

        btn_settings = QPushButton("⚙️ Настройки")
        btn_settings.setFixedSize(100, 30)
        btn_settings.clicked.connect(self.open_settings)
        top_layout.addWidget(btn_settings)

        return top_bar

    def create_tool_button(self, icon, text):
        """Создаёт кнопку для левой панели"""
        btn = QPushButton(f" {icon}  {text}")
        btn.setCheckable(True)
        btn.setChecked(False)
        btn.setProperty("tool_button", True)
        btn.setMinimumHeight(40)
        return btn

    def switch_content(self, index):
        """Переключает контент в правой области"""
        self.content_stack.setCurrentIndex(index)
        self.btn_git_work.setChecked(index == 0)
        self.btn_initialize.setChecked(index == 1)

    def open_settings(self):
        """Открывает окно настроек"""
        settings_window = SettingsWindow(self)
        settings_window.exec()

    def apply_theme(self, theme_name):
        """Применяет цветовую тему"""
        self.current_theme = theme_name
        themes = {
            "light": {
                "background": "#F5F7FA",
                "panel_bg": "#E4E7EB",
                "text": "#2D3748",
                "accent": "#3B82F6",
                "border": "#CBD5E0"
            },
            "dark": {
                "background": "#1E293B",
                "panel_bg": "#1E293B",
                "text": "#E2E8F0",
                "accent": "#3B82F6",
                "border": "#334155"
            }
        }

        theme = themes[theme_name]

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {theme['background']};
                color: {theme['text']};
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }}

            #tool_panel {{
                background-color: {theme['panel_bg']};
                border-right: 1px solid {theme['border']};
            }}

            QPushButton[tool_button="true"] {{
                background-color: transparent;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-size: 15px;
                text-align: left;
                qproperty-iconSize: 24px;
                height: 40px;
            }}

            QPushButton[tool_button="true"]:checked {{
                background-color: {theme['accent']};
                color: white;
            }}

            QPushButton[tool_button="true"]:hover:!checked {{
                background-color: {self.lighten_color(theme['accent'], 15)};
            }}

            QFrame {{
                border: none;
            }}

            QTabWidget::pane {{
                border: 1px solid {theme['border']};
                border-radius: 4px;
                background: {theme['background']};
            }}

            QTabBar::tab {{
                background: transparent;
                padding: 8px 16px;
                margin-right: 2px;
                border: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }}

            QTabBar::tab:selected {{
                background: {theme['accent']};
                color: white;
            }}
        """)

        self.tool_panel = self.findChild(QFrame, "tool_panel")
        if self.tool_panel:
            self.tool_panel.setObjectName("tool_panel")

    def lighten_color(self, hex_color, percent):
        """Светлее цвета для ховера"""
        # Упрощённая реализация
        return hex_color[:-2] + "40"