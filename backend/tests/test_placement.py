import pytest
from accounts.models import LearnerProfile
from django.contrib.auth import get_user_model
from placement.views import QUESTIONS
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_placement_sequencing_evidence_and_ownership():
    user = get_user_model().objects.create_user(username="p")
    LearnerProfile.objects.create(user=user, display_name="Demo")
    client = APIClient()
    client.force_authenticate(user)
    data = client.post("/api/v1/placement-sessions/").json()
    url = f"/api/v1/placement-sessions/{data['id']}/answers/"
    assert "answer" not in data["question"]
    other = APIClient()
    other.force_authenticate(get_user_model().objects.create_user(username="other"))
    assert other.get(url).status_code == 404
    assert client.post(url, {"index": 2, "answer": "Hello"}).status_code == 409
    for i, q in enumerate(QUESTIONS):
        data = client.post(url, {"index": i, "answer": q["answer"]}).json()
    assert data["result"]["suggested_level"] == "B1" and len(data["result"]["evidence"]) == 4
    assert data["result"]["confidence"] == "low"
    assert client.post(url, {"index": 4, "answer": "anything"}).status_code == 409
