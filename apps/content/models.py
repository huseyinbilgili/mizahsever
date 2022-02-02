from django.db import models

from core.models import AuthTimeStampedModel
from core.user.models import User


class Category(AuthTimeStampedModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Video(AuthTimeStampedModel):
    title = models.CharField(max_length=225)
    description = models.TextField()
    cover_image = models.ImageField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
