from datetime import timedelta

from assessment.models import AssessmentResult
from classroom.models import LessonSession
from curriculum.models import LessonVersion, Skill
from django.utils import timezone

from .models import SkillProgress


def update_from_attempt(attempt):
    # Typed speaking is not evidence of pronunciation, fluency, or listening ability.
    if attempt.activity.kind in ["speaking", "listening"]:
        return
    skill = Skill.objects.filter(slug=attempt.activity.kind).first()
    if not skill:
        return
    evidence = (
        AssessmentResult.objects.filter(
            attempt__session__learner=attempt.session.learner,
            attempt__activity__kind=attempt.activity.kind,
            evaluator_version="controlled-text-v1",
            confidence__in=["medium", "high"],
        )
        .exclude(scores={})
        .order_by("-created_at", "-id")
    )
    recent = list(evidence[:5])
    if not recent:
        return
    estimate = sum(r.scores["task-completion"] for r in recent) / len(recent)
    last = recent[0].created_at
    days = 1 if estimate < 4 else 3 if len(recent) < 3 else 7
    SkillProgress.objects.update_or_create(
        learner=attempt.session.learner,
        skill=skill,
        defaults={
            "estimate": estimate,
            "evidence_count": evidence.count(),
            "last_practised": last,
            "next_review_due": last + timedelta(days=days),
        },
    )


def recommend(learner):
    versions = list(
        LessonVersion.objects.filter(status="published", lesson__unit__course__published=True)
        .select_related("lesson__unit")
        .order_by("lesson__unit__sequence", "lesson__sequence", "-version")
    )
    done = set(
        LessonSession.objects.filter(learner=learner, completed_at__isnull=False).values_list(
            "lesson_version__lesson_id", flat=True
        )
    )
    for progress in (
        SkillProgress.objects.filter(learner=learner, next_review_due__lte=timezone.now())
        .select_related("skill")
        .order_by("next_review_due", "skill__slug")
    ):
        for v in versions:
            if v.skills.filter(pk=progress.skill_id).exists():
                return {
                    "lesson_version": str(v.id),
                    "title": v.lesson.title,
                    "review": True,
                    "reason": f"Review {progress.skill.title.lower()}: your next practice is due based on recent controlled exercises.",
                }
    for v in versions:
        if (
            v.lesson.unit.level == learner.level
            and v.lesson_id not in done
            and not set(v.lesson.prerequisites.values_list("id", flat=True)) - done
        ):
            return {
                "lesson_version": str(v.id),
                "title": v.lesson.title,
                "review": False,
                "reason": f"A new lesson at your chosen {learner.level} starting level.",
            }
    return {
        "lesson_version": None,
        "reason": "You have completed the available lessons at your chosen level. Review a lesson or choose another level in My account.",
    }
