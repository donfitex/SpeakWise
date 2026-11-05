from .base import *  # noqa: F403

if not env.bool("TEST_POSTGRES", default=False):
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
CELERY_TASK_ALWAYS_EAGER = True
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]
