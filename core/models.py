from django.db import models
from django.utils import timezone


class CreatedTimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class TimeStampedModel(CreatedTimeStampedModel):
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuthTimeStampedModel(TimeStampedModel):
    class Meta:
        abstract = True
