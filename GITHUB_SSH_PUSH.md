# Создание репозитория через SSH

## ✅ SSH настроен и работает!

Ваш SSH ключ уже привязан к GitHub аккаунту `nepobo`.

## Вариант 1: Через GitHub CLI (gh) - быстрее

### Установка GitHub CLI (если не установлен):
```bash
# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Авторизация
gh auth login
```

### Создание репозитория:
```bash
cd /home/nepobo/Myprojects/max-api

# Создать публичный репозиторий
gh repo create max-api --public --source=. --remote=origin --push

# Или приватный
# gh repo create max-api --private --source=. --remote=origin --push
```

## Вариант 2: Через веб-интерфейс + SSH push (рекомендуется)

### Шаг 1: Создайте репозиторий на GitHub
1. Откройте: https://github.com/new
2. Repository name: `max-api`
3. Description: `Python library for MAX Messenger API`
4. Public или Private (выберите)
5. ❌ **НЕ** добавляйте README, .gitignore, license
6. Нажмите **"Create repository"**

### Шаг 2: Подключите через SSH
```bash
cd /home/nepobo/Myprojects/max-api

# Добавьте remote через SSH
git remote add origin git@github.com:nepobo/max-api.git

# Переименуйте ветку в main
git branch -M main

# Загрузите код
git push -u origin main
```

## Вариант 3: Если репозиторий уже существует

```bash
cd /home/nepobo/Myprojects/max-api

# Если remote уже настроен
git remote set-url origin git@github.com:nepobo/max-api.git

# Или добавьте новый
git remote add origin git@github.com:nepobo/max-api.git

# Загрузите
git branch -M main
git push -u origin main
```

## Полная последовательность команд

```bash
# 1. Перейдите в проект
cd /home/nepobo/Myprojects/max-api

# 2. Проверьте статус
git status

# 3. Проверьте текущие remote
git remote -v

# 4. Добавьте GitHub remote (замените max-api на ваше название)
git remote add origin git@github.com:nepobo/max-api.git

# 5. Переименуйте ветку
git branch -M main

# 6. Загрузите на GitHub
git push -u origin main
```

## После успешной загрузки

Репозиторий будет доступен:
```
https://github.com/nepobo/max-api
```

Установка для других пользователей:
```bash
pip install git+https://github.com/nepobo/max-api.git
```

## Troubleshooting

### Если ошибка "remote origin already exists":
```bash
git remote remove origin
git remote add origin git@github.com:nepobo/max-api.git
git push -u origin main
```

### Если нужно изменить URL remote:
```bash
git remote set-url origin git@github.com:nepobo/max-api.git
```

### Проверка SSH ключа:
```bash
ssh -T git@github.com
# Должно быть: Hi nepobo! You've successfully authenticated...
```

## Дополнительные настройки

### Добавить тег версии:
```bash
git tag v0.1.0
git push origin v0.1.0
```

### Создать другие ветки:
```bash
git checkout -b development
git push -u origin development
```

### Настроить репозиторий на GitHub:
- Topics: `python`, `messenger`, `bot`, `max-messenger`, `api-client`, `library`
- About: `Python library for MAX Messenger API integration`
- Website: `https://dev.max.ru/docs-api`

## Готово! 🚀

После `git push` ваш проект будет на GitHub и готов к использованию!
