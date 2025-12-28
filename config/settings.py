import os
from pathlib import Path
from dotenv import load_dotenv

# =========================
# BASE DIR + ENV
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# =========================
# SECURITY
# =========================
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
DEBUG = os.getenv("DEBUG", "0") == "1"

# Добавляем домен Render в разрешенные хосты
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "telegram-webapp-restaurant.onrender.com", # Ваш домен
]

# =========================
# APPLICATIONS
# =========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles", # Обязательно должен быть здесь
    
    "core",
    "catalog",
    "orders",
    "payments",
    "bot",
]

# =========================
# MIDDLEWARE (Добавлен WhiteNoise)
# =========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ИМЕННО ЗДЕСЬ ДЛЯ CSS/JS
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# =========================
# TEMPLATES
# =========================
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

# =========================
# DATABASE (PostgreSQL)
# =========================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "telegram_webapp"),
        "USER": os.getenv("DB_USER", "telegram_webapp_user"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# =========================
# STATIC FILES (Настройка WhiteNoise)
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Хранилище со сжатием и кэшированием для быстрой загрузки
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# =========================
# Telegram WebApp Security
# =========================
X_FRAME_OPTIONS = "ALLOWALL"
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Доверяем домену для POST-запросов (важно для WebApp)
CSRF_TRUSTED_ORIGINS = [
    "https://telegram-webapp-restaurant.onrender.com"
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
