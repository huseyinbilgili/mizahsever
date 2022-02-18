from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.content.models import Comment, Video
from apps.content.serializers import (
    CommentCreateSerializer,
    CommentSerializer,
    VideoCommentSerializer,
    VideoCreateSerializer,
    VideoSerializer,
)
from core.constants import BASE_STATUSES
from core.permissions import VideoPermissions


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (VideoPermissions,)
    authentication_classes = ()
    lookup_field = "slug"

    def create(self, request, *args, **kwargs):
        serializer = VideoCreateSerializer(
            data=request.data, context=dict(user=request.user)
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["get"], serializer_class=VideoCommentSerializer)
    def comments(self, request, *args, **kwargs):
        video = self.get_object()
        queryset = video.comment_set.filter(status=BASE_STATUSES.active)
        return Response(self.serializer_class(queryset, many=True).data)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return self.queryset.filter(commented_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = CommentCreateSerializer(
            data=request.data, context=dict(commented_by=request.user)
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
