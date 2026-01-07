# Django-LibReports

**Django app to allow creating custom reports easily.**

[![build-status-image]][travis]

# Overview

Django app to allow creating custom reports easily..

# Requirements

* Python (3.8)
* Django (3.2+)
* python-dateutil
* django-celery-beat
* pypandoc
* Chrome or Chromium web browser

# Installation

Install using `pip`...

    aws --profile production codeartifact login --tool pip --domain criticalstart --domain-owner 818476207984 --repository criticalstart_global
    pip install django-libreport

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

Install tox (if not already installed):
```
uv tool install tox --with tox-uv
```

### Running tests

Start the required services:
```
docker-compose up -d
```

Run tests with tox:
```
tox
```

Or run tests directly:
```
python3 reports/runtests/runtests.py
```

### Deploying
```
python -m build
aws --profile production codeartifact login --tool twine --domain criticalstart --domain-owner 818476207984 --repository criticalstart_global
twine upload --repository codeartifact dist/*
```
