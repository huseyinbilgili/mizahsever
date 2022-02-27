from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.content.models import Comment, Content
from apps.content.serializers import (
    CommentCreateSerializer,
    CommentSerializer,
    ContentCommentSerializer,
    ContentCreateSerializer,
    ContentSerializer,
)
from core.constants import BASE_STATUSES, CONTENT_STATUSES
from core.permissions import ContentPermissions


class ContentViewSet(ModelViewSet):
    queryset = Content.objects.filter(status=CONTENT_STATUSES.ready)
    serializer_class = ContentSerializer
    permission_classes = (ContentPermissions,)
    authentication_classes = ()
    lookup_field = "slug"

    def create(
        self,
        request,
        *args,
        **kwargs,
    ):
        serializer = ContentCreateSerializer(
            data=request.data,
            context=dict(user=request.user),
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(
        detail=True,
        methods=["get"],
        serializer_class=ContentCommentSerializer,
    )
    def comments(
        self,
        request,
        *args,
        **kwargs,
    ):
        content = self.get_object()
        queryset = content.comment_set.filter(status=BASE_STATUSES.active)
        return Response(
            self.serializer_class(
                queryset,
                many=True,
            ).data
        )


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(
        self,
    ):
        return self.queryset.filter(commented_by=self.request.user)

    def create(
        self,
        request,
        *args,
        **kwargs,
    ):
        serializer = CommentCreateSerializer(
            data=request.data,
            context=dict(commented_by=request.user),
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
