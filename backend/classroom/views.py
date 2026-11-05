from accounts.models import LearnerProfile
from curriculum.models import LessonVersion
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import LessonSession
from .services import representation, submit_answer


@api_view(["POST"])
@transaction.atomic
def start(request):
    pk = serializers.UUIDField().run_validation(request.data.get("lesson_version"))
    version = get_object_or_404(
        LessonVersion, pk=pk, status="published", lesson__unit__course__published=True
    )
    learner = LearnerProfile.objects.select_for_update().get(user=request.user)
    required = set(version.lesson.prerequisites.values_list("id", flat=True))
    completed = set(
        LessonSession.objects.filter(learner=learner, completed_at__isnull=False).values_list(
            "lesson_version__lesson_id", flat=True
        )
    )
    if required - completed:
        return Response({"detail": "Complete the prerequisite lesson first."}, status=403)
    if not version.activities.exists():
        return Response({"detail": "This lesson has no published activities."}, status=409)
    review = serializers.BooleanField(default=False).run_validation(
        request.data.get("review", False)
    )
    session = LessonSession.objects.filter(
        learner=learner, lesson_version=version, completed_at__isnull=True
    ).first()
    if not session and not review:
        session = (
            LessonSession.objects.filter(learner=learner, lesson_version=version)
            .order_by("-created_at")
            .first()
        )
    created = not session
    if not session:
        session = LessonSession.objects.create(learner=learner, lesson_version=version)
    return Response(representation(session), status=201 if created else 200)


@api_view(["GET"])
def detail(request, pk):
    return Response(
        representation(get_object_or_404(LessonSession, pk=pk, learner__user=request.user))
    )


class AnswerSerializer(serializers.Serializer):
    activity_id = serializers.UUIDField()
    answer = serializers.CharField(max_length=4000, trim_whitespace=True)
    request_id = serializers.UUIDField()


@api_view(["POST"])
@transaction.atomic
def answer(request, pk):
    data = AnswerSerializer(data=request.data)
    data.is_valid(raise_exception=True)
    session = get_object_or_404(
        LessonSession.objects.select_for_update(), pk=pk, learner__user=request.user
    )
    attempt = submit_answer(session, **data.validated_data)
    return Response(
        {
            "session": representation(session),
            "attempt": {"id": str(attempt.id), "result": attempt.result},
        }
    )
