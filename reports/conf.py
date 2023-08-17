import sys
from django.conf import settings

_DEFAULT_ORG_MODEL = "report.Organization"
_DEFAULT_REPORT_PACKAGES = []
_DEFAULT_TYPE_CHOICES = (
    ("pdf", "PDF Document"),
    ("docx", "Word Document"),
    ("xlsx", "Excel Document"),
)

if "schemamigration" in sys.argv:
    ORG_MODEL = _DEFAULT_ORG_MODEL
    REPORT_PACKAGES = _DEFAULT_REPORT_PACKAGES
    TYPE_CHOICES = _DEFAULT_TYPE_CHOICES
else:
    ORG_MODEL = getattr(settings, "ORGANIZATION_MODEL", _DEFAULT_ORG_MODEL)
    REPORT_PACKAGES = getattr(settings, "REPORT_PACKAGES", _DEFAULT_REPORT_PACKAGES)
    TYPE_CHOICES = getattr(settings, "REPORT_TYPE_CHOICES", _DEFAULT_TYPE_CHOICES)
