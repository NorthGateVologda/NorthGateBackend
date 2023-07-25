from datetime import timedelta
import os
from pathlib import Path
import environ
import logging

ENVIRON = os.environ
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = ENVIRON.get("ENVIRONMENT", "development") == "development"

def get_secret(key, default=""):
    value = os.getenv(key, default)
    if os.path.isfile(value):
        with open(value) as f:
            return f.read().replace("\n", "")
    return value.replace("\n", "")


def get_env(key):
    env = environ.Env()
    path_to_env = os.path.join(BASE_DIR, ".env")
    environ.Env.read_env(path_to_env)
    return env(key)


if DEBUG:
    SECRET_KEY = get_env("BACKEND_SECRET_KEY")
    YANDEX_KEY = get_env("YANDEX_KEY")
    YANDEX_URL = get_env("YANDEX_URL")
    CORS_ALLOW_ALL_ORIGINS = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

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
    YANDEX_KEY = get_secret("YANDEX_KEY")
    YANDEX_URL = get_secret("YANDEX_URL")
    CORS_ALLOWED_ORIGINS = [ENVIRON.get("CORS_ALLOWED_ORIGINS")]
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
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

ALLOWED_HOSTS = [ENVIRON.get("ALLOWED_HOSTS", "*")]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.gis',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'api'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'SIGNING_KEY': SECRET_KEY,
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True
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