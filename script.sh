#!/bin/bash

# Название проекта (можно поменять)
PROJECT_NAME=""

# Создаем основную структуру
mkdir -p "$PROJECT_NAME"/{app/{routers,models,schemas,db,utils},tests}

# Создаем __init__.py в каждом Python-пакете
touch "$PROJECT_NAME"/app/__init__.py
touch "$PROJECT_NAME"/app/routers/__init__.py
touch "$PROJECT_NAME"/app/models/__init__.py
touch "$PROJECT_NAME"/app/schemas/__init__.py
touch "$PROJECT_NAME"/app/db/__init__.py
touch "$PROJECT_NAME"/app/utils/__init__.py
touch "$PROJECT_NAME"/tests/__init__.py

# Основные файлы
touch "$PROJECT_NAME"/app/main.py
touch "$PROJECT_NAME"/app/routers/{items.py,users.py}
touch "$PROJECT_NAME"/app/models/{item.py,user.py}
touch "$PROJECT_NAME"/app/schemas/{item.py,user.py}
touch "$PROJECT_NAME"/app/db/{session.py,models.py}
touch "$PROJECT_NAME"/app/utils/security.py
touch "$PROJECT_NAME"/tests/{test_items.py,test_users.py}

# Файлы проекта
touch "$PROJECT_NAME"/requirements.txt
touch "$PROJECT_NAME"/.env
touch "$PROJECT_NAME"/README.md

# Создаем виртуальное окружение (опционально)
python -m venv "$PROJECT_NAME/.venv"

echo "✅ Структура FastAPI-проекта создана в папке '$PROJECT_NAME'!"
