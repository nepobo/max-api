#!/bin/bash
# Быстрое получение информации о боте

source venv/bin/activate 2>/dev/null || {
    echo "❌ Виртуальное окружение не найдено"
    echo "Запустите сначала: bash install.sh"
    exit 1
}

python examples/get_bot_info.py
