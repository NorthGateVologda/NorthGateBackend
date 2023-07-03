import os
from pathlib import Path
import environ


def get_secret(key, default=""):
    value = os.getenv(key, default)
    if os.path.isfile(value):
        with open(value) as f:
            return f.read().replace("\n", "")
    return value.replace("\n", "")


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = get_secret("BACKEND_SECRET_KEY")
DEBUG = get_secret("BACKEND_ENVIRONMENT") == "dev"
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.gis',
    'rest_framework',
    'apps.api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
APPEND_SLASH = True

DATABASES = {
    'default': {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": get_secret("BACKEND_DB_NAME"),
        "USER": get_secret("BACKEND_DB_USER"),
        "PASSWORD": get_secret("BACKEND_DB_PASSWORD"),
        "HOST": get_secret("BACKEND_DB_HOST"),
        "PORT": get_secret("BACKEND_DB_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
