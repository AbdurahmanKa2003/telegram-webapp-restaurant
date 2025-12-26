# orders/signals.py
import logging

from asgiref.sync import async_to_sync
from django.db.models.signals import pre_save
from django.dispatch import receiver
from telegram import Bot
from telegram.error import TelegramError

from .models import Order
from core.bot_settings import get_bot_settings  # у тебя это уже есть

logger = logging.getLogger(__name__)

USER_NOTIFY_STATUSES = {"PAID", "PREPARING", "READY", "ON_THE_WAY", "DELIVERED", "CANCELED"}
ADMIN_NOTIFY_STATUSES = {"PAID"}


@receiver(pre_save, sender=Order)
def notify_status_change(sender, instance: Order, **kwargs):
    # Создание нового заказа не трогаем
    if not instance.pk:
        return

    old = Order.objects.filter(pk=instance.pk).first()
    if not old or old.status == instance.status:
        return

    settings = get_bot_settings()
    if not settings:
        return

    token = getattr(settings, "telegram_token", None)  # если у тебя НЕТ поля telegram_token — см. ниже
    if not token:
        # Если токен хранится в .env (как раньше) — просто делай так:
        import os
        token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        return

    admin_user_chat_id = getattr(settings, "admin_user_chat_id", None)
    admin_group_chat_id = getattr(settings, "admin_group_chat_id", None)

    bot = Bot(token=token)

    def safe_send(chat_id: int, text: str):
        """Никогда не ломаем сохранение заказа из-за Telegram."""
        try:
            async_to_sync(bot.send_message)(chat_id=chat_id, text=text)
        except TelegramError as e:
            # ВАЖНО: не кидаем исключение дальше
            logger.warning("Telegram notify failed: chat_id=%s err=%s", chat_id, e)

    # 1) Уведомление пользователю (если чат доступен)
    if instance.status in USER_NOTIFY_STATUSES and instance.tg_user_id:
        safe_send(
            chat_id=int(instance.tg_user_id),
            text=f"📦 Order #{instance.id} status: {old.status} ➜ {instance.status}",
        )

    # 2) Уведомление админу/группе (например только при PAID)
    if instance.status in ADMIN_NOTIFY_STATUSES:
        msg = (
            f"✅ PAID order #{instance.id}\n"
            f"Mode: {instance.mode}\n"
            f"Total: {instance.total} ₺"
        )

        if admin_user_chat_id:
            safe_send(chat_id=int(admin_user_chat_id), text=msg)

        if admin_group_chat_id:
            safe_send(chat_id=int(admin_group_chat_id), text=msg)