# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-02 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0003_auto_20171119_1232"),
    ]

    operations = [
        migrations.AddField(
            model_name="reportschedule",
            name="name",
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name="reportschedule",
            name="report_datetime",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
