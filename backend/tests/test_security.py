import uuid
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


@pytest.mark.django_db
def test_prerequisites_out_of_order_and_invalid_answers():
    call_command("seed_demo")
    u = get_user_model().objects.create_user(username="gates")
    LearnerProfile.objects.create(user=u, display_name="Demo")
    c = APIClient()
    c.force_authenticate(u)
    versions = list(LessonVersion.objects.order_by("lesson__unit__sequence"))
    versions[1].lesson.prerequisites.add(versions[0].lesson)
    assert (
        c.post("/api/v1/lesson-sessions/", {"lesson_version": str(versions[1].id)}).status_code
        == 403
    )
    session = c.post("/api/v1/lesson-sessions/", {"lesson_version": str(versions[0].id)}).json()
    url = f"/api/v1/lesson-sessions/{session['id']}/turns/"
    assert (
        c.post(
            url,
            {
                "activity_id": str(versions[0].activities.last().id),
                "answer": "x",
                "request_id": str(uuid.uuid4()),
            },
        ).status_code
        == 400
    )
    assert (
        c.post(
            url,
            {
                "activity_id": session["activity"]["id"],
                "answer": "",
                "request_id": str(uuid.uuid4()),
            },
        ).status_code
        == 400
    )
    assert c.get("/admin/").status_code == 302


@pytest.mark.django_db
def test_inactive_session_retention_cleans_audio_and_turns(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    call_command("seed_demo")
    u = get_user_model().objects.create_user(username="retention")
    p = LearnerProfile.objects.create(user=u, display_name="Demo")
    consent = ConsentRecord.objects.create(learner=p, granted=True)
    v = LessonVersion.objects.first()
    s = LessonSession.objects.create(learner=p, lesson_version=v)
    job = SpeechAttempt.objects.create(
        session=s,
        activity=v.activities.first(),
        consent=consent,
        request_id=uuid.uuid4(),
        audio=SimpleUploadedFile("x.wav", b"synthetic"),
        expires_at=timezone.now() + timedelta(minutes=1),
    )
    path = job.audio.path
    LessonSession.objects.filter(pk=s.pk).update(updated_at=timezone.now() - timedelta(days=91))
    call_command("purge_learner_data")
    from pathlib import Path

    assert (
        not Path(path).exists()
        and not LessonSession.objects.exists()
        and not SpeechAttempt.objects.exists()
    )


@pytest.mark.django_db
@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication"],
        "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    }
)
def test_cross_user_feedback_reports_denied():
    from assessment.models import AssessmentResult
    from classroom.services import submit_answer

    call_command("seed_demo")
    u = get_user_model().objects.create_user(username="owner")
    p = LearnerProfile.objects.create(user=u, display_name="Demo")
    v = LessonVersion.objects.first()
    s = LessonSession.objects.create(learner=p, lesson_version=v)
    a = v.activities.first()
    submit_answer(s, a.id, a.answers[0], uuid.uuid4())
    result = AssessmentResult.objects.get()
    other = get_user_model().objects.create_user(username="stranger")
    LearnerProfile.objects.create(user=other, display_name="Other")
    c = APIClient()
    c.force_authenticate(other)
    assert c.post(f"/api/v1/assessments/{result.id}/report/", {"reason": "test"}).status_code == 404
    c.force_authenticate(u)
    assert (
        c.post(f"/api/v1/assessments/{result.id}/report/", {"reason": "Please review"}).status_code
        == 201
    )


@pytest.mark.django_db
def test_malformed_auth_payloads_return_validation_errors():
    c = APIClient()
    assert c.post("/api/v1/auth/login/", [], format="json").status_code == 400
    assert (
        c.post(
            "/api/v1/auth/login/",
            {"username": "x", "password": {"unexpected": "object"}},
            format="json",
        ).status_code
        == 400
    )
    assert (
        c.post(
            "/api/v1/auth/password-reset/confirm/",
            {"uid": [], "token": {}, "password": "sample"},
            format="json",
        ).status_code
        == 400
    )
