import os
import json
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ✅ Надёжно ищем .env рядом с manage.py
# runbot.py: bot/management/commands/runbot.py
# поэтому поднимаемся на 4 уровня вверх до корня проекта
BASE_DIR = Path(__file__).resolve().parents[4]
load_dotenv(BASE_DIR / ".env")


def normalize_webapp_url(url: str) -> str:
    """
    Делает URL безопасным для WebApp:
    - должен быть https
    - если нет path или он '/', добавит '/webapp/'
    - добавит trailing slash
    """
    url = (url or "").strip()
    if not url:
        return ""

    # если забыли https://
    if url.startswith("http://"):
        url = "https://" + url[len("http://"):]
    if not url.startswith("https://"):
        # не ломаем запуск, просто вернём как есть
        return url

    p = urlparse(url)
    path = p.path or "/"
    if path == "/":
        path = "/webapp/"
    if not path.endswith("/"):
        path += "/"

    return urlunparse((p.scheme, p.netloc, path, "", p.query, ""))


class Command(BaseCommand):
    help = "Run Telegram bot (python manage.py runbot)"

    def handle(self, *args, **options):
        token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        raw_webapp_url = os.getenv("WEBAPP_URL", "").strip()

        self.stdout.write(f"DEBUG: BASE_DIR={BASE_DIR}")
        self.stdout.write(f"DEBUG: RAW WEBAPP_URL from .env = {raw_webapp_url!r}")

        webapp_url = normalize_webapp_url(raw_webapp_url)
        self.stdout.write(f"DEBUG: NORMALIZED WEBAPP_URL = {webapp_url!r}")

        if not token or token == "PUT_YOUR_TOKEN_HERE":
            self.stderr.write("❌ TELEGRAM_BOT_TOKEN is not set in .env")
            return

        if not webapp_url:
            self.stderr.write("❌ WEBAPP_URL is empty. Put it into .env")
            self.stderr.write("   Example: WEBAPP_URL=https://xxxx.ngrok-free.dev/webapp/")
            return

        if not webapp_url.startswith("https://"):
            self.stderr.write("⚠️ WEBAPP_URL is not https. Telegram WebApp usually requires https.")
            # не выходим, пусть запускается

        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            # ✅ 1) Inline-кнопка (внутри сообщения) — это самый надёжный способ открытия WebApp
            kb_inline = [
                [InlineKeyboardButton("🍽 Открыть меню", web_app=WebAppInfo(url=webapp_url))],
            ]

            await update.message.reply_text(
                "✅ Откройте меню:",
                reply_markup=InlineKeyboardMarkup(kb_inline),
            )

            # ❗️Важно:
            # Кнопка под клавиатурой (ReplyKeyboardMarkup + web_app)
            # часто открывает WebApp без нормального initData в некоторых клиентах.
            # Поэтому мы её НЕ используем.
            #await update.message.reply_text(
             #   "ℹ️ Кнопку «под клавиатурой» убрали, потому что она часто открывает WebApp без initData, "
             #   "и заказ не создаётся. Используй кнопку выше или Menu Button (BotFather)."
            #)

        async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text("Нажми /start — там будет кнопка открытия меню ✅")

        async def on_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
            # Это сработает ТОЛЬКО если ты вызываешь tg.sendData(...) из WebApp
            data = update.message.web_app_data.data
            try:
                payload = json.loads(data)
            except Exception:
                payload = data

            await update.message.reply_text(f"✅ Данные из WebApp:\n{payload}")

        app = Application.builder().token(token).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("menu", menu))
        app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, on_webapp_data))

        self.stdout.write("🤖 Bot started. Press Ctrl+C to stop.")
        app.run_polling(drop_pending_updates=True)
