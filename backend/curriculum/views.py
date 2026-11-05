from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Course, LessonVersion


@api_view(["GET"])
def courses(request):
    data = []
    for c in Course.objects.filter(published=True).order_by("created_at"):
        units = []
        for u in c.units.all():
            lessons = []
            for lesson in u.lessons.all():
                v = lesson.versions.filter(status="published").order_by("-version").first()
                if v:
                    lessons.append(
                        {
                            "id": str(v.id),
                            "lesson_id": str(lesson.id),
                            "title": lesson.title,
                            "objective": v.objective,
                            "minutes": v.estimated_minutes,
                            "prerequisites": [
                                str(x) for x in lesson.prerequisites.values_list("id", flat=True)
                            ],
                        }
                    )
            units.append({"id": str(u.id), "title": u.title, "level": u.level, "lessons": lessons})
        data.append({"id": str(c.id), "title": c.title, "version": c.version, "units": units})
    return Response({"results": data})


@api_view(["GET"])
def lesson(request, pk):
    v = get_object_or_404(
        LessonVersion, pk=pk, status="published", lesson__unit__course__published=True
    )
    return Response(
        {
            "id": str(v.id),
            "title": v.lesson.title,
            "objective": v.objective,
            "explanation": v.explanation,
            "accessibility_notes": v.accessibility_notes,
            "version": v.version,
            "minutes": v.estimated_minutes,
        }
    )
