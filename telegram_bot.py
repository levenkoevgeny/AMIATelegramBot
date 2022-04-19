import telebot
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AMIATelegramBot.settings')
django.setup()

from bot.models import TelegramUser

from telebot import apihelper

apihelper.proxy = {'https':'http://levenko:1986@192.168.0.123:8080'}

bot = telebot.TeleBot("5276008496:AAGWfe-mMCvi981zK71G33ViK6K_Dh0QG44", parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message.from_user.id)
    obj, _ = TelegramUser.objects.get_or_create(user_id=int(message.from_user.id))
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(content_types=["text", "sticker", "pinned_message", "photo", "audio"])
def function_name(message):

    print(message)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('messages',
                                            {
                                                'type': 'chat_message',
                                                'message': {'lastname': "test"}
                                            })


bot.infinity_polling()
