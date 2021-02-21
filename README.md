# Django-LibReports

**Django app to allow creating custom reports easily.**

[![build-status-image]][travis]

# Overview

Django app to allow creating custom reports.

# Requirements

* Django (2.2+)
* python-dateutil
* pathlib 
* pychrome
* django-celery-beat
* pypandoc
* Chrome or Chromium web browser

# Installation

Install using `pip`...

    pip install django-libreport
    OR 
    pip install git+https://github.com/AdvancedThreatAnalytics/django-libreport.git

Example settings:

    CHROME_URL = 'http://localhost:9222'
    ORGANIZATION_MODEL = 'myapp.Organization'
    REPORT_PACKAGES = ('myapp.reports', )  # Packages were reports can be found
    INSTALLED_APPS = (
        ...
        'django_celery_beat',
        'reports',
    )

For generating PDF reports you must have a Chrome/Chromium browser instance running:

    google-chrome --remote-debugging-port=9222

or headless mode:

    google-chrome --headless --disable-gpu --remote-debugging-port=9222

You will then have to create an API to manage these. More docs to come...

That's it, we're done!

[build-status-image]: https://secure.travis-ci.org/AdvancedThreatAnalytics/django-libreports.png?branch=master
[travis]: http://travis-ci.org/AdvancedThreatAnalytics/django-libreports?branch=master

## Breaking Changes
### 0.1.2
If you have Django < 2.2, this upgrade will NOT work. Don't upgrade. 
The following instructions apply only if you have any existing reports and data. Otherwise, feel free to skip the entire section below. 

0.1.2 introduces breaking changes with how JSONField is used. Previously the package `jsonfield` was doing db transformation from `text` field type (in Postgres) to `json`. This has not been necessary for a while now. Here is how you can upgrade

Update your database first from `text` to `jsonb` type. Specifically you need to update two columns in two different tables

```shell
SELECT 
   table_name, 
   column_name, 
   data_type 
FROM 
   information_schema.columns
WHERE 
   table_name = 'reports_report';
   
   table_name   |   column_name   |        data_type
----------------+-----------------+--------------------------
 reports_report | id              | integer
 reports_report | report          | character varying
 reports_report | typ             | character varying
 reports_report | created_at      | timestamp with time zone
 reports_report | emails          | ARRAY
 reports_report | name            | character varying
 reports_report | start_datetime  | timestamp with time zone
 reports_report | end_datetime    | timestamp with time zone
 reports_report | config          | text
 reports_report | document        | character varying
 reports_report | created_by_id   | integer
 reports_report | organization_id | integer
(12 rows)

ALTER TABLE reports_report
    ALTER COLUMN config TYPE JSONB USING config::JSONB;

   table_name   |   column_name   |        data_type
----------------+-----------------+--------------------------
 reports_report | id              | integer
 reports_report | report          | character varying
 reports_report | typ             | character varying
 reports_report | created_at      | timestamp with time zone
 reports_report | emails          | ARRAY
 reports_report | name            | character varying
 reports_report | start_datetime  | timestamp with time zone
 reports_report | end_datetime    | timestamp with time zone
 reports_report | config          | jsonb
 reports_report | document        | character varying
 reports_report | created_by_id   | integer
 reports_report | organization_id | integer
(12 rows)
```

You need to convert any existing `str` data in the database to JSON appropriately. You can do this using Django Shell. Data conversion.
```python
import json
from reports.models import Report

for report in Report.objects.all():
    if isinstance(report.config, dict):
        continue
    value = json.loads(report.config)
    report.config = dict() or value
    report.save(update_fields=['config', ])

```

For table `reports_reportschedule`, you'll need to repeat most of the steps.
```text
SELECT 
   table_name, 
   column_name, 
   data_type 
FROM 
   information_schema.columns
WHERE 
   table_name = 'reports_reportschedule';

       table_name       |   column_name    |        data_type
------------------------+------------------+--------------------------
 reports_reportschedule | id               | integer
 reports_reportschedule | report           | character varying
 reports_reportschedule | typ              | character varying
 reports_reportschedule | created_at       | timestamp with time zone
 reports_reportschedule | emails           | ARRAY
 reports_reportschedule | schedule         | text
 reports_reportschedule | period           | character varying
 reports_reportschedule | created_by_id    | integer
 reports_reportschedule | organization_id  | integer
 reports_reportschedule | periodic_task_id | integer
 reports_reportschedule | config           | text
 reports_reportschedule | name             | character varying
 reports_reportschedule | report_datetime  | timestamp with time zone
(13 rows)
  
ALTER TABLE reports_reportschedule
    ALTER COLUMN schedule TYPE JSONB USING schedule::JSONB; 
ALTER TABLE reports_reportschedule
    ALTER COLUMN config TYPE JSONB USING config::JSONB;


       table_name       |   column_name    |        data_type
------------------------+------------------+--------------------------
 reports_reportschedule | id               | integer
 reports_reportschedule | report           | character varying
 reports_reportschedule | typ              | character varying
 reports_reportschedule | created_at       | timestamp with time zone
 reports_reportschedule | emails           | ARRAY
 reports_reportschedule | schedule         | jsonb
 reports_reportschedule | period           | character varying
 reports_reportschedule | created_by_id    | integer
 reports_reportschedule | organization_id  | integer
 reports_reportschedule | periodic_task_id | integer
 reports_reportschedule | config           | jsonb
 reports_reportschedule | name             | character varying
 reports_reportschedule | report_datetime  | timestamp with time zone
(13 rows) 
```

Data conversion.
```python
import json
from reports.models import ReportSchedule

for schedule in ReportSchedule.objects.all():
    if isinstance(schedule.schedule, dict) and isinstance(schedule.config, dict):
        continue
    print(schedule.id, schedule.schedule, schedule.config)

for schedule in ReportSchedule.objects.all():
    if not isinstance(schedule.schedule, dict):
        new_schedule = json.loads(schedule.schedule)
        if not new_schedule:
            new_schedule = dict()
    if not isinstance(schedule.config, dict):
        new_config = json.load(schedule.config)
        if not new_config:
            new_config = dict()
    schedule.save(update_fields=['schedule', 'config'])
```

### Redoing database structure
New migrations have been generated. You should apply these to avoid any conflicts, if you have existing data. The process is simple 

Delete the existing migrations
```text
SELECT * from django_migrations WHERE app='reports';
DELETE FROM django_migrations WHERE app='reports';
```
Fake apply the new migration. You are `fake`ing the new migration because the previous instructions for conversion already have made changes to the database, and it is in the right state. 

```text
python manage.py migrate reports 0001_initial --fake
```
After applying you should see
```text
python manage.py showmigrations reports --list
reports
 [X] 0001_initial
```
