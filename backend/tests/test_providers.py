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


@override_settings(SPEECH_PROVIDER="pocketsphinx")
def test_free_offline_adapter_transcribes_synthetic_command_without_scores():
    import subprocess

    # Synthetic model voice only; this verifies an actual decoder, not scoring quality.
    wav = subprocess.run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-f",
            "lavfi",
            "-i",
            "flite=text=go forward ten meters",
            "-ar",
            "16000",
            "-ac",
            "1",
            "-f",
            "wav",
            "pipe:1",
        ],
        capture_output=True,
        check=True,
    ).stdout
    result = transcriber().transcribe(io.BytesIO(wav))
    assert result.provider == "pocketsphinx" and not result.simulated
    assert result.text.startswith("go forward")
    assert (
        not pronunciation_evaluator().evaluate(io.BytesIO(wav), "go forward ten meters").dimensions
    )


@override_settings(SPEECH_PROVIDER="pocketsphinx")
def test_offline_adapter_rejects_silence():
    import wave

    out = io.BytesIO()
    with wave.open(out, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes(b"\0\0" * 16000)
    with pytest.raises(ProviderUnavailable):
        transcriber().transcribe(io.BytesIO(out.getvalue()))
