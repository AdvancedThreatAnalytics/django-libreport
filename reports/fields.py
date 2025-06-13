from django.db import models


class ChoicesCharField(models.CharField):
    description = "A choices field that does not require migrations"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop("choices", None)
        return name, path, args, kwargs
