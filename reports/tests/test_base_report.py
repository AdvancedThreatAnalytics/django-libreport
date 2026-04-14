from datetime import date, timedelta
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from reports.base import BaseReport


class DeprecatedReport(BaseReport):
    id = "deprecated_example"
    name = "Deprecated Example"
    deprecation_date = date(2026, 1, 1)


class NonDeprecatedReport(BaseReport):
    id = "active_example"
    name = "Active Example"


class BaseReportDeprecationTestCase(TestCase):
    def test_non_deprecated_report_has_no_eol_date(self):
        report = NonDeprecatedReport()
        self.assertIsNone(report.eol_date)

    def test_non_deprecated_report_days_remaining_is_none(self):
        report = NonDeprecatedReport()
        self.assertIsNone(report.deprecation_days_remaining)

    def test_non_deprecated_report_is_not_deprecated(self):
        report = NonDeprecatedReport()
        self.assertFalse(report.is_deprecated)

    def test_non_deprecated_report_is_not_retired(self):
        report = NonDeprecatedReport()
        self.assertFalse(report.is_retired)

    def test_deprecated_report_eol_date(self):
        report = DeprecatedReport()
        expected = date(2026, 1, 1) + timedelta(days=90)
        self.assertEqual(report.eol_date, expected)

    def test_deprecated_report_is_deprecated(self):
        report = DeprecatedReport()
        self.assertTrue(report.is_deprecated)

    @patch("reports.base.timezone")
    def test_deprecated_report_days_remaining_during_grace_period(self, mock_tz):
        mock_tz.now.return_value = timezone.datetime(2026, 2, 1, tzinfo=timezone.utc)
        report = DeprecatedReport()
        # EOL = 2026-04-01, today = 2026-02-01 → 59 days remaining
        self.assertEqual(report.deprecation_days_remaining, 59)
        self.assertFalse(report.is_retired)

    @patch("reports.base.timezone")
    def test_deprecated_report_days_remaining_on_eol_date(self, mock_tz):
        mock_tz.now.return_value = timezone.datetime(2026, 4, 1, tzinfo=timezone.utc)
        report = DeprecatedReport()
        self.assertEqual(report.deprecation_days_remaining, 0)
        self.assertFalse(report.is_retired)

    @patch("reports.base.timezone")
    def test_deprecated_report_is_retired_after_eol(self, mock_tz):
        mock_tz.now.return_value = timezone.datetime(2026, 5, 1, tzinfo=timezone.utc)
        report = DeprecatedReport()
        self.assertTrue(report.deprecation_days_remaining < 0)
        self.assertTrue(report.is_retired)

    def test_grace_period_default(self):
        self.assertEqual(BaseReport._DEPRECATION_GRACE_PERIOD_DAYS, 90)
