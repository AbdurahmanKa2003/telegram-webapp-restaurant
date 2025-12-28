from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("api/", include("orders.api_urls")),
    path("api/catalog/", include("catalog.api_urls")),
]

# Всегда добавляем эти пути, чтобы Django знал, где искать файлы в DEBUG и после collectstatic
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
