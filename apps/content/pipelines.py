import os
import uuid

from django.utils.text import slugify
from moviepy.editor import VideoFileClip

from apps.content.models import Comment, Content, ContentMedia
from core.constants import CONTENT_MEDIA_STATUSES, CONTENT_STATUSES
from core.utils import generate_filename


class ContentMediaProcessPipeline:
    def __init__(self, content_media):
        self.instance = content_media
        self.clip = VideoFileClip(filename=self.instance.file.path)
        self.tmp_filename = uuid.uuid4()
        self.tmp_file_paths = []

    def set_status(self):
        self.instance.status = CONTENT_MEDIA_STATUSES.ready

    def set_duration(self):
        self.instance.duration = self.clip.duration

    def set_preview(self):
        tmp_filepath = f"media/content/tmp/previews/{self.tmp_filename}.gif"
        sub_clip = self.clip.subclip(0, 5)
        sub_clip.write_gif(tmp_filepath)
        self.instance.preview = tmp_filepath
        self.tmp_file_paths.append(tmp_filepath)

    def set_cover_image(self):
        tmp_filepath = f"media/content/tmp/cover_images/{self.tmp_filename}.png"
        self.clip.save_frame(
            filename=tmp_filepath,
            t=self.clip.duration / 2,
        )
        self.instance.cover_image = tmp_filepath
        self.tmp_file_paths.append(tmp_filepath)

    def delete_tmp_preview(self):
        for tmp_filepath in self.tmp_file_paths:
            os.remove(tmp_filepath)

    def run(self):
        self.set_duration()
        self.set_preview()
        self.delete_tmp_preview()
        self.instance.save()
        return self.instance


class ContentCreatePipeline:
    def __init__(self, title, description, created_by, tags, file):
        self.title = title
        self.description = description
        self.created_by = created_by
        self.tags = tags
        self.file = file
        self._content = None
        self._content_media = None

    @property
    def content(self):
        return self._content

    @property
    def content_media(self):
        return self._content_media

    def create_content_media(self):
        self._content_media = ContentMedia.objects.create(content=self.content, file=self.file)

    def create(self):
        self._content = Content.objects.create(
            title=self.title,
            slug=slugify(self.title),
            description=self.description,
            created_by=self.created_by,
            status=CONTENT_STATUSES.created,
        )

    def create_tags(self):
        self.content.tags.add(*self.tags)

    def run(self):
        self.create()
        self.create_tags()
        self.create_content_media()
        return self.content


class ContentCommentCreatePipeline:
    def __init__(self, answer, content, commented_by):
        self.answer = answer
        self.content = content
        self.commented_by = commented_by
        self._comment = None

    @property
    def comment(self):
        return self._comment

    def create(self):
        self._comment = Comment.objects.create(
            commented_by=self.commented_by, answer=self.comment, content=self.content
        )

    def run(self):
        self.create()
        return self.comment
