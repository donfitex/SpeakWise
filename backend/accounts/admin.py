from django.contrib import admin

from .models import ConsentRecord, LearnerProfile


@admin.register(LearnerProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "level", "created_at"]
    readonly_fields = [
        "user",
        "display_name",
        "first_language",
        "level",
        "goals",
        "pronunciation_model",
        "daily_minutes",
        "created_at",
        "updated_at",
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ConsentRecord)
class ConsentAdmin(admin.ModelAdmin):
    list_display = ["id", "policy_version", "granted", "created_at"]
    readonly_fields = ["learner", "policy_version", "granted", "created_at"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
