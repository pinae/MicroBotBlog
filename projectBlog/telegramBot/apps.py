from django.apps import AppConfig
from django.conf import settings
from django.urls import reverse
from telegram import Bot
from telegram.ext import Dispatcher
from telegram.ext import MessageHandler, Filters
from queue import Queue
from .bot import message, image


class TelegrambotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegramBot'
    bot: Bot = None
    dispatcher: Dispatcher = None

    def ready(self):
        if not self.bot:
            self.bot = Bot(settings.TELEGRAM_BOT["token"])
        if not self.dispatcher:
            self.dispatcher = Dispatcher(bot=self.bot, update_queue=Queue(), use_context=True)
            self.dispatcher.add_handler(
                MessageHandler(Filters.text & (~Filters.command), message))
            self.dispatcher.add_handler(
                MessageHandler(filters=Filters.photo, callback=image))
        if settings.TELEGRAM_BOT["register_webhook"]:
            self.bot.setWebhook(settings.TELEGRAM_BOT["webhook_base_url"] + reverse('webhook'))
