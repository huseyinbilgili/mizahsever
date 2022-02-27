import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
from django.conf import settings

from api.celery_schedule_conf import CELERYBEAT_SCHEDULE

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "api.settings",
)

app = Celery("api")

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)
app.conf.beat_schedule = CELERYBEAT_SCHEDULE
app.autodiscover_tasks(settings.INSTALLED_APPS)
