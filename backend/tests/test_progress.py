import uuid
from datetime import timedelta

import pytest
from accounts.models import LearnerProfile
from classroom.models import LessonSession
from classroom.services import submit_answer
from curriculum.models import LessonVersion
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.utils import timezone
from progress.models import SkillProgress
from progress.services import recommend, update_from_attempt


@pytest.mark.django_db
def test_progress_valid_evidence_and_repeatable_recommendation():
    call_command("seed_demo")
    u = get_user_model().objects.create_user(username="progress")
    p = LearnerProfile.objects.create(user=u, display_name="Demo", level="A1")
    v = LessonVersion.objects.filter(lesson__unit__level="A1").first()
    s = LessonSession.objects.create(learner=p, lesson_version=v)
    a = v.activities.first()
    attempt = submit_answer(s, a.id, "wrong", uuid.uuid4())
    progress = SkillProgress.objects.get(learner=p, skill__slug="grammar")
    assert progress.estimate == 1 and progress.evidence_count == 1
    update_from_attempt(attempt)
    progress.refresh_from_db()
    assert progress.evidence_count == 1
    progress.next_review_due = timezone.now() - timedelta(seconds=1)
    progress.save()
    assert recommend(p) == recommend(p) and recommend(p)["review"]
    speaking = LessonVersion.objects.filter(lesson__unit__level="pre-A1").first()
    s = LessonSession.objects.create(learner=p, lesson_version=speaking, position=1)
    a = speaking.activities.last()
    submit_answer(s, a.id, a.answers[0], uuid.uuid4())
    assert not SkillProgress.objects.filter(learner=p, skill__slug="speaking").exists()


@pytest.mark.django_db
def test_dashboard_is_owner_scoped_and_history_paginated():
    from rest_framework.test import APIClient

    call_command("seed_demo")
    u = get_user_model().objects.create_user(username="journal")
    p = LearnerProfile.objects.create(user=u, display_name="Demo")
    version = LessonVersion.objects.filter(lesson__unit__level="A1").first()
    session = LessonSession.objects.create(learner=p, lesson_version=version)
    a = version.activities.first()
    submit_answer(session, a.id, "wrong", uuid.uuid4())
    c = APIClient()
    c.force_authenticate(u)
    assert c.get("/api/v1/learners/me/summary/").json()["practice_attempts"] == 1
    history = c.get("/api/v1/learners/me/history/").json()
    assert history["count"] == 1 and history["results"][0]["assessment_id"]
    other = get_user_model().objects.create_user(username="private")
    LearnerProfile.objects.create(user=other, display_name="Other")
    c.force_authenticate(other)
    assert c.get("/api/v1/learners/me/history/").json()["count"] == 0
    assert c.get("/api/v1/learners/me/summary/").json()["practice_attempts"] == 0
