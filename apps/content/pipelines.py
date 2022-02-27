from django.utils.text import slugify

from apps.content.models import Comment, Content
from core.constants import CONTENT_STATUSES


class ContentMediaCreatePipeline:
    def __init__(self, content, file):
        self.content = content
        self.file = file

    def create(self):
        pass  # Call async job

    def run(self):
        pass


class ContentCreatePipeline:
    def __init__(self, title, description, created_by, tags):
        self.title = title
        self.description = description
        self.created_by = created_by
        self.tags = tags
        self._content = None

    @property
    def content(self):
        return self._content

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
