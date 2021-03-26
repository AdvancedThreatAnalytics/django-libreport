# Generated by Django 2.2.19 on 2021-03-25 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_auto_20201211_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='schedule',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='reports',
                to='reports.ReportSchedule'
            ),
        ),
        migrations.AddField(
            model_name='report',
            name='status',
            field=models.CharField(
                choices=[
                    ('running', 'Running'), ('completed', 'Completed'),
                    ('failed', 'Failed'), ('skipped', 'Skipped')
                ],
                default='running',
                max_length=256
            ),
        ),
    ]
