from django.urls import path
from .api_views import create_order, list_orders

urlpatterns = [
    path("orders/create/", create_order),
    path("orders/list/", list_orders),
]