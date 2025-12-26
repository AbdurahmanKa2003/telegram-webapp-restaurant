# orders/models.py
from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING_PAYMENT", "PENDING_PAYMENT"),
        ("PAID", "PAID"),
        ("PREPARING", "PREPARING"),
        ("READY", "READY"),
        ("ON_THE_WAY", "ON_THE_WAY"),
        ("DELIVERED", "DELIVERED"),
        ("CANCELED", "CANCELED"),
        ("EXPIRED", "EXPIRED"),
    ]

    tg_user_id = models.BigIntegerField(db_index=True)
    mode = models.CharField(max_length=20, default="pickup")
    address = models.CharField(max_length=255, blank=True, default="")
    phone = models.CharField(max_length=50, blank=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING_PAYMENT")
    total = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def items_count(self) -> int:
        return self.items.count()

    def items_summary(self) -> str:
        # "Бургер x2, Кола x1"
        return ", ".join([f"{i.product_name} x{i.qty}" for i in self.items.all()])

    def __str__(self):
        return f"Order #{self.id} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=120)
    price = models.IntegerField()
    qty = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product_name} x{self.qty}"