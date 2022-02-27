import uuid

from django.db import models

from apps.user.models import User
from core.constants import BASE_STATUSES, CONTENT_MEDIA_STATUSES, CONTENT_STATUSES
from core.fields import CreatingUserField
from core.models import AuthTimeStampedModel


class Tag(AuthTimeStampedModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Content(AuthTimeStampedModel):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, db_index=True, editable=False
    )
    title = models.CharField(max_length=225)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    created_by = CreatingUserField(
        related_name="created_%(app_label)s_%(class)s_set", on_delete=models.PROTECT
    )
    tags = models.ManyToManyField(Tag)
    status = models.PositiveSmallIntegerField(
        choices=CONTENT_STATUSES, default=CONTENT_STATUSES.created, db_index=True
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

    def get_absolute_url(self):
        return self.slug


class ContentMedia(AuthTimeStampedModel):
    content = models.ForeignKey(
        Content, related_name="medias", on_delete=models.CASCADE
    )
    cover_image = models.ImageField(upload_to="media/content/cover_images")
    duration = models.PositiveSmallIntegerField(default=0)
    preview = models.FileField(
        upload_to="media/content/animations", null=True, blank=True
    )
    file = models.FileField(upload_to="media/contents")
    status = models.PositiveSmallIntegerField(
        choices=CONTENT_STATUSES, default=CONTENT_MEDIA_STATUSES.created, db_index=True
    )


class Comment(AuthTimeStampedModel):
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    answer = models.TextField()
    status = models.PositiveSmallIntegerField(
        choices=BASE_STATUSES, default=BASE_STATUSES.active, db_index=True
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.commented_by.get_full_name()} - {self.content.title} - {self.answer}"
