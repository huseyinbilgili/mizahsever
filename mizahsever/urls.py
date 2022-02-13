from django.contrib import admin
from django.urls import path, include

from core.user.views import AuthTokenView

urlpatterns = [
    # path("admin/", admin.site.urls),
    path(r"api/v1/user/", include("core.user.urls"))
]
