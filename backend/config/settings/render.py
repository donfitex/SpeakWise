from .production import *  # noqa: F403

# Render terminates TLS before forwarding requests to the container.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
_hostname = env("RENDER_EXTERNAL_HOSTNAME", default="")
if _hostname:
    ALLOWED_HOSTS = list(dict.fromkeys([*ALLOWED_HOSTS, _hostname]))
    CSRF_TRUSTED_ORIGINS = list(dict.fromkeys([*CSRF_TRUSTED_ORIGINS, f"https://{_hostname}"]))
MEDIA_ROOT = Path("/var/data/private-media")
