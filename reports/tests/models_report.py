from datetime import datetime

from django.test import TestCase
from reports.models import Report
from reports.runtests.example.models import Organization
from reports.tasks import generate_document


class ReportModelTestCase(TestCase):
    def test_generate_document(self):
        start = datetime(2017, 1, 1, 12, 33)
        end = datetime(2017, 1, 2, 12, 33)
        org = Organization.objects.create(name="Org")
        report = Report.objects.create(
            report="example",
            organization=org,
            start_datetime=start,
            end_datetime=end,
            typ="pdf",
        )

        report.generate_document()

        report = Report.objects.get(pk=report.pk)
        self.assertEqual(report.document.read(), b"Some data")
        file_name = "org-example-report-2017-01-01-to-2017-01-02.pdf"
        self.assertTrue(report.document.name.endswith(file_name))

    def test_generate_document_idempotency(self):
        from unittest.mock import patch

        start = datetime(2017, 1, 1, 12, 33)
        end = datetime(2017, 1, 2, 12, 33)
        org = Organization.objects.create(name="Org2")
        report = Report.objects.create(
            report="example",
            organization=org,
            start_datetime=start,
            end_datetime=end,
            typ="pdf",
        )

        with patch.object(
            Report, "generate_document", wraps=report.generate_document
        ) as mock_generate:
            generate_document.apply(args=(report.pk,))
            report.refresh_from_db()
            self.assertEqual(report.status, Report.STATUS_COMPLETED)
            self.assertEqual(mock_generate.call_count, 1)

            # Report is already COMPLETED, so it should not be generated again
            generate_document.apply(args=(report.pk,))
            report.refresh_from_db()
            self.assertEqual(report.status, Report.STATUS_COMPLETED)
            self.assertEqual(mock_generate.call_count, 1)
