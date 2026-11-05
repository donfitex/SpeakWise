import uuid

import pytest
from accounts.models import LearnerProfile
from classroom.models import ActivityAttempt, LessonSession, TeacherTurn
from curriculum.models import LessonVersion
from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework.test import APIClient


@pytest.fixture
def learner(db):
    call_command("seed_demo")
    user = get_user_model().objects.create_user(username="learner")
    LearnerProfile.objects.create(user=user, display_name="Demo")
    client = APIClient()
    client.force_authenticate(user)
    return client


def test_resume_retry_completion_and_idempotency(learner):
    version = LessonVersion.objects.filter(lesson__unit__level="A1").first()
    url = "/api/v1/lesson-sessions/"
    session = learner.post(url, {"lesson_version": str(version.id)}).json()
    pk = session["id"]
    url += pk + "/turns/"
    wrong = {
        "activity_id": session["activity"]["id"],
        "answer": "wrong",
        "request_id": str(uuid.uuid4()),
    }
    assert learner.post(url, wrong).json()["session"]["position"] == 0
    assert learner.post(url, wrong).status_code == 200 and ActivityAttempt.objects.count() == 1
    assert learner.post(url, {**wrong, "answer": "different"}).status_code == 400
    for a in version.activities.all():
        data = learner.post(
            url, {"activity_id": str(a.id), "answer": a.answers[0], "request_id": str(uuid.uuid4())}
        ).json()
    assert data["session"]["completed"] and data["session"]["activity"] is None
    assert learner.post("/api/v1/lesson-sessions/", {"lesson_version": str(version.id)}).json()[
        "completed"
    ]
    assert LessonSession.objects.count() == 1
    assert TeacherTurn.objects.count() == 6
    assert learner.get(f"/api/v1/lesson-sessions/{pk}/").json()["turns"][-1]["speaker"] == "teacher"
    other = APIClient()
    other.force_authenticate(get_user_model().objects.create_user(username="other"))
    assert other.get(f"/api/v1/lesson-sessions/{pk}/").status_code == 404
