from rest_framework import serializers

from apps.content.models import Comment, Video
from apps.content.pipelines import CommentCreatePipeline, VideoCreatePipeline
from apps.user.serializers import UserSerializer


class VideoSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()

    class Meta:
        model = Video
        fields = ("title", "description", "cover_image", "created_by", "video")


class VideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ("title", "description", "cover_image", "video")

    def create(self, validated_data):
        VideoCreatePipeline(
            title=validated_data.get("title"),
            description=validated_data.get("description"),
            cover_image=validated_data.get("cover_image"),
            video=validated_data.get("video"),
            created_by=self.context.get("user"),
        ).run()


class VideoCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("commented_by", "answer", "created_at")


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("answer", "video")

    def create(self, validated_data):
        CommentCreatePipeline(
            answer=validated_data.get("comment"),
            commented_by=self.context.get("commented_by"),
        ).run()


class CommentSerializer(serializers.ModelSerializer):
    video = VideoSerializer()

    class Meta:
        model = Comment
        fields = ("video", "answer", "status", "created_at")
