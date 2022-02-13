from rest_framework.routers import SimpleRouter

from apps.user.views import UserViewSet

app_name = "user"

router = SimpleRouter()
router.register(r"", UserViewSet)

urlpatterns = router.urls
