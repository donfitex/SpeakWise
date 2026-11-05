from accounts.models import LearnerProfile
from curriculum.models import Activity, LessonVersion, Record
from django.db import models


class LessonSession(Record):
    learner = models.ForeignKey(LearnerProfile, on_delete=models.CASCADE)
    lesson_version = models.ForeignKey(LessonVersion, on_delete=models.PROTECT)
    position = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["learner", "lesson_version"], name="learner_lesson_session"
            )
        ]


class ActivityAttempt(Record):
    session = models.ForeignKey(LessonSession, on_delete=models.CASCADE, related_name="attempts")
    activity = models.ForeignKey(Activity, on_delete=models.PROTECT)
    request_id = models.UUIDField()
    answer = models.TextField()
    result = models.JSONField(default=dict)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["session", "request_id"], name="attempt_request_unique")
        ]


class TeacherTurn(Record):
    session = models.ForeignKey(LessonSession, on_delete=models.CASCADE, related_name="turns")
    speaker = models.CharField(
        max_length=10, choices=[("teacher", "Teacher"), ("learner", "Learner")]
    )
    content = models.TextField()
    activity = models.ForeignKey(Activity, on_delete=models.PROTECT, null=True, blank=True)
