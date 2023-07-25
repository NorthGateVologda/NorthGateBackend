# README

## Backend часть платформы NorthGate

Данный проект представляет собой backend часть платформы NorthGate. Он разработан с использованием фреймворка Django, Django Rest Framework, GeoDjango и базы данных PostGIS.

### Установка

1. Клонируйте репозиторий проекта.

2. Установите зависимости, используя следующие команды:

   - Для локальной разработки
   ```shell
   pip install -r requirements/dev.txt
   ```

   - Для пользования
   ```shell
   pip install -r requirements/prod.txt
   ```

3. Создайте файл `.env` в корневой директории проекта и укажите необходимые переменные окружения.

   Пример содержимого `.env`:

   ```plaintext
   DB_NAME=имя_базы_данных
   DB_USER=пользователь_базы_данных
   DB_PASSWORD=пароль_базы_данных
   DB_HOST=хост_базы_данных
   DB_PORT=порт_базы_данных
   SECRET_KEY=секретный_ключ
   ENVIRONMENT=development
   ```

4. Примените миграции с помощью следующей команды:
   ```shell
   python manage.py migrate
   ```

5. Запустите сервер разработки:
   ```shell
   python manage.py runserver
   ```

### Конфигурация базы данных

В данном проекте используется база данных PostGIS. Ниже приведен пример настройки базы данных в файле `settings.py`:

```python
DATABASES = {
    'default': {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": env("DB_NAME"), 
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"), 
        "PORT": env("DB_PORT"),
    }
}
```

## Роутинг

## Авторизация и регистрация пользователей

### `POST /api/user/login/`
Авторизоваться в системе, получив access токен и refresh токен.

Пример CURL-запроса:
```bash
curl -X POST "https://example.com/api/user/login/" \
-H "Content-Type: application/json" \
-d '{"username": "your_username", "password": "your_password"}'
```

### `POST /api/user/registration/`
Зарегистрироваться в системе, получив access токен и refresh токен.

Пример CURL-запроса:
```bash
curl -X POST "https://example.com/api/user/registration/" \
-H "Content-Type: application/json" \
-d '{"username": "new_username", "password": "new_password"}'
```

### `POST /api/user/logout/`
Выйти из системы по access токену.

Пример CURL-запроса:
```bash
curl -X POST "https://example.com/api/user/logout/" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### `POST /api/user/token/refresh/`
Обновить access токен.

Пример CURL-запроса:
```bash
curl -X POST "https://example.com/api/user/token/refresh/" \
-H "Authorization: Bearer YOUR_REFRESH_TOKEN"
```

## Тепловая карта

### `GET /api/get_residential_hexagons/`
Получить тепловую карту по городу, требуется токен для доступа.

Пример CURL-запроса:
```bash
curl -X GET "https://example.com/api/get_residential_hexagons/" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
-d '{"city":"city name"}'
```

### Конфигурация для Docker

Для удобства развертывания проекта существует файл `docker-compose.yml`, который описывает конфигурацию контейнеров Docker.

```yaml
version: '3.9'
services:
  backend:
    build: .
    command: bash -c "python manage.py migrate & gunicorn -w 3 config.wsgi --bind 0.0.0.0:8000"
    volumes:
      - .:/app
    ports:
      - "8000:8000"
```

### Примечание

Необходимо в корне проекта при DEBUG создать `.env` файл со всеми необходимыми переменными окружения.
