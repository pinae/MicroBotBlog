from django.apps import AppConfig
from django.conf import settings
from django.urls import reverse
#from telegram import Bot
from telegram.ext import Application
from telegram.ext import MessageHandler, filters
#from telegram.utils.request import Request
from telegram.error import RetryAfter
#from queue import Queue
from .bot import message, image, error_handler


class TelegrambotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegramBot'
    application: Application = None
    #bot: Bot = None
    #dispatcher: Dispatcher = None
    webhook_registered = False

    def ready(self):
        #if not self.bot:
        #    self.bot = Bot(settings.TELEGRAM_BOT["token"], request=Request(read_timeout=10, connect_timeout=10))
        if not self.application:
            self.application = Application.builder().updater(None).token(settings.TELEGRAM_BOT["token"]).build()
            #self.dispatcher = Dispatcher(bot=self.bot, update_queue=Queue(), use_context=True, workers=1)
            self.application.add_error_handler(error_handler, block=True)
            self.application.add_handler(
                MessageHandler(filters.TEXT & (~filters.COMMAND), message))
            self.application.add_handler(
                MessageHandler(filters=filters.PHOTO, callback=image))
        if settings.TELEGRAM_BOT["register_webhook"] and not self.webhook_registered:
            try:
                self.application.bot.setWebhook(settings.DOMAIN + reverse('webhook'))
            except RetryAfter:
                print("Telegram didn't accept the setWebhook command. " +
                      "This is probably because there was another request to the API within one second.")
                print("This is what the bot already knows about the webhook:")
                print(self.application.bot.get_webhook_info())
            self.webhook_registered = True
