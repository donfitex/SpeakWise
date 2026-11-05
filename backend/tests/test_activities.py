import pytest
from classroom.services import evaluate
from curriculum.models import Activity
from django.core.management import call_command


@pytest.mark.django_db
@pytest.mark.parametrize("kind", Activity.TYPES)
def test_each_activity_type_reports_task_specific_evidence(kind):
    call_command("seed_demo")
    a = Activity.objects.filter(kind=kind).first()
    assert a is not None
    result = evaluate(a, "  " + a.answers[0].upper() + "!  ")
    assert result["correct"] and result["scores"] == {"task-completion": 5}
    assert result["activity_type"] == kind and result["reference"] and result["next_step"]
    assert not result["pronunciation_evaluated"]
    retry = evaluate(a, "unrelated response")
    assert not retry["correct"] and a.hint in retry["feedback"]
