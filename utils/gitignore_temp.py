# utils/gitignore_temp.py
def get_default_gitignore() -> str:
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