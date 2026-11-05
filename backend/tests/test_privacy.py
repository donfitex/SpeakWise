import uuid
from datetime import timedelta

import pytest
from accounts.models import ConsentRecord, LearnerProfile
from classroom.models import LessonSession
from curriculum.models import LessonVersion
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.utils import timezone
from rest_framework.test import APIClient
from speech.models import SpeechAttempt


@pytest.mark.django_db
def test_revoke_and_account_deletion_remove_private_files(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    call_command("seed_demo")
    u = get_user_model().objects.create_user(username="delete-me", password="sample-pass")
    p = LearnerProfile.objects.create(user=u, display_name="Demo")
    consent = ConsentRecord.objects.create(learner=p, granted=True)
    version = LessonVersion.objects.first()
    s = LessonSession.objects.create(learner=p, lesson_version=version)
    job = SpeechAttempt.objects.create(
        session=s,
        activity=version.activities.first(),
        consent=consent,
        request_id=uuid.uuid4(),
        audio=SimpleUploadedFile("sample.wav", b"synthetic"),
        expires_at=timezone.now() + timedelta(minutes=5),
    )
    path = job.audio.path
    c = APIClient()
    c.force_authenticate(u)
    assert (
        c.post("/api/v1/learners/me/consent/", {"granted": False}, format="json").status_code == 200
    )
    from pathlib import Path

    assert not Path(path).exists()
    job.refresh_from_db()
    assert job.status == "deleted"
    assert c.get("/api/v1/learners/me/data/").json()["profile"]["id"] == str(p.id)
    assert (
        c.delete(
            "/api/v1/learners/me/data/",
            {"password": "bad", "confirmation": "DELETE"},
            format="json",
        ).status_code
        == 400
    )
    assert (
        c.delete(
            "/api/v1/learners/me/data/",
            {"password": "sample-pass", "confirmation": "DELETE"},
            format="json",
        ).status_code
        == 204
    )
    assert (
        not get_user_model().objects.filter(pk=u.pk).exists() and SpeechAttempt.objects.count() == 0
    )
