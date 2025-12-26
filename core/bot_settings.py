# core/bot_settings.py
from .models import BotSettings

def get_bot_settings() -> BotSettings | None:
    # берём первую запись (обычно она одна)
    return BotSettings.objects.order_by("-updated_at").first()