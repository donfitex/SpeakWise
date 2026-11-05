"""Separate replaceable providers. Transcription never proves pronunciation quality."""

from dataclasses import dataclass
from typing import BinaryIO, Protocol

from django.conf import settings


class ProviderUnavailable(Exception):
    pass


@dataclass(frozen=True)
class Transcript:
    text: str
    provider: str
    simulated: bool = False


@dataclass(frozen=True)
class Evaluation:
    dimensions: dict
    evidence: list
    confidence: str
    provider: str
    simulated: bool = False


class Transcriber(Protocol):
    def transcribe(self, audio: BinaryIO) -> Transcript: ...


class Synthesizer(Protocol):
    def synthesize(self, text: str) -> bytes: ...


class PronunciationEvaluator(Protocol):
    def evaluate(self, audio: BinaryIO, reference: str) -> Evaluation: ...


class Aligner(Protocol):
    def align(self, audio: BinaryIO, transcript: str) -> list: ...


class DisabledProvider:
    def transcribe(self, audio):
        raise ProviderUnavailable("Transcription is not configured. Please use typed practice.")

    def synthesize(self, text):
        raise ProviderUnavailable("Model audio is unavailable. Use the caption.")

    def evaluate(self, audio, reference):
        return Evaluation(
            {},
            ["No calibrated pronunciation evaluator is configured."],
            "not-enough-evidence",
            "disabled",
        )

    def align(self, audio, transcript):
        return []


class MockTranscriber:
    def transcribe(self, audio):
        return Transcript("Synthetic test transcript", "mock", simulated=True)


class OpenAITranscriber:
    def transcribe(self, audio):
        from openai import OpenAI

        if not settings.SPEECH_API_KEY:
            raise ProviderUnavailable("Transcription is unavailable. Please use typed practice.")
        try:
            client = OpenAI(api_key=settings.SPEECH_API_KEY, timeout=30, max_retries=1)
            response = client.audio.transcriptions.create(
                model=settings.SPEECH_TRANSCRIPTION_MODEL, file=audio
            )
            return Transcript(response.text, "openai")
        except Exception as exc:
            raise ProviderUnavailable(
                "Transcription could not finish. Please retry or type your answer."
            ) from exc


def transcriber():
    if settings.SPEECH_PROVIDER == "openai":
        return OpenAITranscriber()
    if settings.SPEECH_PROVIDER == "mock" and settings.ALLOW_MOCK_SPEECH:
        return MockTranscriber()
    return DisabledProvider()


def synthesizer():
    return DisabledProvider()


def pronunciation_evaluator():
    return DisabledProvider()


def aligner():
    return DisabledProvider()
