from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants import GENDER_TYPES, USER_STATUSES, USER_TYPES
from core.utils import generate_filename, phone_regex


class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    email_allowed = models.BooleanField(default=False)
    sms_allowed = models.BooleanField(default=False)
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_TYPES, null=True, blank=True
    )
    avatar = models.ImageField(
        upload_to=generate_filename("profile_images"), null=True, blank=True
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=20, db_index=True
    )
    status = models.PositiveSmallIntegerField(
        choices=USER_STATUSES, default=USER_STATUSES.active, db_index=True
    )
    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPES, default=USER_TYPES.default
    )
