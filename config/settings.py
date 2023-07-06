import os
from pathlib import Path
import environ
import logging

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.environ.get("ENVIRONMENT") == "development"

def get_secret(key, default=""):
    value = os.getenv(key, default)
    if os.path.isfile(value):
        with open(value) as f:
            return f.read().replace("\n", "")
    return value.replace("\n", "")


def get_env(key):
    if DEBUG:
        env_file = "dev.env"
    else:
        env_file = "prod.env"

    env = environ.Env()
    path_to_env = os.path.join(BASE_DIR, env_file)
    environ.Env.read_env(path_to_env)
    return env(key)


if DEBUG:
    SECRET_KEY = get_env("BACKEND_SECRET_KEY")

    DATABASES = {
        'default': {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": get_env("BACKEND_DB_NAME"),
            "USER": get_env("BACKEND_DB_USER"),
            "PASSWORD": get_env("BACKEND_DB_PASSWORD"),
            "HOST": get_env("BACKEND_DB_HOST"),
            "PORT": get_env("BACKEND_DB_PORT"),
        }
    }
else:
    SECRET_KEY = get_secret("BACKEND_SECRET_KEY")

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

CORS_ALLOWED_ORIGIN_REGEXES = [get_env("CORS_ALLOWED_ORIGIN_REGEXES")]
ALLOWED_HOSTS = [get_env("ALLOWED_HOSTS")]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.gis',
    'rest_framework',
    'apps.api.apps.ApiConfig',
    'corsheaders'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
APPEND_SLASH = True
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'