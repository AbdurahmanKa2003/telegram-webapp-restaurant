# orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = ("product_id", "product_name", "price", "qty")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tg_user_id",
        "mode",
        "status",
        "total",
        "phone",
        "address",
        "items_count_display",
        "items_summary_display",
        "created_at",
    )
    list_filter = ("status", "mode", "created_at")
    search_fields = ("id", "tg_user_id", "phone", "address", "items__product_name")
    ordering = ("-id",)
    list_editable = ("status",)
    inlines = [OrderItemInline]

    # пока оплаты нет — можно скрывать ожидающие оплату (или оставь как есть)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # если хочешь видеть ВСЕ (включая pending) — просто верни qs
        return qs.exclude(status="PENDING_PAYMENT").exclude(status="EXPIRED")

    @admin.display(description="Items count")
    def items_count_display(self, obj):
        return obj.items.count()

    @admin.display(description="Order items")
    def items_summary_display(self, obj):
        return obj.items_summary()