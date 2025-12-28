from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import webapp 

# Оставьте только это:
urlpatterns = [
    path("admin/", admin.site.urls),
    path("webapp/", webapp, name="webapp"), 
    path("", include("core.urls")),
    path("api/", include("orders.api_urls")),
    path("api/catalog/", include("catalog.api_urls")),
]
# Строки с urlpatterns += static(...) на Render не нужны, 
# так как WhiteNoise работает автоматически через Middleware.
# Эти строки нужны ТОЛЬКО для локальной разработки. 
# На Render WhiteNoise сам подхватит STATIC_ROOT.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
