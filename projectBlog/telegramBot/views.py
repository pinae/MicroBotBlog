from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.apps import apps
from telegram import Update
from json import loads, decoder
import asyncio


@csrf_exempt
def webhook(request):
    async def pass_to_telegram_bot_application(update_json, csrf_token):
        application = apps.get_app_config('telegramBot').application
        telegram_update = Update.de_json(data=update_json, bot=application.bot)
        application.bot_data['csrf_token'] = csrf_token
        await application.process_update(telegram_update)

    try:
        update_data = loads(request.body)
        print("Webhook request data:")
        print(update_data)
        print("---------------------")
    except decoder.JSONDecodeError:
        return HttpResponse("Error: This is not vaild JSON.", status=500)
    if ("message" in update_data
            and "from" in update_data["message"]
            and "is_bot" not in update_data["message"]["from"]):
        update_data["message"]["from"]["is_bot"] = False
    asyncio.run(pass_to_telegram_bot_application(update_data, get_token(request)))
    return HttpResponse("OK")
