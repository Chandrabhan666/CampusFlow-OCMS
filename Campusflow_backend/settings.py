from datetime import timedelta
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"

# ✅ FIX: Add ALL Vercel deployment URLs
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'smart-attendance-7bjr.vercel.app',
    'smart-attendance-7bjr-lei75lla3-chandrabhan666s-projects.vercel.app',
    'campus-flow-ocms.vercel.app',
    'campus-flow-ocms-r6c4fgq9y-chandrabhan666s-projects.vercel.app',
    '.vercel.app',  # Wildcard for all Vercel preview deployments
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "rest_framework_simplejwt.token_blacklist",
    "accounts",
    "courses",
    "enrollments",
    "reviews",
    "dashboard",
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

ROOT_URLCONF = "Campusflow_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Campusflow_backend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "ocms_db"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# ✅ FIX: Add CSRF trusted origins for Vercel
CSRF_TRUSTED_ORIGINS = [
    "https://smart-attendance-7bjr.vercel.app",
    "https://smart-attendance-7bjr-lei75lla3-chandrabhan666s-projects.vercel.app",
    "https://campus-flow-ocms.vercel.app",
    "https://campus-flow-ocms-r6c4fgq9y-chandrabhan666s-projects.vercel.app",
]

# ✅ FIX: Handle X-Forwarded headers from Vercel proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Cache: use Redis only when REDIS_URL is set and not localhost (Vercel has no local Redis).
# On Vercel (VERCEL=1), never use 127.0.0.1 so the app works without Redis.
REDIS_URL = os.getenv("REDIS_URL")
_ON_VERCEL = os.getenv("VERCEL") == "1"

_cache_backend = "django.core.cache.backends.locmem.LocMemCache"
_cache_location = "ocms-fallback-cache"

_use_redis = bool(REDIS_URL)
if _use_redis and _ON_VERCEL and ("127.0.0.1" in REDIS_URL or "localhost" in REDIS_URL):
    _use_redis = False  # Never use localhost Redis on Vercel

if _use_redis:
    try:
        import redis  # noqa: F401
    except ImportError:
        _use_redis = False
    else:
        _cache_backend = "django.core.cache.backends.redis.RedisCache"
        _cache_location = REDIS_URL

CACHES = {
    "default": {
        "BACKEND": _cache_backend,
        "LOCATION": _cache_location,
        "TIMEOUT": 600,
    }
}
