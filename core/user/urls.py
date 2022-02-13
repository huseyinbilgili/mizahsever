from django.urls import path
from rest_framework.routers import DefaultRouter

from core.user.views import UserViewSet, AuthTokenView

app_name = "user"

router = DefaultRouter()
router.register(r"", UserViewSet)
urlpatterns = [
    path(r'login/', AuthTokenView.as_view(), name="login"),
]
urlpatterns += router.urls
