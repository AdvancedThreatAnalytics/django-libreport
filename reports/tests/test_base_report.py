from datetime import date

from django.test import TestCase

from reports.base import BaseReport


class RetiringReport(BaseReport):
    id = "retiring_example"
    name = "Retiring Example"
    retiring_date = date(2026, 7, 8)


class ActiveReport(BaseReport):
    id = "active_example"
    name = "Active Example"


class BaseReportRetiringDateTestCase(TestCase):
    def test_retiring_date_defaults_to_none(self):
        report = ActiveReport()
        self.assertIsNone(report.retiring_date)

    def test_retiring_date_can_be_set(self):
        report = RetiringReport()
        self.assertEqual(report.retiring_date, date(2026, 7, 8))
