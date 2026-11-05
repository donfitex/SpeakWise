from accounts.models import LearnerProfile
from curriculum.models import Record
from django.db import models


class PlacementSession(Record):
    learner = models.ForeignKey(LearnerProfile, on_delete=models.CASCADE)
    answers = models.JSONField(default=list)
    result = models.JSONField(default=dict)
