from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parents[2]
env = environ.Env(DJANGO_DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR.parent / ".env", overwrite=False)
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "core",
    "accounts",
    "curriculum",
    "placement",
    "classroom",
    "speech",
    "assessment",
    "progress",
]
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
WSGI_APPLICATION = "config.wsgi.application"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="speakwise"),
        "USER": env("POSTGRES_USER", default="speakwise"),
        "PASSWORD": env("POSTGRES_PASSWORD", default=""),
        "HOST": env("DATABASE_HOST", default="localhost"),
        "PORT": "5432",
    }
}
if env("DATABASE_URL", default=""):
    DATABASES = {"default": env.db()}
    if DATABASES["default"].get("HOST", "").endswith(".neon.tech"):
        DATABASES["default"].setdefault("OPTIONS", {})["sslmode"] = "verify-full"
        DATABASES["default"]["CONN_MAX_AGE"] = 0
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        "core.parsers.ObjectJSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "60/minute",
        "user": "300/minute",
        "auth": "10/minute",
        "speech": "20/hour",
    },
}
SPECTACULAR_SETTINGS = {"TITLE": "SpeakWise API", "VERSION": "1.0.0", "SERVE_INCLUDE_SCHEMA": False}
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CELERY_BROKER_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CELERY_TASK_IGNORE_RESULT = True
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_TIME_LIMIT = 120
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
}
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
X_FRAME_OPTIONS = "DENY"

SPEECH_PROVIDER = env("SPEECH_PROVIDER", default="disabled")
SPEECH_API_KEY = env("SPEECH_API_KEY", default="")
SPEECH_TRANSCRIPTION_MODEL = env("SPEECH_TRANSCRIPTION_MODEL", default="gpt-4o-mini-transcribe")
ALLOW_MOCK_SPEECH = False

MEDIA_ROOT = BASE_DIR.parent / "private-media"
FILE_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 3 * 1024 * 1024
CELERY_BEAT_SCHEDULE = {
    "purge-audio": {"task": "speech.tasks.purge_expired_audio", "schedule": 300.0}
}

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS", default=["http://localhost:5173", "http://127.0.0.1:5173"]
)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@localhost")
CELERY_BEAT_SCHEDULE["purge-learner-data"] = {
    "task": "speech.tasks.purge_learner_data",
    "schedule": 86400.0,
}

_mail_backend = env("EMAIL_BACKEND", default="django.core.mail.backends.locmem.EmailBackend")
_mail_options = {}
if _mail_backend == "django.core.mail.backends.smtp.EmailBackend":
    _mail_options = {
        "host": env("EMAIL_HOST", default="localhost"),
        "port": env.int("EMAIL_PORT", default=587),
        "use_tls": env.bool("EMAIL_USE_TLS", default=True),
        "username": env("EMAIL_HOST_USER", default=""),
        "password": env("EMAIL_HOST_PASSWORD", default=""),
        "timeout": 15,
    }
MAILERS = {"default": {"BACKEND": _mail_backend, "OPTIONS": _mail_options}}
