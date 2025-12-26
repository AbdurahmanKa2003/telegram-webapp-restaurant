from django.contrib import admin
from django.urls import path
from core.views import webapp
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path("webapp/", webapp, name="webapp"),
    path("", include("core.urls")),
    path("api/", include("orders.api_urls")),
    path("api/catalog/", include("catalog.api_urls")),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )