from django.urls import path
from .api_views import menu

urlpatterns = [
    path("menu/", menu, name="catalog_menu"),
]