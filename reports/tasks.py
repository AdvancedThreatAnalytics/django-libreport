import logging

from celery import shared_task
from celery.exceptions import MaxRetriesExceededError

from .models import Report, ReportSchedule

logger = logging.getLogger(__name__)


@shared_task(ignore_result=True, bind=True, default_retry_delay=1 * 60)
def generate_document(self, report_id):
    """
    Generates the report document. Retry after 1 minute
    """

    try:
        report = Report.objects.get(pk=report_id)
    except Report.DoesNotExist as exc:
        self.retry(exc=exc, max_retries=3)
    try:
        report.generate_document()
    except Exception as exc:
        logger.exception("Error generating report")
        try:
            self.retry()
        except MaxRetriesExceededError:
            report.status = Report.STATUS_FAILED
            self.save(update_fields=["status"])
            raise exc


@shared_task(ignore_result=True)
def schedule_task(report_schedule_id):
    report_schedule = ReportSchedule.objects.get(pk=report_schedule_id)
    report_schedule.schedule_report()
