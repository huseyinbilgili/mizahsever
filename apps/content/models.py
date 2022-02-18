import uuid
from django.db import models

from apps.user.models import User
from core.constants import BASE_STATUSES, VIDEO_STATUSES
from core.fields import CreatingUserField
from core.models import AuthTimeStampedModel


class Tag(AuthTimeStampedModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Video(AuthTimeStampedModel):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, db_index=True, editable=False)
    title = models.CharField(max_length=225)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    cover_image = models.ImageField(upload_to="media/video_cover_images/")
    created_by = CreatingUserField(related_name="created_%(app_label)s_%(class)s_set", on_delete=models.PROTECT)
    video = models.FileField(upload_to="media/videos")
    tags = models.ManyToManyField(Tag)
    status = models.PositiveSmallIntegerField(choices=VIDEO_STATUSES, default=VIDEO_STATUSES.created, db_index=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

    def get_absolute_url(self):
        return self.slug


class Comment(AuthTimeStampedModel):
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    answer = models.TextField()
    status = models.PositiveSmallIntegerField(
        choices=BASE_STATUSES, default=BASE_STATUSES.active, db_index=True
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.commented_by.get_full_name()} - {self.video.title} - {self.answer}"
