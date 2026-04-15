from datetime import date, timedelta

from django.test import TestCase

from reports.base import BaseReport


class RetiringReport(BaseReport):
    id = "retiring_example"
    name = "Retiring Example"
    retirement_date = date(2026, 7, 8)


class ActiveReport(BaseReport):
    id = "active_example"
    name = "Active Example"


class BaseReportRetirementTestCase(TestCase):
    def test_retirement_date_defaults_to_none(self):
        report = ActiveReport()
        self.assertIsNone(report.retirement_date)

    def test_retirement_date_can_be_set(self):
        report = RetiringReport()
        self.assertEqual(report.retirement_date, date(2026, 7, 8))

    def test_is_retired_false_when_no_date(self):
        report = ActiveReport()
        self.assertFalse(report.is_retired)

    def test_is_retired_false_when_date_in_future(self):
        report = RetiringReport()
        report.retirement_date = date.today() + timedelta(days=30)
        self.assertFalse(report.is_retired)

    def test_is_retired_true_when_date_today(self):
        report = RetiringReport()
        report.retirement_date = date.today()
        self.assertTrue(report.is_retired)

    def test_is_retired_true_when_date_in_past(self):
        report = RetiringReport()
        report.retirement_date = date.today() - timedelta(days=1)
        self.assertTrue(report.is_retired)
