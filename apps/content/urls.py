from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.content.views import VideoViewSet

app_name = "content"

router = SimpleRouter()
router.register(r"videos", VideoViewSet, basename="videos")

urlpatterns = [
    path('', include(router.urls)),
]
