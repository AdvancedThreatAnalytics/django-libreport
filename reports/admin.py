from django.contrib import admin, messages
from django.db.models import Q

from .models import Report, ReportSchedule
from .tasks import generate_document


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    actions = ("regenerate_report",)
    list_display = (
        "id",
        "report",
        "typ",
        "created_by",
    )
    list_filter = ("organization",)

    def regenerate_report(self, request, queryset):
        """
        From the given queryset: only regenerate the reports which have an empty
        document, to avoid overwriting reports with valid documents generated.
        """
        regenerated_count = 0
        requested_count = queryset.count()

        for report in queryset.filter(Q(document="") | Q(document=None)):
            generate_document.apply_async(args=(report.id,), countdown=30)
            regenerated_count += 1

        msg = "Re-generating {} reports out of {}".format(
            regenerated_count, requested_count
        )

        if regenerated_count < requested_count:
            self.message_user(request, msg, messages.ERROR)
        else:
            self.message_user(request, msg, messages.SUCCESS)

    regenerate_report.short_description = "Re-generate selected Reports"


@admin.register(ReportSchedule)
class ReportScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "report",
        "name",
        "typ",
        "created_by",
    )
    list_filter = ("organization", "period")
    search_fields = (
        "name",
        "created_by__name",
        "created_by__email",
        "organization__psa_id",
    )
