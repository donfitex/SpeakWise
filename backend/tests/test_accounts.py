import pytest
from accounts.models import LearnerProfile
from django.contrib.auth import get_user_model
from django.core import mail
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_registration_profile_ownership_and_reset():
    a = APIClient()
    b = APIClient()
    payload = {
        "username": "learner",
        "email": "learner@example.test",
        "password": "Strong-sample-pass!98",
        "display_name": "Demo",
        "eligible": True,
    }
    assert a.post("/api/v1/auth/register/", payload).status_code == 201
    other = get_user_model().objects.create_user(username="other", password="anything")
    LearnerProfile.objects.create(user=other, display_name="Other")
    b.force_authenticate(other)
    assert a.patch("/api/v1/learners/me/", {"display_name": "Changed"}).status_code == 200
    assert b.get("/api/v1/learners/me/").json()["display_name"] == "Other"
    assert APIClient().get("/api/v1/learners/me/").status_code == 403
    assert a.post("/api/v1/learners/me/consent/", {"granted": True}, format="json").json()[
        "granted"
    ]
    assert not b.get("/api/v1/learners/me/consent/").json()["granted"]
    response = APIClient().post("/api/v1/auth/password-reset/", {"email": payload["email"]})
    assert response.status_code == 200 and len(mail.outbox) == 1
    code = mail.outbox[0].body.split()[-1]
    uid, token = code.split("/")
    assert (
        APIClient()
        .post(
            "/api/v1/auth/password-reset/confirm/",
            {"uid": uid, "token": token, "password": "A-new-safe-pass!908"},
        )
        .status_code
        == 200
    )
    assert (
        APIClient()
        .post(
            "/api/v1/auth/password-reset/confirm/",
            {"uid": uid, "token": token, "password": "A-new-safe-pass!908"},
        )
        .status_code
        == 400
    )


def test_unsafe_auth_requires_csrf_and_profile_validation():
    client = APIClient(enforce_csrf_checks=True)
    assert client.post("/api/v1/auth/login/", {"username": "x", "password": "x"}).status_code == 403
    user = get_user_model().objects.create_user(username="sample")
    LearnerProfile.objects.create(user=user, display_name="Demo")
    client = APIClient()
    client.force_authenticate(user)
    assert client.patch("/api/v1/learners/me/", {"daily_minutes": 0}).status_code == 400
