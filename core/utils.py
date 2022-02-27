import os
import uuid
from datetime import datetime

from django.utils.deconstruct import deconstructible


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
