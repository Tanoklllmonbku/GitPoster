# build_exe.py
import os
import sys
from pathlib import Path

# Пути
PROJECT_DIR = Path(__file__).parent
SRC_DIR = PROJECT_DIR / "main.py"  # путь к главному файлу GUI
ICON_PATH = PROJECT_DIR / "GUI" / "Icons" / "Icon.ico"  # путь к иконке
DIST_DIR = PROJECT_DIR / "dist"
BUILD_DIR = PROJECT_DIR / "build"

# Проверка: существует ли иконка
if not ICON_PATH.exists():
    print(f"❌ Иконка не найдена: {ICON_PATH}")
    print("Создай папку assets/ и положи туда app_icon.ico")
    input("Нажмите Enter для выхода...")
    sys.exit(1)

cmd = [
    "pyinstaller",
    "--name=DocReator",                    # Имя приложения
    "--onefile",                           # В один файл
    "--windowed",                          # Без консоли (для GUI)
    f"--icon={ICON_PATH}",                 # Иконка
    f"--distpath={DIST_DIR}",              # Куда сохранить .exe
    f"--workpath={BUILD_DIR}",             # Временные файлы
    "--clean",                             # Очистка кэша
    "--noconfirm",                         # Не спрашивать подтверждение
    str(SRC_DIR)                           # Главный файл
]

print("🚀 Сборка .exe...")
print("Команда:", " ".join(cmd))
os.system(" ".join(cmd))

exe_path = DIST_DIR / "GitPoster.exe"
if exe_path.exists():
    print(f"\n✅ Успех! EXE создан: {exe_path}")
    print(f"📍 Путь: {exe_path.resolve()}")
else:
    print(f"\n❌ Ошибка: файл не создан")
    print(f"Ожидаемый путь: {exe_path}")

input("\nНажмите Enter, чтобы закрыть...")