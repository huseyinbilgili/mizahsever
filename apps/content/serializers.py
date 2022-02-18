from rest_framework import serializers
from django.urls.base import reverse
from apps.content.models import Comment, Video
from apps.content.pipelines import CommentCreatePipeline, VideoCreatePipeline
from apps.user.serializers import UserSerializer


class VideoSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    absolute_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Video
        fields = ("pk", "title", "description", "cover_image", "created_by", "video", "absolute_url")

    def get_absolute_url(self, obj):
        return reverse("content:videos-detail", args=[], kwargs={"slug": obj.slug})


class VideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ("title", "description", "cover_image", "video", "tags")

    def create(self, validated_data):
        VideoCreatePipeline(
            title=validated_data.get("title"),
            description=validated_data.get("description"),
            cover_image=validated_data.get("cover_image"),
            video=validated_data.get("video"),
            created_by=self.context.get("user"),
            tags=validated_data.get("tags"),
        ).run()


class VideoCommentSerializer(serializers.ModelSerializer):
    commented_by = UserSerializer()

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
