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


class OfflineTranscriber:
    """Free bundled US-English ASR; approximate text only, never pronunciation grading."""

    def transcribe(self, audio):
        import array
        import os
        import subprocess

        from pocketsphinx import Decoder

        payload = audio.read(2 * 1024 * 1024 + 1)
        if len(payload) > 2 * 1024 * 1024:
            raise ProviderUnavailable("Recording exceeds the processing limit.")
        try:
            pcm = subprocess.run(
                [
                    "ffmpeg",
                    "-v",
                    "error",
                    "-nostdin",
                    "-i",
                    "pipe:0",
                    "-vn",
                    "-t",
                    "31",
                    "-f",
                    "s16le",
                    "-acodec",
                    "pcm_s16le",
                    "-ac",
                    "1",
                    "-ar",
                    "16000",
                    "pipe:1",
                ],
                input=payload,
                capture_output=True,
                check=True,
                timeout=15,
            ).stdout
            samples = array.array("h", pcm)
            if not samples or max(abs(n) for n in samples) < 128:
                raise ProviderUnavailable(
                    "The recording is too quiet. Try again or type your answer."
                )
            decoder = Decoder(logfn=os.devnull)
            decoder.start_utt()
            decoder.process_raw(pcm, False, True)
            decoder.end_utt()
            hypothesis = decoder.hyp()
            if not hypothesis or not hypothesis.hypstr.strip():
                raise ProviderUnavailable(
                    "No clear words were found. Try again or type your answer."
                )
            return Transcript(hypothesis.hypstr[:4000], "pocketsphinx")
        except (subprocess.SubprocessError, OSError) as exc:
            raise ProviderUnavailable(
                "Offline transcription could not finish. Please use typed practice."
            ) from exc


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
    if settings.SPEECH_PROVIDER == "pocketsphinx":
        return OfflineTranscriber()
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
