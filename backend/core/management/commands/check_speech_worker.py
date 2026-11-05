"""Exercise real Redis/Celery transport using only a short synthetic WAV."""

import io
import time
import uuid
import wave
from datetime import timedelta

from accounts.models import ConsentRecord, LearnerProfile
from classroom.models import LessonSession
from curriculum.models import LessonVersion
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from speech.models import SpeechAttempt
from speech.tasks import process_speech, remove_audio


class Command(BaseCommand):
    help = "Test real worker safe fallback; requires SPEECH_PROVIDER=disabled and seeded sample content."

    def handle(self, *args, **kwargs):
        if settings.SPEECH_PROVIDER != "disabled":
            raise CommandError("Run this smoke test only with speech disabled.")
        version = (
            LessonVersion.objects.filter(status="published", activities__kind="speaking")
            .distinct()
            .first()
        )
        if not version:
            raise CommandError("Run seed_demo first.")
        activities = list(version.activities.all())
        position = next(i for i, a in enumerate(activities) if a.kind == "speaking")
        user = get_user_model().objects.create_user(username="worker-smoke-" + uuid.uuid4().hex)
        job = None
        try:
            profile = LearnerProfile.objects.create(
                user=user, display_name="Synthetic worker smoke"
            )
            consent = ConsentRecord.objects.create(learner=profile, granted=True)
            session = LessonSession.objects.create(
                learner=profile, lesson_version=version, position=position
            )
            out = io.BytesIO()
            with wave.open(out, "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(16000)
                wav.writeframes(b"\0\0" * 16000)
            job = SpeechAttempt.objects.create(
                session=session,
                activity=activities[position],
                consent=consent,
                request_id=uuid.uuid4(),
                audio=SimpleUploadedFile("synthetic.wav", out.getvalue(), content_type="audio/wav"),
                expires_at=timezone.now() + timedelta(minutes=5),
            )
            process_speech.delay(str(job.pk))
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                job.refresh_from_db()
                if job.status in ["complete", "failed"]:
                    break
                time.sleep(0.25)
            if job.status != "failed" or job.audio or job.result.get("scores"):
                raise CommandError(
                    "Expected disabled-provider fallback, empty score, and audio cleanup within 30 seconds."
                )
            self.stdout.write(
                self.style.SUCCESS(
                    "Real Redis/Celery speech job finished with safe disabled-provider fallback and audio cleanup."
                )
            )
        finally:
            if job:
                job.refresh_from_db()
                job.status = "deleted"
                remove_audio(job)
                job.save()
                job.delete()
            user.delete()
