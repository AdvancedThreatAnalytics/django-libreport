# Django-LibReports

**Django app to allow creating custom reports easily.**

[![build-status-image]][travis]

# Overview

Django app to allow creating custom reports easily..

# Requirements

* Python (3.8)
* Django (2.2+)
* python-dateutil
* pychrome
* django-celery-beat
* jsonfield
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

# Development

### Setting up
Setup dependencies
```
pip install -r requirements.txt
```
### Running tests

```
python3 tests/runtests.py
```
