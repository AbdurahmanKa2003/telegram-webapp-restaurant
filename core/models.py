from django.db import models

# core/models.pyfrom django.db import models

class BotSettings(models.Model):
    admin_user_chat_id = models.BigIntegerField(blank=True, null=True)   # личка админа
    admin_group_chat_id = models.BigIntegerField(blank=True, null=True)  # группа/чат

    # опционально: валюта/тексты/прочее
    currency_symbol = models.CharField(max_length=10, default="₽")

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Bot Settings"

    class Meta:
        verbose_name = "Bot Settings"
        verbose_name_plural = "Bot Settings"
