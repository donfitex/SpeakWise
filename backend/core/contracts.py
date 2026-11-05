"""Explicit OpenAPI contracts for function-based endpoints. No answer keys are exposed."""

from drf_spectacular.utils import extend_schema

TEXT = {"type": "string"}
UUID = {"type": "string", "format": "uuid"}
NUMBER = {"type": "number"}
INTEGER = {"type": "integer"}
BOOLEAN = {"type": "boolean"}
JSON = {"type": "object", "additionalProperties": True}


def array(item):
    return {"type": "array", "items": item}


def obj(**fields):
    return {"type": "object", "properties": fields, "required": list(fields)}


def nullable(schema):
    return {**schema, "nullable": True}


ACTIVITY = obj(
    id=UUID, kind=TEXT, prompt=TEXT, example=TEXT, hint=TEXT, options=array(TEXT), cues=JSON
)
SESSION = obj(
    id=UUID,
    lesson_version=UUID,
    title=TEXT,
    objective=TEXT,
    explanation=TEXT,
    position=INTEGER,
    total=INTEGER,
    completed=BOOLEAN,
    activity=nullable(ACTIVITY),
    turns=array(obj(speaker=TEXT, content=TEXT)),
)
RESULT = obj(
    correct=BOOLEAN,
    feedback=TEXT,
    confidence=TEXT,
    evidence_type=TEXT,
    rubric_version=INTEGER,
    scores=JSON,
    pronunciation_evaluated=BOOLEAN,
    activity_type=TEXT,
    next_step=TEXT,
    reference=TEXT,
)
SPEECH = obj(
    id=UUID,
    status=TEXT,
    transcript=TEXT,
    duration_seconds=nullable(NUMBER),
    result=JSON,
    audio_retained=BOOLEAN,
    expires_at={"type": "string", "format": "date-time"},
)
PLACEMENT = obj(
    id=UUID,
    answered=INTEGER,
    total=INTEGER,
    question=nullable(obj(skill=TEXT, prompt=TEXT, options=array(TEXT))),
    result=nullable(
        obj(
            suggested_level=TEXT,
            confidence=TEXT,
            evidence=array(obj(skill=TEXT, correct=BOOLEAN)),
            explanation=TEXT,
        )
    ),
)
ERROR = obj(detail=TEXT)


def install():
    from accounts import views as accounts
    from accounts.serializers import ProfileSerializer
    from assessment import views as assessment
    from classroom import views as classroom
    from curriculum import views as curriculum
    from drf_spectacular.utils import inline_serializer
    from placement import views as placement
    from progress import views as progress
    from rest_framework import serializers
    from speech import views as speech

    from core.views import health

    def doc(view, response, request=None, status=200, description=None):
        if isinstance(request, dict) and "type" in request:
            request = {"application/json": request}
        extend_schema(
            request=request,
            responses={status: response, 400: ERROR, 403: ERROR, 404: ERROR, 429: ERROR},
            description=description,
        )(view)

    doc(health, obj(status=TEXT, service=TEXT))
    doc(accounts.csrf, obj(csrfToken=TEXT))
    doc(accounts.register, ProfileSerializer, accounts.RegisterSerializer, 201)
    doc(
        accounts.sign_in,
        ProfileSerializer,
        obj(username=TEXT, password={"type": "string", "writeOnly": True}),
    )
    doc(accounts.sign_out, None, status=204)
    doc(accounts.me, ProfileSerializer, ProfileSerializer)
    doc(accounts.consent, obj(granted=BOOLEAN, policy_version=TEXT), obj(granted=BOOLEAN))
    doc(accounts.password_reset, ERROR, obj(email={"type": "string", "format": "email"}))
    doc(
        accounts.reset_confirm,
        ERROR,
        obj(uid=TEXT, token=TEXT, password={"type": "string", "writeOnly": True}),
    )
    doc(
        accounts.data_controls,
        JSON,
        obj(
            password={"type": "string", "writeOnly": True},
            confirmation={"type": "string", "enum": ["DELETE"]},
        ),
        description="GET exports owner records. DELETE requires current password and DELETE confirmation; returns 204.",
    )
    doc(
        curriculum.courses,
        obj(
            results=array(
                obj(
                    id=UUID,
                    title=TEXT,
                    version=INTEGER,
                    units=array(
                        obj(
                            id=UUID,
                            title=TEXT,
                            level=TEXT,
                            lessons=array(
                                obj(
                                    id=UUID,
                                    lesson_id=UUID,
                                    title=TEXT,
                                    objective=TEXT,
                                    minutes=INTEGER,
                                    prerequisites=array(UUID),
                                )
                            ),
                        )
                    ),
                )
            )
        ),
    )
    doc(
        curriculum.lesson,
        obj(
            id=UUID,
            title=TEXT,
            objective=TEXT,
            explanation=TEXT,
            accessibility_notes=TEXT,
            version=INTEGER,
            minutes=INTEGER,
        ),
    )
    doc(placement.start, PLACEMENT, status=201)
    doc(placement.detail, PLACEMENT, obj(index=INTEGER, answer=TEXT))
    doc(
        classroom.start,
        SESSION,
        obj(lesson_version=UUID, review=BOOLEAN),
        201,
        description="Start/resume a published lesson. review is optional (default false). Existing sessions return 200.",
    )
    doc(classroom.detail, SESSION)
    doc(
        classroom.answer,
        obj(session=SESSION, attempt=obj(id=UUID, result=RESULT)),
        classroom.AnswerSerializer,
    )
    upload = inline_serializer(
        "SpeechUpload",
        fields={"audio": serializers.FileField(), "request_id": serializers.UUIDField()},
    )
    doc(speech.upload, SPEECH, {"multipart/form-data": upload}, 202)
    doc(
        speech.detail,
        SPEECH,
        description="Owner status/feedback. DELETE removes transcript/result/audio and returns 204.",
    )
    doc(
        progress.progress,
        obj(
            skills=array(
                obj(
                    skill=TEXT,
                    estimate=NUMBER,
                    evidence_count=INTEGER,
                    last_practised=TEXT,
                    next_review_due=TEXT,
                )
            ),
            note=TEXT,
        ),
    )
    doc(
        progress.recommendations,
        obj(lesson_version=nullable(UUID), reason=TEXT),
        description="When a lesson is available, title and review fields are also returned.",
    )
    doc(
        progress.summary,
        obj(
            completed_lessons=INTEGER,
            practice_attempts=INTEGER,
            recorded_practice_seconds=NUMBER,
            resume=array(obj(id=UUID, title=TEXT)),
        ),
    )
    doc(
        progress.history,
        obj(
            count=INTEGER,
            next=nullable(TEXT),
            previous=nullable(TEXT),
            results=array(
                obj(
                    id=UUID,
                    title=TEXT,
                    activity_type=TEXT,
                    created_at=TEXT,
                    result=RESULT,
                    assessment_id=nullable(UUID),
                )
            ),
        ),
    )
    doc(assessment.report, ERROR, obj(reason=TEXT), 201)
