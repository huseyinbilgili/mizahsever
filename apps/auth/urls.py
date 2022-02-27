from django.urls import path

from apps.auth.views import AuthTokenView

app_name = "auth"

urlpatterns = [
    path(
        r"login/",
        AuthTokenView.as_view(),
        name="login",
    ),
]
