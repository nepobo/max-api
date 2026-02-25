# Инструкция по загрузке на GitHub

## Шаг 1: Создайте репозиторий на GitHub

1. Откройте https://github.com/new
2. Название репозитория: `max-api` (или любое другое)
3. Описание: `Python library for MAX Messenger API`
4. **НЕ** выбирайте "Add a README file"
5. **НЕ** выбирайте "Add .gitignore"
6. **НЕ** выбирайте "Choose a license"
7. Нажмите "Create repository"

## Шаг 2: Подключите локальный репозиторий

После создания GitHub покажет команды. Выполните:

```bash
cd /home/nepobo/Myprojects/max-api

# Добавьте remote (замените YOUR_USERNAME на ваш GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/max-api.git

# Или если используете SSH:
# git remote add origin git@github.com:YOUR_USERNAME/max-api.git

# Переименуйте ветку в main (если нужно)
git branch -M main

# Загрузите код
git push -u origin main
```

## Шаг 3: Настройте GitHub (опционально)

### Добавьте описание репозитория:
- Topics: `python`, `messenger`, `bot`, `max-messenger`, `api-client`
- Description: `Python library for MAX Messenger API integration`
- Website: https://dev.max.ru/docs-api

### Настройте README:
GitHub автоматически отобразит ваш `README.md`

### Создайте Release:
```bash
# После первого push создайте тег
git tag v0.1.0
git push origin v0.1.0
```

На GitHub перейдите в "Releases" → "Create a new release" → выберите тег `v0.1.0`

## Быстрые команды

```bash
# Проверить текущий remote
git remote -v

# Добавить remote (ЗАМЕНИТЕ YOUR_USERNAME!)
git remote add origin https://github.com/YOUR_USERNAME/max-api.git

# Переименовать ветку
git branch -M main

# Загрузить на GitHub
git push -u origin main

# Проверить статус
git status
```

## Если remote уже существует

```bash
# Посмотреть текущие remote
git remote -v

# Удалить старый remote
git remote remove origin

# Добавить новый
git remote add origin https://github.com/YOUR_USERNAME/max-api.git

# Загрузить
git push -u origin main
```

## После успешной загрузки

Ваш репозиторий будет доступен по адресу:
```
https://github.com/YOUR_USERNAME/max-api
```

Другие пользователи смогут установить вашу библиотеку:
```bash
pip install git+https://github.com/YOUR_USERNAME/max-api.git
```

## Полезные ссылки

- Создать новый репозиторий: https://github.com/new
- GitHub CLI: https://cli.github.com/ (если хотите создать через командную строку)
- GitHub Personal Access Tokens: https://github.com/settings/tokens (если нужен token для HTTPS)
