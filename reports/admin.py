from django.contrib import admin
from .models import Report, ReportSchedule


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'report', 'typ', 'created_by', 'deleted')
    list_filter = ('organization', 'deleted')


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
