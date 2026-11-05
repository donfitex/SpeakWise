from accounts.models import LearnerProfile
from classroom.models import ActivityAttempt
from curriculum.models import Record, Rubric
from django.db import models
from speech.models import SpeechAttempt


class AssessmentResult(Record):
    attempt = models.OneToOneField(ActivityAttempt, on_delete=models.CASCADE, null=True, blank=True)
    speech_attempt = models.OneToOneField(
        SpeechAttempt, on_delete=models.CASCADE, null=True, blank=True
    )
    rubric = models.ForeignKey(Rubric, on_delete=models.PROTECT)
    rubric_version = models.PositiveIntegerField()
    scores = models.JSONField(default=dict)
    evidence = models.JSONField(default=list)
    confidence = models.CharField(max_length=30)
    evaluator_version = models.CharField(max_length=80)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(attempt__isnull=False, speech_attempt__isnull=True)
                    | models.Q(attempt__isnull=True, speech_attempt__isnull=False)
                ),
                name="assessment_one_attempt",
            )
        ]


class FeedbackReport(Record):
    learner = models.ForeignKey(LearnerProfile, on_delete=models.CASCADE)
    assessment = models.ForeignKey(AssessmentResult, on_delete=models.CASCADE)
    reason = models.CharField(max_length=1000)
    status = models.CharField(
        max_length=20, default="open", choices=[("open", "Open"), ("reviewed", "Reviewed")]
    )
