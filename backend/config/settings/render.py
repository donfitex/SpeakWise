from .production import *  # noqa: F403

# Render terminates HTTPS before forwarding requests to the container.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
_hostname = env("RENDER_EXTERNAL_HOSTNAME", default="")
if _hostname:
    ALLOWED_HOSTS = list(dict.fromkeys([*ALLOWED_HOSTS, _hostname]))
    CSRF_TRUSTED_ORIGINS = list(dict.fromkeys([*CSRF_TRUSTED_ORIGINS, f"https://{_hostname}"]))

# One Gunicorn process: rate limits remain shared within that process.
# Accounts, sessions, and progress use PostgreSQL, never the ephemeral filesystem.
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
MEDIA_ROOT = Path("/tmp/speakwise-private-media")
SPEECH_UPLOADS_ENABLED = False
SPEECH_PROVIDER = "disabled"
PASSWORD_RESET_ENABLED = False
# The free pilot sends no email. Never log password-reset tokens.
MAILERS = {"default": {"BACKEND": "core.mail.DisabledEmailBackend"}}
