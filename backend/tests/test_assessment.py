import pytest
from assessment.services import validated_scores
from rest_framework.exceptions import ValidationError


class Rubric:
    dimensions = [{"key": "target-sound", "min": 1, "max": 5}]


def test_uncertain_simulated_or_missing_evidence_never_scores():
    for confidence, evidence, simulated in [
        ("low", ["sample"], False),
        ("high", [], False),
        ("high", ["sample"], True),
    ]:
        assert (
            validated_scores(Rubric(), {"target-sound": 5}, evidence, confidence, simulated) == {}
        )


def test_bounds_dimension_and_valid_evidence():
    assert validated_scores(Rubric(), {"target-sound": 3}, ["recording evidence"], "medium") == {
        "target-sound": 3
    }
    for scores in [{"target-sound": 6}, {"invented": 3}, {"target-sound": True}]:
        with pytest.raises(ValidationError):
            validated_scores(Rubric(), scores, ["evidence"], "high")
