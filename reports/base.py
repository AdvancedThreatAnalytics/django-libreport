import base64
import sys
import tempfile
from datetime import timedelta

from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
from pypandoc import convert_text
from socket import gethostbyname

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = _ver[0] == 2

#: Python 3.x?
is_py3 = _ver[0] == 3

if is_py2:
    from urlparse import urlparse
elif is_py3:
    from urllib.parse import urlparse


class BaseReport(object):
    id = ""
    name = ""
    deprecation_date = None

    # Number of days after deprecation_date before the report is fully retired.
    _DEPRECATION_GRACE_PERIOD_DAYS = 90

    @property
    def eol_date(self):
        """The date the report becomes fully retired, or ``None``."""
        if self.deprecation_date is None:
            return None
        return self.deprecation_date + timedelta(
            days=self._DEPRECATION_GRACE_PERIOD_DAYS
        )

    @property
    def deprecation_days_remaining(self):
        """Days until EOL.

        Returns a positive int during the grace period, ``0`` on the EOL date,
        a negative int after EOL, or ``None`` if the report is not deprecated.
        """
        if self.eol_date is None:
            return None
        return (self.eol_date - timezone.now().date()).days

    @property
    def is_deprecated(self):
        """``True`` if the report has a deprecation date set."""
        return self.deprecation_date is not None

    @property
    def is_retired(self):
        """``True`` if the report is past its EOL date."""
        days = self.deprecation_days_remaining
        return days is not None and days < 0

    def get_report_name(self, **kwargs):
        return " ".join([kwargs["organization"].name, self.id.capitalize(), "Report"])

    def get_report_filename(self, **kwargs):
        return "{0} {1} to {2}.{3}".format(
            self.get_report_name(**kwargs),
            kwargs["start_datetime"].date(),
            kwargs["end_datetime"].date(),
            kwargs["typ"],
        )

    def markdown_to_doc(self, markdown, typ, reference=None):
        """
        :param markdown: markdown document as a string
        :param typ: document conversion output extension
        :param reference: path to the reference docx, if different from default
        :return: path to a temporary file
        """

        with tempfile.NamedTemporaryFile(suffix=".{0}".format(typ)) as temp:
            extra_args = ["--dpi=180"]
            if typ == "docx":
                if reference:
                    extra_args.append("--reference-doc={}".format(reference))
                extra_args.append("--toc")
            convert_text(
                markdown,
                typ,
                "markdown_phpextra",
                outputfile=temp.name,
                extra_args=extra_args,
            )
            with open(temp.name, "rb") as document:
                return ContentFile(document.read())
