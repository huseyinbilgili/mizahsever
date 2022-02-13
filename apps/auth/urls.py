from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.auth.views import AuthTokenView

app_name = "auth"

router = SimpleRouter()


urlpatterns = [
    path(r"login/", AuthTokenView.as_view(), name="login"),
]

urlpatterns += router.urls
