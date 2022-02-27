from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants import BASE_STATUSES, USER_TYPES
from core.utils import generate_filename


class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    email_allowed = models.BooleanField(default=False)
    sms_allowed = models.BooleanField(default=False)
    avatar = models.ImageField(
        upload_to=generate_filename("profile_images"), null=True, blank=True
    )
    status = models.PositiveSmallIntegerField(
        choices=BASE_STATUSES, default=BASE_STATUSES.active, db_index=True
    )
    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPES, default=USER_TYPES.default
    )
