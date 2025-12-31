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
    ".onrender.com",
]

# =========================
# ПРИЛОЖЕНИЯ
# =========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",  # ДОЛЖНО БЫТЬ ПЕРЕД cloudinary
    
    # Cloudinary - ТОЛЬКО для медиа
    'cloudinary',
    'cloudinary_storage',
    
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
    "whitenoise.middleware.WhiteNoiseMiddleware",
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
                "django.template.context_processors.static",  # ДОБАВИТЬ!
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# =========================
# БАЗА ДАННЫХ
# =========================
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# =========================
# СТАТИКА (CSS, JS) - WhiteNoise
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ГДЕ ИСКАТЬ СТАТИЧЕСКИЕ ФАЙЛЫ (важно!)
STATICFILES_DIRS = [
    BASE_DIR / "static",  # глобальная папка static
    BASE_DIR / "static/webapp",  # ваши CSS/JS файлы здесь
]

# WhiteNoise настройки
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Дополнительные настройки WhiteNoise
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_ROOT = BASE_DIR / "staticfiles"

# =========================
# МЕДИА (изображения) - Cloudinary
# =========================
MEDIA_URL = "/media/"

# Используем Cloudinary ТОЛЬКО если есть настройки
if all([
    os.getenv('CLOUDINARY_CLOUD_NAME'),
    os.getenv('CLOUDINARY_API_KEY'),
    os.getenv('CLOUDINARY_API_SECRET')
]):
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
        'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
        'folder': 'media/',
    }
else:
    # Локальное хранение медиа, если нет Cloudinary
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_ROOT = BASE_DIR / 'media'

# =========================
# БЕЗОПАСНОСТЬ И WEBAPP
# =========================
X_FRAME_OPTIONS = "ALLOWALL"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [
    "https://telegram-webapp-restaurant.onrender.com",
    "https://*.onrender.com",
]

# =========================
# ТЕЛЕГРАМ БОТ (исправление конфликта)
# =========================
# Убедитесь, что бот запускается только один раз
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# =========================
# ДРУГИЕ НАСТРОЙКИ
# =========================
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================
# РЕНДЕР СЕРВИС
# =========================
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
