# Backend часть платформы NorthGate

Он разработан с использованием фреймворка Django, Django Rest Framework, GeoDjango и базы данных PostGIS.

## Установка

1. Клонируйте репозиторий проекта.

2. Установите зависимости, используя следующую команду:
    ```shell
    pip install -r requirements.txt
    ```

3. Создайте файл `.env` в корневой директории проекта и укажите необходимые переменные окружения. Пример содержимого `.env`:

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

## Конфигурация базы данных

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

В системе доступны следующие маршруты:

```
/api/v1/object_tourism/
```
1. Маршрут для просмотра туристических объектов в заданной окружности
2. Обязательно тело при отправке в JSON формате:
```json
{
  "center_lat":"..", 
  "center_lon": "..", 
  "radius": "..", 
  "username": ".."
}
```
Пример:
```json
{
  "center_lat":"5343335.558077131", 
  "center_lon": "6106854.834885075", 
  "radius": "100", 
  "username": "Vasya"
}
```
- `center_lat` - широта центра области поиска **в системе Google Mercator (EPSG:3857)** 
- `center_lon` - долгота центра области поиска **в системе Google Mercator (EPSG:3857)** 
- `radius` - радиус области поиска **в метрах**
- `username` - имя пользователя
