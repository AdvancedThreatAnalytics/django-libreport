from django.core.files.base import ContentFile
from reports.models import BaseReport


class ExampleReport(BaseReport):
    """
    Example report
    """

    id = "example"
    name = "Example report"

    def generate(self, **kwargs):
        return ContentFile("Some data")
