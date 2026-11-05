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
