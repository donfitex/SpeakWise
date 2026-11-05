from django.core.exceptions import ImproperlyConfigured
from django.core.mail.backends.base import BaseEmailBackend


class DisabledEmailBackend(BaseEmailBackend):
    """Fail closed when any code tries to send email in the no-email pilot."""

    def send_messages(self, email_messages):
        if email_messages:
            raise ImproperlyConfigured("Email delivery is unavailable in this free pilot.")
        return 0
