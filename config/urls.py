from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Исправленный импорт: импортируем именно 'webapp'
from core.views import webapp 

urlpatterns = [
    path("admin/", admin.site.urls),
    # Исправленный путь: используем функцию 'webapp'
    path("webapp/", webapp, name="webapp"), 
    path("", include("core.urls")),
    path("api/", include("orders.api_urls")),
    path("api/catalog/", include("catalog.api_urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
