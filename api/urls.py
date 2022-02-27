from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(r"v1/", include("apps.auth.urls")),
    path(r"v1/user/", include("apps.user.urls")),
    path(r"v1/content/", include("apps.content.urls")),
]
if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
