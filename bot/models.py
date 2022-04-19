from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class TelegramUser(models.Model):
    user_id = models.BigAutoField(primary_key=True, verbose_name="User ID")
    first_name = models.CharField(verbose_name="Имя", max_length=100, blank=True, null=True)
    username = models.CharField(verbose_name="Логин", max_length=100, blank=True, null=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=100, blank=True, null=True)
    avatar = models.ImageField(verbose_name="Аватар", upload_to='avatars', blank=True, null=True)

    def __str__(self):
        return "{0} {1}".format(str(self.user_id), self.last_name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('messages',
                                                {
                                                    'type': 'chat_message',
                                                    'message': {'lastname': self.last_name}
                                                })

    class Meta:
        ordering = ('user_id',)
        verbose_name = 'Telegram пользователь'
        verbose_name_plural = 'Telegram пользователи'


class Message(models.Model):
    message_text = models.TextField(verbose_name="Текст сообщения")
    telegram_user = models.ForeignKey(TelegramUser, verbose_name="Кто написал", on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.message_text, self.telegram_user.last_name)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
