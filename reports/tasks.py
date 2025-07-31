import logging

from celery import shared_task
from celery.exceptions import MaxRetriesExceededError

from .models import Report, ReportSchedule

logger = logging.getLogger(__name__)


@shared_task(ignore_result=True, bind=True, default_retry_delay=1 * 60, acks_late=True)
def generate_document(self, report_id):
    """
    Generates the report document. Retry after 1 minute
    Idempotency: Only generate if not already completed, failed, or skipped.
    """
    try:
        report = Report.objects.get(pk=report_id)
    except Report.DoesNotExist as exc:
        self.retry(exc=exc, max_retries=3)
    try:
        # Idempotency check - don't overwrite existing reports
        if report.status in [Report.STATUS_COMPLETED, Report.STATUS_FAILED, Report.STATUS_SKIPPED]:
            logger.info(f"Report {report_id} already processed with status {report.status}, skipping generation.")
            return
        report.generate_document()
    except Exception as exc:
        logger.exception(f"Error generating report {report.report}, will retry")
        try:
            self.retry()
        except MaxRetriesExceededError:
            logger.exception(
                f"Error generating report {report.report}, no more retries"
            )
            report.status = Report.STATUS_FAILED
            report.save(update_fields=["status"])
            raise exc


@shared_task(ignore_result=True)
def schedule_task(report_schedule_id):
    report_schedule = ReportSchedule.objects.get(pk=report_schedule_id)
    report_schedule.schedule_report()
