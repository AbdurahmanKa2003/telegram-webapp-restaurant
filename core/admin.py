from django.contrib import admin
from .models import BotSettings

@admin.register(BotSettings)
class BotSettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "admin_user_chat_id", "admin_group_chat_id", "currency_symbol", "updated_at")
