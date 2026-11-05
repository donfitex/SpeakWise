from accounts.models import LearnerProfile
from curriculum.models import Record, Skill
from django.db import models


class SkillProgress(Record):
    learner = models.ForeignKey(LearnerProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    estimate = models.FloatField()
    evidence_count = models.PositiveIntegerField()
    last_practised = models.DateTimeField()
    next_review_due = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["learner", "skill"], name="learner_skill_unique")
        ]
