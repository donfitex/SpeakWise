from rest_framework.exceptions import ValidationError

from .models import AssessmentResult


def validated_scores(rubric, scores, evidence, confidence, simulated=False):
    if simulated or confidence not in ["medium", "high"] or not evidence:
        return {}
    dimensions = {d["key"]: d for d in rubric.dimensions}
    validated = {}
    for key, score in scores.items():
        d = dimensions.get(key)
        if (
            not d
            or not isinstance(score, (int, float))
            or isinstance(score, bool)
            or not d["min"] <= score <= d["max"]
        ):
            raise ValidationError("Score outside the versioned task rubric.")
        validated[key] = score
    return validated


def record_text(attempt):
    r = attempt.result
    evidence = [
        {
            "kind": "controlled-text-match",
            "matched": r["correct"],
            "note": "No pronunciation diagnosis. Reference matching can reject other valid wording.",
        }
    ]
    return AssessmentResult.objects.get_or_create(
        attempt=attempt,
        defaults={
            "rubric": attempt.activity.rubric,
            "rubric_version": r["rubric_version"],
            "scores": validated_scores(
                attempt.activity.rubric, r["scores"], evidence, r["confidence"]
            ),
            "evidence": evidence,
            "confidence": r["confidence"],
            "evaluator_version": "controlled-text-v1",
        },
    )[0]


def record_speech(job):
    r = job.result
    return AssessmentResult.objects.get_or_create(
        speech_attempt=job,
        defaults={
            "rubric": job.activity.rubric,
            "rubric_version": job.activity.rubric.version,
            "scores": validated_scores(
                job.activity.rubric,
                r.get("scores", {}),
                r.get("evidence", []),
                r.get("confidence", "not-enough-evidence"),
                r.get("simulated", False),
            ),
            "evidence": r.get("evidence", []),
            "confidence": r.get("confidence", "not-enough-evidence"),
            "evaluator_version": "disabled-pronunciation-v1",
        },
    )[0]
