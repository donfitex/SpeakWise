from django.core.management.base import BaseCommand

from speech.tasks import purge_expired_audio


class Command(BaseCommand):
    help = "Delete expired processing audio; schedule at least every ten minutes."

    def handle(self, *args, **kwargs):
        self.stdout.write(f"Deleted {purge_expired_audio()} expired recordings.")
