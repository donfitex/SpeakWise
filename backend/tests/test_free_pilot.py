import uuid
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from speech.models import SpeechAttempt


@pytest.mark.django_db
def test_free_pilot_rejects_audio_without_saving_or_queueing(settings, tmp_path):
    settings.SPEECH_UPLOADS_ENABLED = False
    settings.MEDIA_ROOT = tmp_path
    client = APIClient()
    client.force_authenticate(get_user_model().objects.create_user(username="free-pilot"))
    with patch("speech.views.process_speech.delay") as enqueue:
        response = client.post(
            f"/api/v1/lesson-sessions/{uuid.uuid4()}/speech-attempts/",
            {"audio": SimpleUploadedFile("test.wav", b"synthetic", content_type="audio/wav")},
        )
    assert response.status_code == 503
    enqueue.assert_not_called()
    assert not SpeechAttempt.objects.exists()
    assert not list(tmp_path.iterdir())


def test_free_pilot_password_reset_never_sends_or_claims_delivery(settings):
    settings.PASSWORD_RESET_ENABLED = False
    with patch("accounts.views.send_mail") as send:
        response = APIClient().post(
            "/api/v1/auth/password-reset/", {"email": "synthetic@example.com"}
        )
    assert response.status_code == 503
    assert "unavailable" in response.json()["detail"]
    send.assert_not_called()
