from api.celery import app
from apps.content.models import ContentMedia
from apps.content.pipelines import ContentMediaProcessPipeline
from core.constants import CONTENT_MEDIA_STATUSES
from core.tasks import LockTask


@app.task(base=LockTask)
def process_content_media():
    queryset = ContentMedia.objects.filter(status=CONTENT_MEDIA_STATUSES.created)
    for content_media in queryset:
        ContentMediaProcessPipeline(content_media=content_media).run()
