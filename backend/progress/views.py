from accounts.models import LearnerProfile
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import SkillProgress
from .services import recommend


@api_view(["GET"])
def progress(request):
    learner = LearnerProfile.objects.get(user=request.user)
    rows = (
        SkillProgress.objects.filter(learner=learner)
        .select_related("skill")
        .order_by("skill__slug")
    )
    return Response(
        {
            "skills": [
                {
                    "skill": r.skill.title,
                    "estimate": r.estimate,
                    "evidence_count": r.evidence_count,
                    "last_practised": r.last_practised,
                    "next_review_due": r.next_review_due,
                }
                for r in rows
            ],
            "note": "Estimates describe recent controlled text tasks, not overall English mastery. Speech and listening quality are not inferred from text.",
        }
    )


@api_view(["GET"])
def recommendations(request):
    return Response(recommend(LearnerProfile.objects.get(user=request.user)))


@api_view(["GET"])
def history(request):
    from classroom.models import ActivityAttempt
    from rest_framework.pagination import PageNumberPagination

    attempts = (
        ActivityAttempt.objects.filter(session__learner__user=request.user)
        .select_related("activity", "assessmentresult", "session__lesson_version__lesson")
        .order_by("-created_at", "-id")
    )
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(attempts, request)
    results = []
    for a in page:
        assessment = getattr(a, "assessmentresult", None)
        results.append(
            {
                "id": str(a.id),
                "title": a.session.lesson_version.lesson.title,
                "activity_type": a.activity.kind,
                "created_at": a.created_at,
                "result": a.result,
                "assessment_id": str(assessment.id) if assessment else None,
            }
        )
    return paginator.get_paginated_response(results)


@api_view(["GET"])
def summary(request):
    from classroom.models import ActivityAttempt, LessonSession
    from django.db.models import Sum
    from speech.models import SpeechAttempt

    sessions = LessonSession.objects.filter(learner__user=request.user)
    return Response(
        {
            "completed_lessons": sessions.filter(completed_at__isnull=False)
            .values("lesson_version__lesson_id")
            .distinct()
            .count(),
            "practice_attempts": ActivityAttempt.objects.filter(session__in=sessions).count(),
            "recorded_practice_seconds": SpeechAttempt.objects.filter(
                session__in=sessions, status="complete"
            ).aggregate(total=Sum("duration_seconds"))["total"]
            or 0,
            "resume": [
                {"id": str(s.id), "title": s.lesson_version.lesson.title}
                for s in sessions.filter(completed_at__isnull=True)
                .select_related("lesson_version__lesson")
                .order_by("-updated_at")[:5]
            ],
        }
    )
