import re
import unicodedata

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import ActivityAttempt, TeacherTurn


def normalize(text):
    return re.sub(r"[^\w\s]", "", unicodedata.normalize("NFKC", text).casefold()).strip().split()


ACTIVITY_HELP = {
    "grammar": "Check the subject and verb in the model.",
    "vocabulary": "Compare the meaning of the word with the example.",
    "listening": "Replay the model or read its caption, then find the key detail.",
    "reading": "Find the part of the text that supports your answer.",
    "sentence-building": "Compare the word order with the model sentence.",
    "writing": "This controlled exercise checks a model response; other valid wording may need human review.",
    "speaking": "Typed practice checks words only. Pronunciation has not been evaluated.",
}


def evaluate(activity, answer):
    correct = any(normalize(answer) == normalize(reference) for reference in activity.answers)
    return {
        "correct": correct,
        "feedback": "You matched the reference. Well done—try using it in your own conversation."
        if correct
        else f"Good practice. Try this model: {activity.example}. {activity.hint}",
        "confidence": "high" if correct else "medium",
        "evidence_type": "controlled-text-match",
        "rubric_version": activity.rubric.version,
        "scores": {"task-completion": 5 if correct else 1},
        "pronunciation_evaluated": False,
        "activity_type": activity.kind,
        "next_step": ACTIVITY_HELP[activity.kind],
        "reference": activity.example,
    }


def submit_answer(session, activity_id, answer, request_id):
    previous = session.attempts.filter(request_id=request_id).first()
    if previous:
        if str(previous.activity_id) != str(activity_id) or previous.answer != answer:
            raise ValidationError("This request key was already used for another answer.")
        return previous
    activities = list(session.lesson_version.activities.all())
    if session.completed_at or session.position >= len(activities):
        raise ValidationError("Lesson is complete.")
    activity = activities[session.position]
    if str(activity.id) != str(activity_id):
        raise ValidationError("Answer the current activity first. Refresh your lesson.")
    result = evaluate(activity, answer)
    attempt = ActivityAttempt.objects.create(
        session=session, activity=activity, request_id=request_id, answer=answer, result=result
    )
    TeacherTurn.objects.create(
        session=session, speaker="learner", content=answer, activity=activity
    )
    TeacherTurn.objects.create(
        session=session, speaker="teacher", content=result["feedback"], activity=activity
    )
    if result["correct"]:
        session.position += 1
        if session.position == len(activities):
            session.completed_at = timezone.now()
        session.save()
    return attempt


def representation(session):
    activities = list(session.lesson_version.activities.all())
    current = activities[session.position] if session.position < len(activities) else None
    return {
        "id": str(session.id),
        "title": session.lesson_version.lesson.title,
        "objective": session.lesson_version.objective,
        "explanation": session.lesson_version.explanation,
        "position": session.position,
        "total": len(activities),
        "turns": [
            {"speaker": t.speaker, "content": t.content}
            for t in session.turns.order_by("created_at", "id")[:100]
        ],
        "completed": bool(session.completed_at),
        "activity": {
            "id": str(current.id),
            "kind": current.kind,
            "prompt": current.prompt,
            "example": current.example,
            "hint": current.hint,
            "options": current.options,
            "cues": current.cues,
        }
        if current
        else None,
    }
