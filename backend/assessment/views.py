from accounts.models import LearnerProfile
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import AssessmentResult, FeedbackReport


@api_view(["POST"])
def report(request, pk):
    assessment = get_object_or_404(
        AssessmentResult.objects.filter(
            Q(attempt__session__learner__user=request.user)
            | Q(speech_attempt__session__learner__user=request.user)
        ),
        pk=pk,
    )
    reason = serializers.CharField(max_length=1000).run_validation(request.data.get("reason"))
    FeedbackReport.objects.create(
        learner=LearnerProfile.objects.get(user=request.user), assessment=assessment, reason=reason
    )
    return Response(
        {
            "detail": "Your feedback report has been saved for review. You can retry the activity at any time."
        },
        status=201,
    )
