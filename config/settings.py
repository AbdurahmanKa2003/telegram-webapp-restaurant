import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# =========================
# ПУТИ И ОКРУЖЕНИЕ
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# =========================
# БЕЗОПАСНОСТЬ
# =========================
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-dev-key-123")
DEBUG = os.getenv("DEBUG", "0") == "1"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "telegram-webapp-restaurant.onrender.com",
    ".onrender.com",  # добавлено для всех поддоменов Render
]

# =========================
# ПРИЛОЖЕНИЯ (ИСПРАВЛЕННЫЙ ПОРЯДОК!)
# =========================
INSTALLED_APPS = [
    # Django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",  # ДОЛЖНО БЫТЬ ПЕРЕД cloudinary!
    
    # Third-party apps
    'cloudinary',  # сначала библиотека
    'cloudinary_storage',  # потом storage
    
    # Ваши приложения
    "core",
    "catalog",
    "orders",
    "payments",
    "bot",
]

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ДОЛЖНО БЫТЬ ПОСЛЕ SecurityMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# =========================
# БАЗА ДАННЫХ (PostgreSQL)
# =========================
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# =========================
# СТАТИКА (CSS, JS, fonts) - WhiteNoise
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Директории со статическими файлами (исходные файлы)
STATICFILES_DIRS = [
    BASE_DIR / "static",  # если есть глобальная папка static
]

# WhiteNoise настройки для Render
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Оптимизация WhiteNoise
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_AUTOREFRESH = DEBUG  # автообновление только в режиме отладки

# Кэширование статики
WHITENOISE_MAX_AGE = 31536000 if not DEBUG else 0  # 1 год в продакшене

# =========================
# МЕДИА (изображения) - Cloudinary
# =========================
MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Настройки Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
    # Важно для предотвращения конфликтов
    'resource_type': 'auto',
    'folder': 'media/',
}

# =========================
# БЕЗОПАСНОСТЬ И WEBAPP
# =========================
# Для Telegram Web App
X_FRAME_OPTIONS = "ALLOWALL"

# Для работы через прокси Render
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

CSRF_TRUSTED_ORIGINS = [
    "https://telegram-webapp-restaurant.onrender.com",
    "https://*.onrender.com",
]

# Для CORS (если нужно API)
CORS_ALLOWED_ORIGINS = [
    "https://telegram-webapp-restaurant.onrender.com",
]

# =========================
# ОСТАЛЬНЫЕ НАСТРОЙКИ
# =========================
# Internationalization
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================
# НАСТРОЙКИ ДЛЯ РЕНДЕРА
# =========================
# Автоматическое определение хостов на Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Оптимизация для Render
if not DEBUG:
    # Логирование на Render
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
            },
        },
    }
