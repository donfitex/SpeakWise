from django.contrib import admin

from .models import FeedbackReport


@admin.register(FeedbackReport)
class FeedbackReportAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "created_at"]
    readonly_fields = ["learner", "assessment", "reason", "created_at", "updated_at"]

    def has_add_permission(self, request):
        return False
