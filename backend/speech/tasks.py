import subprocess

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from .models import SpeechAttempt
from .providers import ProviderUnavailable, pronunciation_evaluator, transcriber


def remove_audio(job):
    if job.audio:
        job.audio.delete(save=False)
        job.audio = ""


def validated_duration(path):
    try:
        result = subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-nostdin",
                "-protocol_whitelist",
                "file,pipe",
                "-i",
                path,
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
            capture_output=True,
            timeout=15,
            check=True,
        )
    except (subprocess.SubprocessError, OSError) as exc:
        raise ProviderUnavailable(
            "Audio could not be read. Record again or type your answer."
        ) from exc
    duration = len(result.stdout) / 32000
    if duration < 0.2 or duration > 30.5:
        raise ProviderUnavailable("Record between 0.2 and 30 seconds.")
    return duration


@shared_task(soft_time_limit=75, time_limit=90)
def process_speech(pk):
    with transaction.atomic():
        job = SpeechAttempt.objects.select_for_update().get(pk=pk)
        if job.status != "queued":
            return
        job.status = "processing"
        job.save(update_fields=["status", "updated_at"])
    try:
        latest = job.consent.learner.consentrecord_set.order_by("-created_at").first()
        if job.expires_at <= timezone.now() or not latest or not latest.granted:
            raise ProviderUnavailable(
                "Consent was withdrawn or processing expired. Please use typed practice."
            )
        duration = validated_duration(job.audio.path)
        with job.audio.open("rb") as audio:
            transcript = transcriber().transcribe(audio)
        with job.audio.open("rb") as audio:
            evaluation = pronunciation_evaluator().evaluate(audio, job.activity.example)
        # Never score pronunciation from ASR or advance a lesson from mock output.
        with transaction.atomic():
            job = SpeechAttempt.objects.select_for_update().get(pk=pk)
            if job.status == "deleted":
                return
            job.status = "complete"
            job.duration_seconds = duration
            job.transcript = transcript.text[:4000]
            job.result = {
                "transcript_provider": transcript.provider,
                "simulated": transcript.simulated,
                "pronunciation_evaluated": False,
                "scores": {},
                "confidence": evaluation.confidence,
                "evidence": evaluation.evidence,
                "feedback": "Review the transcript, then use typed practice to continue. Pronunciation was not evaluated.",
            }
            remove_audio(job)
            job.save()
    except Exception:
        with transaction.atomic():
            job = SpeechAttempt.objects.select_for_update().get(pk=pk)
            if job.status == "deleted":
                return
            job.status = "failed"
            job.result = {
                "feedback": "Audio processing could not finish. Check recording length and quality, then record again or use typed practice. No pronunciation score was assigned.",
                "scores": {},
                "confidence": "not-enough-evidence",
            }
            remove_audio(job)
            job.save()


@shared_task
def purge_expired_audio():
    count = 0
    for job in SpeechAttempt.objects.filter(expires_at__lte=timezone.now()).exclude(audio=""):
        remove_audio(job)
        if job.status in ["queued", "processing"]:
            job.status = "failed"
            job.result = {
                "feedback": "Processing expired. Please record again or type your answer.",
                "scores": {},
            }
        job.save()
        count += 1
    return count
