import io

import pytest
from django.test import override_settings
from speech.providers import ProviderUnavailable, pronunciation_evaluator, transcriber


def test_disabled_does_not_fabricate_a_transcript_or_score():
    with pytest.raises(ProviderUnavailable):
        transcriber().transcribe(io.BytesIO(b"test"))
    result = pronunciation_evaluator().evaluate(io.BytesIO(b"test"), "reference")
    assert not result.dimensions and result.confidence == "not-enough-evidence"


@override_settings(SPEECH_PROVIDER="mock", ALLOW_MOCK_SPEECH=True)
def test_mock_is_explicit_and_never_a_live_evaluation():
    assert transcriber().transcribe(io.BytesIO(b"test")).simulated


@override_settings(SPEECH_PROVIDER="mock", ALLOW_MOCK_SPEECH=False)
def test_mock_requires_explicit_test_enablement():
    with pytest.raises(ProviderUnavailable):
        transcriber().transcribe(io.BytesIO(b"test"))
