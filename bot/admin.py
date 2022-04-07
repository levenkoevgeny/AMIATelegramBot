from django.contrib import admin
from .models import TelegramUser, Message

admin.site.register(TelegramUser)
admin.site.register(Message)
