#!/bin/bash

# Скрипт запуска консольного приложения MAX

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Проверка наличия venv
if [ ! -d "venv" ]; then
    echo -e "${RED}Ошибка: Виртуальное окружение не найдено${NC}"
    echo ""
    echo "Запустите сначала: bash install.sh"
    exit 1
fi

# Активация venv
source venv/bin/activate

# Проверка наличия .env
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Внимание: Файл .env не найден${NC}"
    echo ""
    read -p "Создать .env сейчас? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp .env.example .env
        echo ""
        echo -e "${GREEN}.env создан. Добавьте ваш токен бота:${NC}"
        echo "MAX_BOT_TOKEN=ваш_токен_здесь"
        echo ""
        read -p "Открыть .env в редакторе? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            ${EDITOR:-nano} .env
        fi
    fi
fi

# Запуск приложения
echo -e "${GREEN}Запуск консольного приложения MAX...${NC}"
echo ""
python -m console_app.main

# Деактивация venv
deactivate
