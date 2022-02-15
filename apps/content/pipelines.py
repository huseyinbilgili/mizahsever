from apps.content.models import Comment


class VideoCreatePipeline:
    def __init__(self, title, description, cover_image, video, created_by):
        self.title = title
        self.description = description
        self.cover_image = cover_image
        self.video = video
        self.created_by = created_by

    def create_video(self):
        # call async job
        pass

    def run(self):
        self.create_video()


class CommentCreatePipeline:
    def __init__(self, answer, video, commented_by):
        self.answer = answer
        self.video = video
        self.commented_by = commented_by
        self._comment = None

    @property
    def comment(self):
        return self._comment

    def create(self):
        self._comment = Comment.objects.create(
            commented_by=self.commented_by, answer=self.comment, video=self.video
        )

    def run(self):
        self.create()
        return self.comment
