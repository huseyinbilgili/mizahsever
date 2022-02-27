from django.urls import include, path
from rest_framework.routers import SimpleRouter

from apps.content.views import ContentViewSet

app_name = "content"

router = SimpleRouter()
router.register(
    r"contents",
    ContentViewSet,
    basename="contents",
)

urlpatterns = [
    path(
        "",
        include(router.urls),
    ),
]
