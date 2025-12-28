import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url  # Не забудьте добавить в requirements.txt

# =========================
# ПУТИ И ОКРУЖЕНИЕ
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# =========================
# БЕЗОПАСНОСТЬ
# =========================
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-dev-key-123")

# DEBUG должен быть False в продакшене
DEBUG = os.getenv("DEBUG", "0") == "1"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "telegram-webapp-restaurant.onrender.com", # Ваш домен на Render
]

# =========================
# ПРИЛОЖЕНИЯ
# =========================
INSTALLED_APPS = [
    # Хранилище картинок (добавить после pip install django-cloudinary-storage)
    # 'cloudinary_storage', 
    
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # 'cloudinary', # Облако для медиа

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
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Для работы статики на Render
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
        conn_max_age=600
    )
}

# =========================
# СТАТИКА И МЕДИА
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise настройки
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- Настройки Cloudinary (Раскомментируйте, когда получите ключи) ---
# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
#     'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
#     'API_SECRET': os.getenv('CLOUDINARY_API_SECRET')
# }
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# =========================
# БЕЗОПАСНОСТЬ И WEBAPP
# =========================
X_FRAME_OPTIONS = "ALLOWALL"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_TRUSTED_ORIGINS = [
    "https://telegram-webapp-restaurant.onrender.com"
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
