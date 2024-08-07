# Django settings for django-libreports project.
import os

REPORT_PACKAGES = ["reports.runtests.example.my_reports"]

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = ["*"]

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

if "TRAVIS" in os.environ:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "travis",
            "USER": "postgres",
            "PASSWORD": "",
            "HOST": "localhost",
            "PORT": "",
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "docker",
            "USER": "docker",
            "PASSWORD": "docker",
            "HOST": "docker",
            "PORT": "",
        }
    }

TIME_ZONE = "Europe/London"
LANGUAGE_CODE = "en-GB"

SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_URL = "/media/"
MEDIA_ROOT = "media"

STATIC_URL = "/static/"
STATIC_ROOT = "static"

SECRET_KEY = "u@x-aj9(hoh#rb-^ymf#g2jx_hp0vj7u5#b@ag1n^seu9e!%cy"

TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django_celery_beat",
    "reports",
    "reports.runtests.example",
)

AUTH_USER_MODEL = "auth.User"

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
ORGANIZATION_MODEL = "example.Organization"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
