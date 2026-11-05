from accounts.models import ConsentRecord
from classroom.models import LessonSession
from curriculum.models import Activity, Record
from django.db import models


class SpeechAttempt(Record):
    session = models.ForeignKey(
        LessonSession, on_delete=models.CASCADE, related_name="speech_attempts"
    )
    activity = models.ForeignKey(Activity, on_delete=models.PROTECT)
    consent = models.ForeignKey(ConsentRecord, on_delete=models.PROTECT)
    request_id = models.UUIDField()
    audio = models.FileField(upload_to="processing/%Y/%m/%d/", max_length=250, blank=True)
    expires_at = models.DateTimeField()
    status = models.CharField(
        max_length=12,
        default="queued",
        choices=[(x, x) for x in ["queued", "processing", "complete", "failed", "deleted"]],
    )
    transcript = models.TextField(blank=True)
    duration_seconds = models.FloatField(null=True, blank=True)
    result = models.JSONField(default=dict)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["session", "request_id"], name="speech_request_unique")
        ]
