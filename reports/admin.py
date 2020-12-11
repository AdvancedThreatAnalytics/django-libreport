from django.contrib import admin
from .models import Report, ReportSchedule


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'report', 'typ', 'created_by', 'deleted')
    list_filter = ('organization', 'deleted')


@admin.register(ReportSchedule)
class ReportScheduleAdmin(admin.ModelAdmin):
    pass
