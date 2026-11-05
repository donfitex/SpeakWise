import uuid

from django.conf import settings
from django.db import models


class LearnerProfile(models.Model):
    LEVELS = [(v, v) for v in ["pre-A1", "A1", "A2", "B1"]]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=80)
    first_language = models.CharField(max_length=80, blank=True)
    level = models.CharField(max_length=8, choices=LEVELS, default="A1")
    goals = models.JSONField(default=list)
    pronunciation_model = models.CharField(
        max_length=30,
        choices=[("none", "No preference"), ("British", "British"), ("American", "American")],
        default="none",
    )
    daily_minutes = models.PositiveSmallIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ConsentRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    learner = models.ForeignKey(LearnerProfile, on_delete=models.CASCADE)
    policy_version = models.CharField(max_length=20, default="audio-v1")
    granted = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
