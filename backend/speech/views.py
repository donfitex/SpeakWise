import uuid
from datetime import timedelta

from accounts.models import ConsentRecord
from classroom.models import LessonSession
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from .models import SpeechAttempt
from .tasks import process_speech, remove_audio


class SpeechThrottle(UserRateThrottle):
    scope = "speech"


def representation(job):
    return {
        "id": str(job.id),
        "status": job.status,
        "transcript": job.transcript,
        "duration_seconds": job.duration_seconds,
        "result": job.result,
        "audio_retained": bool(job.audio),
        "expires_at": job.expires_at,
    }


@api_view(["POST"])
@throttle_classes([SpeechThrottle])
@transaction.atomic
def upload(request, pk):
    session = get_object_or_404(
        LessonSession.objects.select_for_update(), pk=pk, learner__user=request.user
    )
    key = serializers.UUIDField().run_validation(request.data.get("request_id"))
    previous = SpeechAttempt.objects.filter(session=session, request_id=key).first()
    if previous:
        return Response(representation(previous))
    consent = ConsentRecord.objects.filter(learner=session.learner).order_by("-created_at").first()
    if not consent or not consent.granted:
        return Response({"detail": "Audio processing requires your consent."}, status=403)
    activity = session.lesson_version.activities.all()[
        session.position : session.position + 1
    ].first()
    if session.completed_at or not activity or activity.kind != "speaking":
        return Response({"detail": "This activity does not accept recordings."}, status=400)
    audio = request.FILES.get("audio")
    if not audio or not 1 <= audio.size <= 2 * 1024 * 1024:
        return Response({"detail": "Choose an audio file up to 2 MB."}, status=400)
    suffix = {
        "audio/webm": ".webm",
        "audio/ogg": ".ogg",
        "audio/mp4": ".m4a",
        "audio/wav": ".wav",
        "audio/x-wav": ".wav",
    }.get(audio.content_type.split(";")[0])
    if not suffix:
        return Response({"detail": "Use WebM, Ogg, MP4, or WAV audio."}, status=400)
    session.save(update_fields=["updated_at"])
    audio.name = str(uuid.uuid4()) + suffix
    job = SpeechAttempt.objects.create(
        session=session,
        activity=activity,
        consent=consent,
        request_id=key,
        audio=audio,
        expires_at=timezone.now() + timedelta(minutes=10),
    )

    def enqueue():
        try:
            process_speech.delay(str(job.id))
        except Exception:
            current = SpeechAttempt.objects.get(pk=job.pk)
            remove_audio(current)
            current.status = "failed"
            current.result = {"feedback": "Speech queue unavailable. Please use typed practice."}
            current.save()

    transaction.on_commit(enqueue)
    return Response(representation(job), status=202)


@api_view(["GET", "DELETE"])
@transaction.atomic
def detail(request, pk):
    job = get_object_or_404(
        SpeechAttempt.objects.select_for_update(), pk=pk, session__learner__user=request.user
    )
    if request.method == "DELETE":
        remove_audio(job)
        job.transcript = ""
        job.result = {}
        job.status = "deleted"
        job.save()
        return Response(status=204)
    return Response(representation(job))
