from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .models import Activity, ContentReview, Course, Lesson, LessonVersion, Rubric, Skill, Unit
from .workflow import clone_version, decide, submit_review


@admin.register(LessonVersion)
class VersionAdmin(admin.ModelAdmin):
    list_display = ["lesson", "version", "status", "estimated_minutes"]
    list_filter = ["status", "lesson__unit__level"]
    search_fields = ["lesson__title", "objective"]
    readonly_fields = ["status"]
    actions = ["new_draft", "send_for_review", "archive"]

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != "draft":
            return [f.name for f in self.model._meta.fields] + ["skills"]
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description="Clone selected versions as new drafts")
    def new_draft(self, request, queryset):
        for v in queryset:
            clone_version(v, request.user)

    @admin.action(description="Submit drafts with review notes")
    def send_for_review(self, request, queryset):
        for v in queryset:
            try:
                submit_review(v, request.user, v.review_notes)
            except ValidationError as exc:
                self.message_user(request, str(exc), messages.ERROR)

    @admin.action(description="Archive published versions")
    def archive(self, request, queryset):
        if not request.user.has_perm("curriculum.publish_content"):
            self.message_user(request, "Publisher permission required.", messages.ERROR)
            return
        for v in queryset.filter(status="published"):
            v.status = "archived"
            v.save()
            ContentReview.objects.create(
                version=v,
                requested_by=request.user,
                reviewed_by=request.user,
                status="archived",
                notes="Archived by staff action.",
            )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["lesson_version", "sequence", "kind", "prompt"]
    list_filter = ["kind", "lesson_version__status"]

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.lesson_version.status != "draft":
            return [f.name for f in self.model._meta.fields]
        return []

    def has_delete_permission(self, request, obj=None):
        return bool(
            obj
            and obj.lesson_version.status == "draft"
            and super().has_delete_permission(request, obj)
        )


@admin.register(ContentReview)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["version", "requested_by", "reviewed_by", "status", "created_at"]
    readonly_fields = [
        "version",
        "requested_by",
        "reviewed_by",
        "status",
        "created_at",
        "updated_at",
    ]
    actions = ["approve", "reject"]

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + (["notes"] if obj and obj.status != "pending" else [])

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description="Approve and publish (different reviewer required)")
    def approve(self, request, queryset):
        self.review(request, queryset, True)

    @admin.action(description="Reject and return to draft")
    def reject(self, request, queryset):
        self.review(request, queryset, False)

    def review(self, request, queryset, approve):
        for r in queryset:
            try:
                decide(r, request.user, approve, r.notes)
            except ValidationError as exc:
                self.message_user(request, str(exc), messages.ERROR)


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ["title", "version"]

    def get_readonly_fields(self, request, obj=None):
        if (
            obj
            and obj.activities.filter(
                lesson_version__status__in=["review", "published", "archived"]
            ).exists()
        ):
            return ["title", "version", "dimensions"]
        return []

    def has_delete_permission(self, request, obj=None):
        return bool(
            obj and not obj.activities.exists() and super().has_delete_permission(request, obj)
        )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "unit", "sequence"]

    def get_readonly_fields(self, request, obj=None):
        return (
            ["title", "unit", "sequence", "prerequisites"]
            if obj and obj.versions.exclude(status="draft").exists()
            else []
        )


admin.site.register([Course, Unit, Skill])
