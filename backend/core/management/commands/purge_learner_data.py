from datetime import timedelta

from classroom.models import LessonSession
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from progress.models import SkillProgress
from speech.models import SpeechAttempt
from speech.tasks import purge_expired_audio, remove_audio


class Command(BaseCommand):
    help = "Delete raw audio past expiry and learner sessions/transcripts inactive for 90 days."

    @transaction.atomic
    def handle(self, *args, **options):
        purge_expired_audio()
        old = LessonSession.objects.filter(updated_at__lt=timezone.now() - timedelta(days=90))
        learner_ids = list(old.values_list("learner_id", flat=True))
        for job in SpeechAttempt.objects.filter(session__in=old):
            remove_audio(job)
        count = old.count()
        old.delete()
        SkillProgress.objects.filter(learner_id__in=learner_ids).delete()
        # Rebuild advisory aggregates only from retained evidence.
        from classroom.models import ActivityAttempt
        from progress.services import update_from_attempt

        for attempt in ActivityAttempt.objects.filter(session__learner_id__in=learner_ids).order_by(
            "created_at"
        ):
            update_from_attempt(attempt)
        self.stdout.write(f"Deleted {count} expired sessions and rebuilt affected skill notes.")
