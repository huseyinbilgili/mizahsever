from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.user.models import User
from apps.user.serializers import UserSerializer
from core.permissions import UserPermissions


class UserViewSet(CreateAPIView, RetrieveAPIView, UpdateAPIView, GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (UserPermissions,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token = Token.objects.get(user=serializer.instance).key
        return Response(status=status.HTTP_200_OK, data={"token": token})
