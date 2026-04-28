import json
from datetime import date, datetime, timedelta
from unittest.mock import patch

from django.test import TestCase
from django_celery_beat.models import PeriodicTask

from reports.models import ReportSchedule
from reports.tasks import schedule_task
from reports.runtests.example.models import Organization


class ScheduleReportModelTestCase(TestCase):
    @patch("django.utils.timezone.now")
    def test_datetimes_by_period(self, mNow):
        mNow.return_value = datetime(2012, 12, 12, 12, 12, 12)
        org = Organization(name="Org")

        # Daily
        daily = ReportSchedule(organization=org)
        daily.period = ReportSchedule.PERIOD_DAILY
        start, end = daily.datetimes_by_period()
        self.assertEqual(start, datetime(2012, 12, 11, 0, 0, 0))
        self.assertEqual(end, datetime(2012, 12, 11, 23, 59, 59))

        # Weekly
        weekly = ReportSchedule(organization=org)
        weekly.period = ReportSchedule.PERIOD_WEEKLY
        start, end = weekly.datetimes_by_period()
        self.assertEqual(start, datetime(2012, 12, 3, 0, 0, 0))
        self.assertEqual(end, datetime(2012, 12, 9, 23, 59, 59))

        # Monthly
        monthly = ReportSchedule(organization=org)
        monthly.period = ReportSchedule.PERIOD_MONTHLY
        start, end = monthly.datetimes_by_period()
        self.assertEqual(start, datetime(2012, 11, 1, 0, 0, 0))
        self.assertEqual(end, datetime(2012, 11, 30, 23, 59, 59))

        # Quaterly
        quaterly = ReportSchedule(organization=org)
        quaterly.period = ReportSchedule.PERIOD_QUARTERLY
        start, end = quaterly.datetimes_by_period()
        self.assertEqual(start, datetime(2012, 7, 1, 0, 0, 0))
        self.assertEqual(end, datetime(2012, 9, 30, 23, 59, 59))

        # Yearly
        yearly = ReportSchedule(organization=org)
        yearly.period = ReportSchedule.PERIOD_YEARLY
        start, end = yearly.datetimes_by_period()
        self.assertEqual(start, datetime(2011, 1, 1, 0, 0, 0))
        self.assertEqual(end, datetime(2011, 12, 31, 23, 59, 59))

    @patch("django.utils.timezone.now")
    def test_datetimes_by_period_choosen_date(self, mNow):
        org = Organization(name="Org")
        mNow.return_value = datetime(2012, 12, 12, 12, 12, 12)

        # Daily
        daily = ReportSchedule(organization=org)
        daily.period = ReportSchedule.PERIOD_DAILY
        daily.report_datetime = datetime(2010, 10, 10, 10, 10, 10)
        start, end = daily.datetimes_by_period()
        self.assertEqual(start, datetime(2012, 12, 11, 10, 10, 11))
        self.assertEqual(end, datetime(2012, 12, 12, 10, 10, 10))

        # Weekly
        weekly = ReportSchedule(organization=org)
        weekly.period = ReportSchedule.PERIOD_WEEKLY
        weekly.report_datetime = datetime(2010, 10, 10, 10, 10, 10)
        start, end = weekly.datetimes_by_period()
        self.assertEqual(start, datetime(2012, 12, 5, 10, 10, 11))
        self.assertEqual(end, datetime(2012, 12, 12, 10, 10, 10))

        # Monthly
        monthly = ReportSchedule(organization=org)
        monthly.period = ReportSchedule.PERIOD_MONTHLY
        monthly.report_datetime = datetime(2010, 10, 10, 10, 10, 10)
        start, end = monthly.datetimes_by_period()
        self.assertEqual(start, datetime(2012, 11, 12, 10, 10, 11))
        self.assertEqual(end, datetime(2012, 12, 12, 10, 10, 10))

        # Yearly
        yearly = ReportSchedule(organization=org)
        yearly.period = ReportSchedule.PERIOD_YEARLY
        yearly.report_datetime = datetime(2010, 10, 10, 10, 10, 10)
        start, end = yearly.datetimes_by_period()
        self.assertEqual(start, datetime(2011, 12, 12, 10, 10, 11))
        self.assertEqual(end, datetime(2012, 12, 12, 10, 10, 10))

    def test_set_schedule(self):
        org = Organization.objects.create(name="Org")

        # Daily
        daily = ReportSchedule(organization=org)
        daily.period = ReportSchedule.PERIOD_DAILY
        daily.set_schedule()
        self.assertEqual(
            daily.schedule,
            {
                "day_of_month": "*",
                "day_of_week": "*",
                "hour": "6",
                "minute": "0",
                "month_of_year": "*",
            },
        )

        # Weekly
        weekly = ReportSchedule(organization=org)
        weekly.period = ReportSchedule.PERIOD_WEEKLY
        weekly.set_schedule()
        self.assertEqual(
            weekly.schedule,
            {
                "day_of_month": "*",
                "day_of_week": "1",
                "hour": "6",
                "minute": "0",
                "month_of_year": "*",
            },
        )

        # Monthly
        monthly = ReportSchedule(organization=org)
        monthly.period = ReportSchedule.PERIOD_MONTHLY
        monthly.set_schedule()
        self.assertEqual(
            monthly.schedule,
            {
                "day_of_month": "1",
                "day_of_week": "*",
                "hour": "6",
                "minute": "0",
                "month_of_year": "*",
            },
        )

        # Yearly
        yearly = ReportSchedule(organization=org)
        yearly.period = ReportSchedule.PERIOD_YEARLY
        yearly.set_schedule()
        self.assertEqual(
            yearly.schedule,
            {
                "day_of_month": "1",
                "day_of_week": "*",
                "hour": "6",
                "minute": "0",
                "month_of_year": "1",
            },
        )

        # Quarterly
        quarterly = ReportSchedule(organization=org)
        quarterly.period = ReportSchedule.PERIOD_QUARTERLY
        quarterly.set_schedule()
        self.assertEqual(
            quarterly.schedule,
            {
                "minute": "0",
                "hour": "6",
                "day_of_week": "*",
                "day_of_month": "1",
                "month_of_year": "*/3",
            },
        )

    def test_set_schedule_choosen_date(self):
        org = Organization.objects.create(name="Org")

        # Daily
        daily = ReportSchedule(organization=org)
        daily.period = ReportSchedule.PERIOD_DAILY
        daily.report_datetime = datetime(2010, 10, 10, 10, 10, 10)
        daily.set_schedule()
        self.assertEqual(
            daily.schedule,
            {
                "day_of_month": "*",
                "day_of_week": "*",
                "hour": "10",
                "minute": "10",
                "month_of_year": "*",
            },
        )

        # Weekly
        weekly = ReportSchedule(organization=org)
        weekly.period = ReportSchedule.PERIOD_WEEKLY
        # This is a Sunday
        weekly.report_datetime = datetime(2010, 10, 10, 10, 10, 10)
        weekly.set_schedule()
        self.assertEqual(
            weekly.schedule,
            {
                "day_of_month": "*",
                "day_of_week": "0",
                "hour": "10",
                "minute": "10",
                "month_of_year": "*",
            },
        )

        # Monthly
        monthly = ReportSchedule(organization=org)
        monthly.period = ReportSchedule.PERIOD_MONTHLY
        monthly.report_datetime = datetime(2010, 10, 10, 10, 10, 10)
        monthly.set_schedule()
        self.assertEqual(
            monthly.schedule,
            {
                "day_of_month": "10",
                "day_of_week": "*",
                "hour": "10",
                "minute": "10",
                "month_of_year": "*",
            },
        )

        # Quarterly
        quarterly = ReportSchedule(organization=org)
        quarterly.period = ReportSchedule.PERIOD_QUARTERLY
        quarterly.report_datetime = datetime(2010, 10, 10, 10, 10, 10)
        quarterly.set_schedule()
        self.assertEqual(
            quarterly.schedule,
            {
                "day_of_month": "10",
                "day_of_week": "*",
                "hour": "10",
                "minute": "10",
                "month_of_year": "*/3",
            },
        )

        # Yearly
        yearly = ReportSchedule(organization=org)
        yearly.period = ReportSchedule.PERIOD_YEARLY
        yearly.report_datetime = datetime(2010, 10, 10, 10, 10, 10)
        yearly.set_schedule()
        self.assertEqual(
            yearly.schedule,
            {
                "day_of_month": "10",
                "day_of_week": "*",
                "hour": "10",
                "minute": "10",
                "month_of_year": "10",
            },
        )

    def test_quarterly_task_no_datetime_returns_valid_schedule(self):
        org = Organization.objects.create(name="Org")

        # Quarterly
        quarterly = ReportSchedule(organization=org)
        quarterly.period = ReportSchedule.PERIOD_QUARTERLY

        # Test that when report_datetime is None, the schedule is valid
        quarterly.report_datetime = None
        quarterly.set_schedule()

        # Should run at 6:00AM, first day of the month, every 3 months
        self.assertEqual(
            quarterly.schedule,
            {
                "day_of_month": "1",
                "day_of_week": "*",
                "hour": "6",
                "minute": "0",
                "month_of_year": "*/3",
            },
        )

    def test_periodic_task_kwargs(self):
        org = Organization.objects.create(name="Org")

        schedule = ReportSchedule(organization=org)
        schedule.period = ReportSchedule.PERIOD_DAILY
        schedule.set_schedule()
        schedule.set_periodic_task()

        task = schedule.periodic_task
        # Make sure django-celery-beat can properly load kwargs
        json.loads(task.kwargs)

    @patch.object(ReportSchedule, "schedule_report")
    def test_schedule_task_runs_for_active_report(self, mock_schedule_report):
        """schedule_report must be called for a report with no retirement date."""
        org = Organization.objects.create(name="ActiveOrg")
        schedule = ReportSchedule.objects.create(
            report="example", typ="pdf", organization=org
        )
        schedule.set_schedule()
        schedule_task(schedule.pk)
        mock_schedule_report.assert_called_once()

    @patch("reports.tasks.REPORTS")
    @patch.object(ReportSchedule, "schedule_report")
    def test_schedule_task_skipped_when_report_is_retired(
        self, mock_schedule_report, mock_reports
    ):
        """schedule_report must not be called once the retirement date has passed."""
        from reports.base import BaseReport

        class RetiredReport(BaseReport):
            id = "retired_test"
            name = "Retired Test"
            retirement_date = date.today() - timedelta(days=1)

        mock_reports.get.return_value = RetiredReport
        self.assertTrue(RetiredReport().is_retired)

        org = Organization.objects.create(name="RetiredOrg")
        schedule = ReportSchedule.objects.create(
            report="example", typ="pdf", organization=org
        )
        schedule.set_schedule()
        schedule_task(schedule.pk)

        mock_schedule_report.assert_not_called()

    @patch("reports.tasks.REPORTS")
    @patch.object(ReportSchedule, "schedule_report")
    def test_schedule_task_runs_during_grace_period(
        self, mock_schedule_report, mock_reports
    ):
        """schedule_report must be called when retirement date is still in the future."""
        from reports.base import BaseReport

        class GracePeriodReport(BaseReport):
            id = "grace_test"
            name = "Grace Period Test"
            retirement_date = date.today() + timedelta(days=30)

        mock_reports.get.return_value = GracePeriodReport

        org = Organization.objects.create(name="GraceOrg")
        schedule = ReportSchedule.objects.create(
            report="example", typ="pdf", organization=org
        )
        schedule.set_schedule()
        schedule_task(schedule.pk)

        mock_schedule_report.assert_called_once()
