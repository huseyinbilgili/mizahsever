import os
import uuid
from datetime import datetime

from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible

phone_regex = RegexValidator(
    regex=getattr(settings, "USER_PHONE_REGEX", r"^(05)\d{9}$"),
)


@deconstructible
class GenerateFilename(object):
    def __init__(self, path, ext=".jpg"):
        self.path = path
        self.ext = ext

    def __call__(self, instance, *args, **kwargs):
        filename = str(uuid.uuid4()) + self.ext
        datetime_str = datetime.now().strftime("%Y/%m/%d")
        return os.path.join(self.path, datetime_str, filename)


generate_filename = GenerateFilename
