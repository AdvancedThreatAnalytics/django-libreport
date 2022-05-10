from django.contrib import admin, messages
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import quote
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import Report, ReportSchedule
from .tasks import generate_document


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "report",
        "typ",
        "created_by",
    )
    list_filter = ("organization",)
    actions = ("regenerate_report",)

    @property
    def generated(self):
        return bool(self.document)

    @property
    def urls(self):
        urls = super(ReportAdmin, self).urls
        urls.insert(0, self.rereun_url)  # this should be before generic view
        return urls

    @property
    def rereun_url(self):
        from django.urls import path

        info = self.model._meta.app_label, self.model._meta.model_name
        return path(
            "<path:object_id>/rerun/",
            self.admin_site.admin_view(self.rerun_view),
            name="%s_%s_rerun" % info,
        )

    def _redirect_to_change_view(self, object_id, request):
        opts = self.model._meta
        preserved_filters = self.get_preserved_filters(request)
        obj_url = reverse(
            "admin:%s_%s_change" % (opts.app_label, opts.model_name),
            args=(quote(object_id),),
            current_app=self.admin_site.name,
        )
        redirect_url = add_preserved_filters(
            {"preserved_filters": preserved_filters, "opts": opts}, obj_url
        )
        return HttpResponseRedirect(redirect_url)

    def rerun_view(self, request, object_id, extra_context=None):
        generate_document.apply_async(args=(object_id,))
        msg = _("Report Id: %s scheduled for regeneration" % (object_id,))
        self.message_user(request, msg, messages.SUCCESS)
        return self._redirect_to_change_view(object_id, request)

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
        "organization__name",
    )
