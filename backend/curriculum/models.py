import uuid

from django.core.exceptions import ValidationError
from django.db import models


class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Skill(Record):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Course(Record):
    title = models.CharField(max_length=160)
    audience = models.CharField(max_length=100, default="Learners aged 16 and over")
    version = models.PositiveIntegerField(default=1)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Unit(Record):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="units")
    title = models.CharField(max_length=160)
    level = models.CharField(max_length=8, choices=[(x, x) for x in ["pre-A1", "A1", "A2", "B1"]])
    sequence = models.PositiveIntegerField()

    class Meta:
        ordering = ["sequence", "id"]
        constraints = [models.UniqueConstraint(fields=["course", "sequence"], name="unit_sequence")]


class Lesson(Record):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=160)
    sequence = models.PositiveIntegerField()
    prerequisites = models.ManyToManyField("self", symmetrical=False, blank=True)

    class Meta:
        ordering = ["sequence", "id"]
        constraints = [models.UniqueConstraint(fields=["unit", "sequence"], name="lesson_sequence")]

    def __str__(self):
        return self.title


class LessonVersion(Record):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, related_name="versions")
    version = models.PositiveIntegerField()
    objective = models.TextField()
    explanation = models.TextField()
    estimated_minutes = models.PositiveSmallIntegerField(default=5)
    accessibility_notes = models.TextField(
        default="Typed responses, captions, and replay are available."
    )
    status = models.CharField(
        max_length=12,
        choices=[(x, x) for x in ["draft", "review", "published", "archived"]],
        default="draft",
    )
    skills = models.ManyToManyField(Skill)
    review_notes = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["lesson", "version"], name="lesson_version_unique")
        ]

    def save(self, *args, **kwargs):
        previous = type(self).objects.filter(pk=self.pk).first()
        if previous and previous.status in ["published", "archived"]:
            protected = [
                "lesson_id",
                "version",
                "objective",
                "explanation",
                "estimated_minutes",
                "accessibility_notes",
            ]
            if any(getattr(previous, f) != getattr(self, f) for f in protected):
                raise ValidationError("Published content is immutable; create a new draft version.")
        super().save(*args, **kwargs)


class Rubric(Record):
    title = models.CharField(max_length=100)
    version = models.PositiveIntegerField(default=1)
    dimensions = models.JSONField(default=list)

    def save(self, *args, **kwargs):
        if (
            self.pk
            and type(self).objects.filter(pk=self.pk).exists()
            and self.activities.filter(
                lesson_version__status__in=["published", "archived"]
            ).exists()
        ):
            raise ValidationError("A published rubric is immutable; create a new rubric version.")
        super().save(*args, **kwargs)


class Activity(Record):
    TYPES = [
        "grammar",
        "vocabulary",
        "listening",
        "reading",
        "sentence-building",
        "writing",
        "speaking",
    ]
    lesson_version = models.ForeignKey(
        LessonVersion, on_delete=models.CASCADE, related_name="activities"
    )
    sequence = models.PositiveIntegerField()
    kind = models.CharField(max_length=30, choices=[(x, x) for x in TYPES])
    prompt = models.TextField()
    example = models.TextField()
    hint = models.TextField()
    answers = models.JSONField(default=list)
    options = models.JSONField(default=list, blank=True)
    rubric = models.ForeignKey(Rubric, on_delete=models.PROTECT, related_name="activities")
    cues = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["sequence", "id"]
        constraints = [
            models.UniqueConstraint(fields=["lesson_version", "sequence"], name="activity_sequence")
        ]

    def clean(self):
        if self.kind not in self.TYPES:
            raise ValidationError("Unsupported activity type.")
        if (
            not isinstance(self.answers, list)
            or not self.answers
            or not all(isinstance(v, str) and v.strip() for v in self.answers)
        ):
            raise ValidationError("Activities require nonempty reference answers.")
        if self.kind not in ["speaking", "writing"] and not self.hint.strip():
            raise ValidationError("Provide a helpful hint.")

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.lesson_version.status in ["published", "archived"]:
            raise ValidationError("Published activities are immutable; edit a new draft.")
        super().save(*args, **kwargs)
