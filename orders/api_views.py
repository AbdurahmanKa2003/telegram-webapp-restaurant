from django.shortcuts import render

import os, json
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .telegram_auth import verify_init_data

# ⚠️ Если у тебя уже есть модели Order/OrderItem — скажи, и я подстрою под твои.
from .models import Order, OrderItem


@csrf_exempt
def create_order(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
        init_data = body.get("init_data", "")
        cart = body.get("cart", [])
        mode = body.get("mode", "pickup")
        address = body.get("address", "")
        phone = body.get("phone", "")

        token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        data = verify_init_data(init_data, token)

        # user JSON строкой: {"id":..., "first_name":...}
        user_raw = data.get("user")
        if not user_raw:
            return JsonResponse({"error": "Telegram user not found"}, status=400)
        user = json.loads(user_raw)

        tg_user_id = user.get("id")

        if not cart:
            return JsonResponse({"error": "Cart is empty"}, status=400)

        if mode == "delivery" and (not address or not phone):
            return JsonResponse({"error": "Address and phone required"}, status=400)

        order = Order.objects.create(
            tg_user_id=tg_user_id,
            mode=mode,
            address=address if mode == "delivery" else "",
            phone=phone if mode == "delivery" else "",
            status="PENDING_PAYMENT",
            created_at=timezone.now(),
        )

        total = 0
        for it in cart:
            pid = int(it["id"])
            name = str(it["name"])
            price = int(it["price"])
            qty = int(it["qty"])
            total += price * qty

            OrderItem.objects.create(
                order=order,
                product_id=pid,
                product_name=name,
                price=price,
                qty=qty,
            )

        order.total = total
        order.save(update_fields=["total"])

        return JsonResponse({"ok": True, "order_id": order.id})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def list_orders(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
        init_data = body.get("init_data", "")
        token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        data = verify_init_data(init_data, token)

        user = json.loads(data.get("user"))
        tg_user_id = user.get("id")

        qs = Order.objects.filter(tg_user_id=tg_user_id).exclude(status__in=["PENDING_PAYMENT", "EXPIRED"]).order_by("-id")[:20]
        orders = []
        for o in qs:
            orders.append({
                "id": o.id,
                "status": o.status,
                "mode": o.mode,
                "total": o.total,
                "created_at": o.created_at.strftime("%Y-%m-%d %H:%M"),
            })

        return JsonResponse({"ok": True, "orders": orders})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
