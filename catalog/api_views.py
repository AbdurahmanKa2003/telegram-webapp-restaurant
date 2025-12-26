from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Product


@require_GET
def menu(request):
    products = (
        Product.objects
        .filter(is_active=True)
        .select_related("category")
        .order_by("category__name", "name")
    )

    data = []
    for p in products:
        image_url = request.build_absolute_uri(p.image.url) if p.image else ""
        data.append({
            "id": p.id,
            "category": p.category.name,
            "name": p.name,
            "desc": p.description or "",
            "price": float(p.price),
            "image_url": image_url,
        })

    return JsonResponse({"items": data})