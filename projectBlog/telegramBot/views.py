from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.apps import apps
from telegram import Update
from json import loads, decoder


@csrf_exempt
def webhook(request):
    dispatcher = apps.get_app_config('telegramBot').dispatcher
    bot = apps.get_app_config('telegramBot').bot
    try:
        update_data = loads(request.body)
    except decoder.JSONDecodeError:
        return HttpResponse("Error: This is not vaild JSON.", status=500)
    if "message" in update_data and "from" in update_data["message"] and "is_bot" not in update_data["message"]["from"]:
        update_data["message"]["from"]["is_bot"] = False
    telegram_update = Update.de_json(data=update_data, bot=bot)
    dispatcher.process_update(telegram_update)
    return HttpResponse("OK")
