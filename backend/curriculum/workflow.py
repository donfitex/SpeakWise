from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import Max

from .models import Activity, ContentReview, Lesson, LessonVersion


def require(user, permission):
    if not user.is_active or not user.is_staff or not user.has_perm(permission):
        raise PermissionDenied


@transaction.atomic
def clone_version(version, user):
    require(user, "curriculum.add_lessonversion")
    Lesson.objects.select_for_update().get(pk=version.lesson_id)
    number = (version.lesson.versions.aggregate(n=Max("version"))["n"] or 0) + 1
    draft = LessonVersion.objects.create(
        lesson=version.lesson,
        version=number,
        objective=version.objective,
        explanation=version.explanation,
        estimated_minutes=version.estimated_minutes,
        accessibility_notes=version.accessibility_notes,
    )
    draft.skills.set(version.skills.all())
    for a in version.activities.all():
        Activity.objects.create(
            lesson_version=draft,
            sequence=a.sequence,
            kind=a.kind,
            prompt=a.prompt,
            example=a.example,
            hint=a.hint,
            answers=a.answers,
            options=a.options,
            rubric=a.rubric,
            cues=a.cues,
        )
    return draft


@transaction.atomic
def submit_review(version, user, notes):
    require(user, "curriculum.change_lessonversion")
    version = LessonVersion.objects.select_for_update().get(pk=version.pk)
    if (
        version.status != "draft"
        or not notes.strip()
        or not version.activities.exists()
        or not version.skills.exists()
    ):
        raise ValidationError("Submit a draft with activities, skills, and review notes.")
    for a in version.activities.all():
        a.full_clean()
    version.status = "review"
    version.save()
    return ContentReview.objects.create(version=version, requested_by=user, notes=notes)


@transaction.atomic
def decide(review, user, approve, notes):
    require(user, "curriculum.publish_content")
    review = ContentReview.objects.select_for_update().select_related("version").get(pk=review.pk)
    if review.status != "pending" or review.requested_by_id == user.id or not notes.strip():
        raise ValidationError("A different reviewer and review notes are required.")
    version = review.version
    if version.status != "review":
        raise ValidationError("Only submitted versions can be reviewed.")
    if approve:
        # Publishing a replacement does not rewrite historical session references.
        for old in version.lesson.versions.filter(status="published").exclude(pk=version.pk):
            old.status = "archived"
            old.save()
    version.status = "published" if approve else "draft"
    version.save()
    review.status = "approved" if approve else "rejected"
    review.reviewed_by = user
    review.notes += "\nReviewer: " + notes
    review.save()
    return version
