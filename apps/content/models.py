from django.db import models

from apps.user.models import User
from core.constants import BASE_STATUSES
from core.models import AuthTimeStampedModel


class Category(AuthTimeStampedModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Video(AuthTimeStampedModel):
    title = models.CharField(max_length=225)
    description = models.TextField()
    cover_image = models.ImageField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField(upload_to="media/videos")

    class Meta:
        ordering = ("-created_at",)


class Comment(AuthTimeStampedModel):
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    answer = models.TextField()
    status = models.PositiveSmallIntegerField(
        choices=BASE_STATUSES, default=BASE_STATUSES.active, db_index=True
    )
