from accounts.models import LearnerProfile
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import PlacementSession

QUESTIONS = [
    {
        "skill": "vocabulary",
        "prompt": "Choose a greeting.",
        "options": ["Hello", "Table", "Blue"],
        "answer": "Hello",
    },
    {
        "skill": "grammar",
        "prompt": "She ___ a teacher.",
        "options": ["am", "is", "are"],
        "answer": "is",
    },
    {
        "skill": "reading",
        "prompt": "Jo takes the bus because it is raining. Why does Jo take the bus?",
        "options": ["It is raining", "It is sunny", "Jo is tired"],
        "answer": "It is raining",
    },
    {
        "skill": "grammar",
        "prompt": "If I had more time, I ___ practise daily.",
        "options": ["would", "will", "am"],
        "answer": "would",
    },
]


def representation(session):
    i = len(session.answers)
    question = (
        {k: v for k, v in QUESTIONS[i].items() if k != "answer"} if i < len(QUESTIONS) else None
    )
    return {
        "id": str(session.id),
        "answered": i,
        "total": len(QUESTIONS),
        "question": question,
        "result": session.result or None,
    }


@api_view(["POST"])
def start(request):
    session = PlacementSession.objects.create(learner=LearnerProfile.objects.get(user=request.user))
    return Response(representation(session), status=201)


@api_view(["GET", "POST"])
@transaction.atomic
def detail(request, pk):
    session = get_object_or_404(
        PlacementSession.objects.select_for_update(), pk=pk, learner__user=request.user
    )
    if request.method == "POST":
        i = len(session.answers)
        if i >= len(QUESTIONS):
            return Response({"detail": "Placement is already complete."}, status=409)
        index = serializers.IntegerField(min_value=0).run_validation(request.data.get("index"))
        if index != i:
            return Response(
                {"detail": "This question has changed. Refresh and try again."}, status=409
            )
        answer = serializers.ChoiceField(choices=QUESTIONS[i]["options"]).run_validation(
            request.data.get("answer")
        )
        session.answers.append(
            {"skill": QUESTIONS[i]["skill"], "correct": answer == QUESTIONS[i]["answer"]}
        )
        if len(session.answers) == len(QUESTIONS):
            correct = sum(x["correct"] for x in session.answers)
            session.result = {
                "suggested_level": ["pre-A1", "A1", "A1", "A2", "B1"][correct],
                "confidence": "low",
                "evidence": session.answers,
                "explanation": "A short text diagnostic suggests a starting point, not a qualification. Listening and spoken performance were not measured. You can choose any starting level in My account.",
            }
        session.save()
    return Response(representation(session))
