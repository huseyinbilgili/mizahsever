from django.urls.base import reverse
from rest_framework import serializers

from apps.content.models import Comment, Content, ContentMedia, Tag
from apps.content.pipelines import (
    ContentCommentCreatePipeline,
    ContentCreatePipeline,
    ContentMediaCreatePipeline,
)
from apps.user.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("pk", "name")


class ContentMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentMedia
        fields = ("pk", "cover_image", "preview", "duration", "file")


class ContentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    absolute_url = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializer(many=True)
    medias = ContentMediaSerializer(many=True)

    class Meta:
        model = Content
        fields = (
            "pk",
            "title",
            "description",
            "created_by",
            "absolute_url",
            "tags",
            "medias",
        )

    def get_absolute_url(self, obj):
        return reverse("content:contents-detail", args=[], kwargs={"slug": obj.slug})


class ContentCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all())
    file = serializers.FileField()

    class Meta:
        model = Content
        fields = ("title", "description", "tags", "file")

    def create(self, validated_data):
        content = ContentCreatePipeline(
            title=validated_data.get("title"),
            description=validated_data.get("description"),
            created_by=self.context.get("user"),
            tags=validated_data.get("tags"),
        ).run()
        ContentMediaCreatePipeline(
            content=content, file=validated_data.get("file")
        ).run()
        return content


class ContentCommentSerializer(serializers.ModelSerializer):
    commented_by = UserSerializer()

    class Meta:
        model = Comment
        fields = ("commented_by", "answer", "created_at")


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("answer", "content")

    def create(self, validated_data):
        ContentCommentCreatePipeline(
            answer=validated_data.get("answer"),
            content=validated_data.get("content"),
            commented_by=self.context.get("commented_by"),
        ).run()


class CommentSerializer(serializers.ModelSerializer):
    content = ContentSerializer()

    class Meta:
        model = Comment
        fields = ("content", "answer", "status", "created_at")
