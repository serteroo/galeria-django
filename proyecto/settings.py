"""
Django settings for proyecto project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key
from django.urls import reverse_lazy

# =========================
# Rutas base y .env
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")          # lee .env en la raíz del repo

# =========================
# Modo / clave / hosts
# =========================
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY") or get_random_secret_key()

# Puedes pasar ALLOWED_HOSTS por env: "ip,dominio,otro"
_ALH = os.getenv("DJANGO_ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS","").split(",") if h.strip()]


# Si expones por IP pública o dominio, completa estas envs en .env
EC2_IP = os.getenv("EC2_PUBLIC_IP", "").strip()
CSRF_TRUSTED_ORIGINS = []

if EC2_IP:
    CSRF_TRUSTED_ORIGINS += [
        f"http://{EC2_IP}:8080",
        f"https://{EC2_IP}:8080",
        f"http://{EC2_IP}",
        f"https://{EC2_IP}",
    ]

# =========================
# Apps
# =========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "rest_framework",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "proyecto.urls"

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

WSGI_APPLICATION = "proyecto.wsgi.application"

# =========================
# Base de datos (MySQL/MariaDB)
# =========================
# Define en .env (ejemplo):
# DB_NAME=backend
# DB_USER=backend
# DB_PASSWORD=tu_password
# DB_HOST=127.0.0.1
# DB_PORT=3306
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =========================
# Password validators
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =========================
# i18n
# =========================
LANGUAGE_CODE =os.getenv("DJANGO_LANGUAGE_CODE", "es-cl")
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE",
"America/Santiago")        # o "America/Santiago"
USE_I18N = True
USE_TZ = True

# =========================
# Archivos estáticos y media
# =========================
# En producción: `python manage.py collectstatic` → a STATIC_ROOT
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# (Opcional) Si tienes una carpeta "static" para desarrollo:
# STATICFILES_DIRS = [BASE_DIR / "static"]

# =========================
# Login/Logout
# =========================
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'galeria'
LOGOUT_REDIRECT_URL = 'login'

# =========================
# Seguridad extra si no DEBUG
# =========================
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

# =========================
# Primary key
# =========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
