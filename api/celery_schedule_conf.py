from __future__ import absolute_import

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    "process-videos": {
        "task": "apps.content.tasks.process_content_media",
        "schedule": crontab(minute="*/30"),
        "args": (),
    },
}
