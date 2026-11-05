from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.middleware.csrf import get_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from .models import ConsentRecord, LearnerProfile
from .serializers import ProfileSerializer


class AuthThrottle(UserRateThrottle):
    scope = "auth"


def csrf_check(request):
    SessionAuthentication().enforce_csrf(request)


@api_view(["GET"])
@permission_classes([AllowAny])
def csrf(request):
    return Response({"csrfToken": get_token(request)})


class RegisterSerializer(serializers.Serializer):
    username = serializers.RegexField(r"^[\w.@+-]+$", max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, max_length=128)
    display_name = serializers.CharField(max_length=80)
    eligible = serializers.BooleanField()

    def validate(self, data):
        if not data["eligible"]:
            raise serializers.ValidationError("This pilot is for learners aged 16 and over.")
        user = get_user_model()(username=data["username"], email=data["email"])
        try:
            validate_password(data["password"], user)
        except ValidationError as exc:
            raise serializers.ValidationError({"password": exc.messages}) from exc
        if get_user_model().objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError("This username is unavailable.")
        return data


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([AuthThrottle])
def register(request):
    csrf_check(request)
    data = RegisterSerializer(data=request.data)
    data.is_valid(raise_exception=True)
    try:
        with transaction.atomic():
            user = get_user_model().objects.create_user(
                username=data.validated_data["username"],
                email=data.validated_data["email"],
                password=data.validated_data["password"],
            )
            profile = LearnerProfile.objects.create(
                user=user, display_name=data.validated_data["display_name"]
            )
    except IntegrityError:
        return Response({"detail": "This username is unavailable."}, status=400)
    login(request, user)
    return Response(ProfileSerializer(profile).data, status=201)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([AuthThrottle])
def sign_in(request):
    csrf_check(request)
    credentials = LoginSerializer(data=request.data)
    credentials.is_valid(raise_exception=True)
    user = authenticate(request, **credentials.validated_data)
    if user is None:
        return Response({"detail": "Check your username and password."}, status=400)
    login(request, user)
    profile, _ = LearnerProfile.objects.get_or_create(
        user=user, defaults={"display_name": user.username}
    )
    return Response(ProfileSerializer(profile).data)


@api_view(["POST"])
def sign_out(request):
    logout(request)
    return Response(status=204)


@api_view(["GET", "PATCH"])
def me(request):
    profile, _ = LearnerProfile.objects.get_or_create(
        user=request.user, defaults={"display_name": request.user.username}
    )
    serializer = (
        ProfileSerializer(profile, data=request.data, partial=True)
        if request.method == "PATCH"
        else ProfileSerializer(profile)
    )
    if request.method == "PATCH":
        serializer.is_valid(raise_exception=True)
        serializer.save()
    return Response(serializer.data)


@api_view(["GET", "POST"])
def consent(request):
    profile = LearnerProfile.objects.get(user=request.user)
    if request.method == "POST":
        value = request.data.get("granted")
        if not isinstance(value, bool):
            return Response({"detail": "granted must be true or false."}, status=400)
        ConsentRecord.objects.create(learner=profile, granted=value)
        if not value:
            from speech.models import SpeechAttempt
            from speech.tasks import remove_audio

            for job in SpeechAttempt.objects.filter(
                session__learner=profile, status__in=["queued", "processing"]
            ):
                remove_audio(job)
                job.status = "deleted"
                job.transcript = ""
                job.result = {}
                job.save()
    latest = ConsentRecord.objects.filter(learner=profile).order_by("-created_at").first()
    return Response({"granted": bool(latest and latest.granted), "policy_version": "audio-v1"})


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([AuthThrottle])
def password_reset(request):
    csrf_check(request)
    if not getattr(settings, "PASSWORD_RESET_ENABLED", True):
        return Response(
            {"detail": "Password reset is unavailable in this pilot. Please contact the operator."},
            status=503,
        )
    email = serializers.EmailField().run_validation(request.data.get("email"))
    for user in get_user_model().objects.filter(email__iexact=email, is_active=True):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        send_mail(
            "Reset your SpeakWise password",
            f"Use this reset code in SpeakWise: {uid}/{token}",
            None,
            [user.email],
        )
    return Response({"detail": "If the account exists, reset instructions have been sent."})


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([AuthThrottle])
def reset_confirm(request):
    csrf_check(request)
    uid = serializers.CharField(max_length=128).run_validation(request.data.get("uid"))
    token = serializers.CharField(max_length=128).run_validation(request.data.get("token"))
    try:
        user = get_user_model().objects.get(pk=urlsafe_base64_decode(uid).decode())
        if not default_token_generator.check_token(user, token):
            raise ValueError
        password = serializers.CharField(max_length=128).run_validation(
            request.data.get("password")
        )
        validate_password(password, user)
    except (
        ValueError,
        TypeError,
        UnicodeDecodeError,
        get_user_model().DoesNotExist,
        ValidationError,
    ):
        return Response({"detail": "Invalid reset code or password."}, status=400)
    user.set_password(password)
    user.save()
    return Response({"detail": "Password changed. Please sign in."})


@api_view(["GET", "DELETE"])
@transaction.atomic
def data_controls(request):
    from classroom.models import LessonSession
    from speech.models import SpeechAttempt
    from speech.tasks import remove_audio

    profile = LearnerProfile.objects.get(user=request.user)
    if request.method == "DELETE":
        password = serializers.CharField(max_length=128).run_validation(
            request.data.get("password")
        )
        if (
            not request.user.check_password(password)
            or request.data.get("confirmation") != "DELETE"
        ):
            return Response({"detail": "Enter your password and DELETE to confirm."}, status=400)
        for job in SpeechAttempt.objects.select_for_update().filter(session__learner=profile):
            remove_audio(job)
            job.delete()
        user = request.user
        logout(request)
        user.delete()
        return Response(status=204)
    sessions = LessonSession.objects.filter(learner=profile).prefetch_related(
        "attempts", "speech_attempts"
    )
    return Response(
        {
            "profile": ProfileSerializer(profile).data,
            "consent": list(
                profile.consentrecord_set.values("policy_version", "granted", "created_at")
            ),
            "sessions": [
                {
                    "id": str(s.id),
                    "completed_at": s.completed_at,
                    "attempts": list(s.attempts.values("answer", "result", "created_at")),
                    "speech_results": list(
                        s.speech_attempts.values("transcript", "result", "created_at")
                    ),
                }
                for s in sessions
            ],
        }
    )
