import io
import uuid
import wave
from datetime import timedelta

import pytest
from accounts.models import ConsentRecord, LearnerProfile
from classroom.models import LessonSession
from curriculum.models import LessonVersion
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import override_settings
from django.utils import timezone
from rest_framework.test import APIClient
from speech.models import SpeechAttempt
from speech.tasks import process_speech, purge_expired_audio


@pytest.fixture
def speech_setup(db, tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    call_command("seed_demo")
    user = get_user_model().objects.create_user(username="speaker")
    profile = LearnerProfile.objects.create(user=user, display_name="Demo")
    version = LessonVersion.objects.filter(lesson__unit__level="pre-A1").first()
    session = LessonSession.objects.create(learner=profile, lesson_version=version, position=1)
    c = APIClient()
    c.force_authenticate(user)
    return c, profile, session


def wav_file(seconds=1):
    out = io.BytesIO()
    with wave.open(out, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(b"\0\0" * int(16000 * seconds))
    return SimpleUploadedFile("test.wav", out.getvalue(), content_type="audio/wav")


@override_settings(SPEECH_PROVIDER="mock", ALLOW_MOCK_SPEECH=True)
def test_audio_consent_processing_idempotency_and_cleanup(speech_setup):
    c, profile, s = speech_setup
    url = f"/api/v1/lesson-sessions/{s.id}/speech-attempts/"
    key = str(uuid.uuid4())
    assert c.post(url, {"request_id": key, "audio": wav_file()}).status_code == 403
    ConsentRecord.objects.create(learner=profile, granted=True)
    r = c.post(url, {"request_id": key, "audio": wav_file()})
    assert r.status_code == 202
    pk = r.json()["id"]
    assert c.post(url, {"request_id": key, "audio": wav_file()}).json()["id"] == pk
    process_speech(pk)
    job = SpeechAttempt.objects.get(pk=pk)
    assert job.status == "complete" and job.result["simulated"] and not job.result["scores"]
    assert not job.audio and job.duration_seconds == 1
    process_speech(pk)
    assert SpeechAttempt.objects.count() == 1
    assert c.delete(f"/api/v1/speech-attempts/{pk}/status/").status_code == 204
    assert not c.get(f"/api/v1/speech-attempts/{pk}/status/").json()["transcript"]


def test_malformed_audio_failure_expiry_and_cross_user_denial(speech_setup):
    c, profile, s = speech_setup
    consent = ConsentRecord.objects.create(learner=profile, granted=True)
    job = SpeechAttempt.objects.create(
        session=s,
        activity=s.lesson_version.activities.last(),
        consent=consent,
        request_id=uuid.uuid4(),
        audio=SimpleUploadedFile("bad.wav", b"not audio"),
        expires_at=timezone.now() + timedelta(minutes=5),
    )
    process_speech(str(job.id))
    job.refresh_from_db()
    assert job.status == "failed" and not job.audio
    job2 = SpeechAttempt.objects.create(
        session=s,
        activity=job.activity,
        consent=consent,
        request_id=uuid.uuid4(),
        audio=wav_file(),
        expires_at=timezone.now() - timedelta(seconds=1),
    )
    assert purge_expired_audio() == 1
    job2.refresh_from_db()
    assert not job2.audio
    c.force_authenticate(get_user_model().objects.create_user(username="other"))
    assert c.get(f"/api/v1/speech-attempts/{job.id}/status/").status_code == 404
