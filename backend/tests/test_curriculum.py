import pytest
from curriculum.models import Activity, Course, LessonVersion
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_seed_idempotent_content_versioning_and_access():
    call_command("seed_demo")
    call_command("seed_demo")
    assert Course.objects.count() == 1 and Activity.objects.count() == 8
    v = LessonVersion.objects.first()
    v.objective = "Rewrite history"
    with pytest.raises(ValidationError):
        v.save()
    a = Activity.objects.first()
    a.prompt = "Rewrite history"
    with pytest.raises(ValidationError):
        a.save()
    client = APIClient()
    client.force_authenticate(get_user_model().objects.create_user(username="sample"))
    assert len(client.get("/api/v1/courses/").json()["results"][0]["units"]) == 4
    v = LessonVersion.objects.create(
        lesson=v.lesson, version=2, objective="Draft", explanation="Draft"
    )
    assert client.get(f"/api/v1/lessons/{v.id}/").status_code == 404
