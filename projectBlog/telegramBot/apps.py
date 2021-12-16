from django.apps import AppConfig
from django.conf import settings
from django.urls import reverse
from telegram import Bot
from telegram.ext import Dispatcher
from telegram.ext import MessageHandler, Filters
from telegram.utils.request import Request
from telegram.error import RetryAfter
from queue import Queue
from .bot import message, image, error_handler


class TelegrambotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegramBot'
    bot: Bot = None
    dispatcher: Dispatcher = None
    webhook_registered = False

    def ready(self):
        if not self.bot:
            self.bot = Bot(settings.TELEGRAM_BOT["token"], request=Request(read_timeout=10, connect_timeout=10))
        if not self.dispatcher:
            self.dispatcher = Dispatcher(bot=self.bot, update_queue=Queue(), use_context=True, workers=1)
            self.dispatcher.add_error_handler(error_handler, run_async=False)
            self.dispatcher.add_handler(
                MessageHandler(Filters.text & (~Filters.command), message))
            self.dispatcher.add_handler(
                MessageHandler(filters=Filters.photo, callback=image))
        if settings.TELEGRAM_BOT["register_webhook"] and not self.webhook_registered:
            try:
                self.bot.setWebhook(settings.DOMAIN + reverse('webhook'))
            except RetryAfter:
                print("Telegram didn't accept the setWebhook command. " +
                      "This is probably because there was another request to the API within one second.")
                print("This is what the bot already knows about the webhook:")
                print(self.bot.get_webhook_info())
            self.webhook_registered = True
