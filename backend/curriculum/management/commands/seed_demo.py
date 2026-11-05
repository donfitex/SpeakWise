from django.core.management.base import BaseCommand
from django.db import transaction

from curriculum.models import Activity, Course, Lesson, LessonVersion, Rubric, Skill, Unit

LESSONS = [
    (
        "pre-A1",
        "A warm hello",
        "Use a greeting and introduce yourself.",
        "Say “Hello” to begin. “My name is Alex” introduces you.",
        ["vocabulary", "speaking"],
        [
            (
                "Choose a greeting.",
                "Hello",
                "Hello",
                "Try a friendly greeting.",
                ["Hello", "Goodbye"],
            ),
            (
                "Introduce yourself using the model name Alex.",
                "My name is Alex",
                "My name is Alex",
                "Start with “My name is…”",
                [],
            ),
        ],
    ),
    (
        "A1",
        "Everyday sentences",
        "Use am, is, and are in simple sentences.",
        "Use “am” with I, “is” with he/she/it, and “are” with you/we/they.",
        ["grammar", "sentence-building"],
        [
            ("I ___ a learner.", "am", "I am a learner.", "The subject is I.", ["am", "is", "are"]),
            (
                "Put these words in order: English / learning / am / I",
                "I am learning English",
                "I am learning English",
                "Begin with I, then am.",
                [],
            ),
        ],
    ),
    (
        "A2",
        "Listen and understand",
        "Find a detail and use it in a response.",
        "Listen for the main detail. You can read the model text as an accessible alternative.",
        ["listening", "reading"],
        [
            (
                "Model: The train leaves at nine. What time does it leave?",
                "nine",
                "The train leaves at nine.",
                "Listen for the time.",
                ["nine", "ten", "eleven"],
            ),
            (
                "Read: Mina walks to work because her office is nearby. Why does she walk?",
                "Her office is nearby",
                "Mina walks to work because her office is nearby.",
                "Find the reason after because.",
                [],
            ),
        ],
    ),
    (
        "B1",
        "A clear introduction",
        "Organize a short introduction with a clear pause.",
        "Introduce your name, say what you do, and give a purpose. Pause between ideas so listeners can follow.",
        ["writing", "speaking"],
        [
            (
                "Use the model to write an introduction for Alex.",
                "My name is Alex and I am learning English",
                "My name is Alex and I am learning English",
                "Join the name and purpose with and.",
                [],
            ),
            (
                "Read the model, pausing after Alex. Typed practice is also welcome.",
                "My name is Alex. I am learning English.",
                "My name is Alex. I am learning English.",
                "Pause between the two sentences.",
                [],
            ),
        ],
    ),
]


class Command(BaseCommand):
    help = "Create synthetic, advisory pilot lessons; never real learner data."

    @transaction.atomic
    def handle(self, *args, **options):
        if Course.objects.filter(title="Everyday English · Sample track").exists():
            self.stdout.write("Demo content already exists; no changes.")
            return
        c = Course.objects.create(title="Everyday English · Sample track", published=True)
        rubric = Rubric.objects.create(
            title="Controlled text practice",
            dimensions=[
                {
                    "key": "task-completion",
                    "min": 1,
                    "max": 5,
                    "description": "5: matches the reference; 1: needs a retry. Text evidence only.",
                }
            ],
        )
        for i, (level, title, objective, explanation, kinds, activities) in enumerate(LESSONS, 1):
            u = Unit.objects.create(
                course=c, title=f"{level} · Everyday English", level=level, sequence=i
            )
            lesson = Lesson.objects.create(unit=u, title=title, sequence=1)
            v = LessonVersion.objects.create(
                lesson=lesson,
                version=1,
                objective=objective,
                explanation=explanation,
                review_notes="Synthetic sample; educational review pending.",
            )
            for j, (kind, (prompt, answer, example, hint, options)) in enumerate(
                zip(kinds, activities), 1
            ):
                skill, _ = Skill.objects.get_or_create(
                    slug=kind, defaults={"title": kind.replace("-", " ").title()}
                )
                v.skills.add(skill)
                Activity.objects.create(
                    lesson_version=v,
                    sequence=j,
                    kind=kind,
                    prompt=prompt,
                    answers=[answer],
                    example=example,
                    hint=hint,
                    options=options,
                    rubric=rubric,
                )
            v.status = "published"
            v.save()
        self.stdout.write(self.style.SUCCESS("Created four synthetic sample lessons."))
