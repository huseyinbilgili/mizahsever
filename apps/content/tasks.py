import logging

from api.celery import app
from apps.content.models import ContentMedia
from apps.content.pipelines import ContentMediaProcessPipeline
from core.constants import CONTENT_MEDIA_STATUSES
from core.tasks import LockTask

logger = logging.getLogger(__name__)


@app.task(base=LockTask)
def process_content_media():
    queryset = ContentMedia.objects.filter(status=CONTENT_MEDIA_STATUSES.created)
    for content_media in queryset:
        try:
            ContentMediaProcessPipeline(content_media=content_media).run()
        except Exception as exc:
            logger.warning(
                f"Could not process content media. [{content_media.id}]",
                extra=dict(error_message=str(exc)),
            )
