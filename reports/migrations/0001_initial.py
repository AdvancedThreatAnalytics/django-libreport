# Generated by Django 2.2.13 on 2021-02-21 11:38
import django.utils.timezone
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import migrations, models

import reports.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("django_celery_beat", "0011_auto_20190508_0153"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.ORGANIZATION_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ReportSchedule",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=64)),
                (
                    "report",
                    models.CharField(
                        choices=[],
                        max_length=64,
                    ),
                ),
                (
                    "typ",
                    models.CharField(
                        choices=[("xlsx", "Excel Document")], max_length=32
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("config", models.JSONField(blank=True, default=dict)),
                (
                    "emails",
                    ArrayField(
                        base_field=models.EmailField(max_length=255),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                ("schedule", models.JSONField(blank=True, default=dict)),
                (
                    "period",
                    models.CharField(
                        choices=[
                            ("daily", "Daily"),
                            ("weekly", "Weekly"),
                            ("monthly", "Monthly"),
                            ("quarterly", "Quarterly"),
                            ("yearly", "Yearly"),
                        ],
                        default="weekly",
                        max_length=32,
                    ),
                ),
                ("report_datetime", models.DateTimeField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.ORGANIZATION_MODEL,
                    ),
                ),
                (
                    "periodic_task",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="django_celery_beat.PeriodicTask",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Report",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=64)),
                (
                    "report",
                    models.CharField(
                        choices=[],
                        max_length=64,
                    ),
                ),
                (
                    "typ",
                    models.CharField(
                        choices=[
                            ("pdf", "PDF Document"),
                            ("docx", "Word Document"),
                            ("xlsx", "Excel Document"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("config", models.JSONField(blank=True, default=dict)),
                (
                    "emails",
                    ArrayField(
                        base_field=models.EmailField(max_length=255),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                ("start_datetime", models.DateTimeField()),
                ("end_datetime", models.DateTimeField()),
                (
                    "document",
                    models.FileField(
                        blank=True,
                        max_length=1024,
                        null=True,
                        upload_to=reports.models.report_upload_to,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.ORGANIZATION_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Report",
                "verbose_name_plural": "Reports",
            },
        ),
    ]
