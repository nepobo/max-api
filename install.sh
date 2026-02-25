#!/bin/bash

# Скрипт автоматической установки MAX API
# Использование: bash install.sh

set -e  # Остановка при ошибке

echo "================================================"
echo "  Установка MAX API Library"
echo "================================================"
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Проверка наличия python3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Ошибка: Python3 не найден${NC}"
    echo "Установите Python3: sudo apt install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Python найден: $(python3 --version)${NC}"

# Проверка наличия python3-venv
echo ""
echo "Проверка наличия python3-venv..."
if ! python3 -m venv --help &> /dev/null; then
    echo -e "${YELLOW}python3-venv не установлен${NC}"
    echo "Для установки выполните:"
    echo -e "${YELLOW}sudo apt update && sudo apt install python3.12-venv python3-full -y${NC}"
    echo ""
    read -p "Попытаться установить сейчас? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt update && sudo apt install python3.12-venv python3-full -y
    else
        echo -e "${RED}Установка прервана. Установите python3-venv вручную.${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✓ python3-venv доступен${NC}"

# Создание виртуального окружения
echo ""
echo "Создание виртуального окружения..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}Виртуальное окружение уже существует${NC}"
    read -p "Пересоздать? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo -e "${GREEN}✓ Виртуальное окружение пересоздано${NC}"
    fi
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Виртуальное окружение создано${NC}"
fi

# Активация виртуального окружения
echo ""
echo "Активация виртуального окружения..."
source venv/bin/activate
echo -e "${GREEN}✓ Виртуальное окружение активировано${NC}"

# Обновление pip
echo ""
echo "Обновление pip..."
pip install --upgrade pip --quiet
echo -e "${GREEN}✓ pip обновлен${NC}"

# Установка зависимостей
echo ""
echo "Установка зависимостей из requirements.txt..."
pip install -r requirements.txt --quiet
echo -e "${GREEN}✓ Зависимости установлены${NC}"

# Проверка установки
echo ""
echo "Проверка установки..."
python -c "from max_api import MAXClient; print('✓ Библиотека max_api импортирована успешно')"

# Создание .env если не существует
if [ ! -f ".env" ]; then
    echo ""
    echo "Создание файла .env..."
    cp .env.example .env
    echo -e "${GREEN}✓ Файл .env создан из .env.example${NC}"
    echo -e "${YELLOW}⚠ Не забудьте добавить ваш токен бота в файл .env${NC}"
else
    echo -e "${YELLOW}Файл .env уже существует${NC}"
fi

# Вывод информации
echo ""
echo "================================================"
echo -e "${GREEN}  Установка завершена успешно! 🎉${NC}"
echo "================================================"
echo ""
echo "Следующие шаги:"
echo ""
echo "1. Получите токен бота на https://business.max.ru/self"
echo ""
echo "2. Добавьте токен в файл .env:"
echo "   nano .env"
echo ""
echo "3. Активируйте виртуальное окружение:"
echo -e "   ${YELLOW}source venv/bin/activate${NC}"
echo ""
echo "4. Запустите консольное приложение:"
echo -e "   ${YELLOW}python -m console_app.main${NC}"
echo ""
echo "   Или запустите примеры:"
echo -e "   ${YELLOW}python examples/echo_bot.py${NC}"
echo -e "   ${YELLOW}python examples/simple_bot.py${NC}"
echo ""
echo "5. Для запуска тестов:"
echo -e "   ${YELLOW}pytest tests/${NC}"
echo ""
echo "================================================"
echo ""
echo "Установленные пакеты:"
pip list | grep -E "(requests|python-dotenv|click|colorama|pydantic|pytest)"
echo ""
echo -e "${GREEN}Готово к работе!${NC}"
echo ""
