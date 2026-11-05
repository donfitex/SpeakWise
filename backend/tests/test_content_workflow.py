import pytest
from curriculum.models import LessonVersion
from curriculum.workflow import clone_version, decide, submit_review
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.management import call_command


@pytest.mark.django_db
def test_content_review_roles_versions_and_separate_reviewer():
    call_command("seed_demo")
    users = get_user_model()
    author = users.objects.create_superuser(
        username="author", email="a@example.test", password="test"
    )
    reviewer = users.objects.create_superuser(
        username="reviewer", email="r@example.test", password="test"
    )
    learner = users.objects.create_user(username="learner")
    published = LessonVersion.objects.first()
    with pytest.raises(PermissionDenied):
        clone_version(published, learner)
    draft = clone_version(published, author)
    assert draft.version == 2 and draft.status == "draft"
    draft.objective = "New objective"
    draft.save()
    review = submit_review(draft, author, "Synthetic content and typed alternatives checked.")
    with pytest.raises(ValidationError):
        decide(review, author, True, "Self review")
    a = draft.activities.first()
    a.prompt = "Changed after review"
    with pytest.raises(ValidationError):
        a.save()
    decide(review, reviewer, True, "Reviewed sample lesson; ready for advisory pilot.")
    published.refresh_from_db()
    draft.refresh_from_db()
    assert published.status == "archived" and draft.status == "published"
    assert published.objective != "New objective"
