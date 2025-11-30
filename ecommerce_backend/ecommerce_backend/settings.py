import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-secret")
DEBUG = os.getenv("DEBUG", "0") == "1"
_allowed = os.getenv("ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [h for h in _allowed.split(",") if h] or ["localhost"]

INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    "rest_framework","drf_yasg","graphene_django","django_filters",
    "ecommerce",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "ecommerce.middleware.request_logging.RequestLoggingMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": ["django.template.context_processors.debug",
    "django.template.context_processors.request","django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",],},
}]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASS"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

# Fallback to SQLite for CI/local testing when Postgres env vars are not provided
if not os.getenv("DB_NAME"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(BASE_DIR / "db.sqlite3"),
        }
    }

AUTH_USER_MODEL = "ecommerce.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

GRAPHENE = {
    "SCHEMA": "ecommerce.graphql.schema.schema"
}

STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Celery
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
