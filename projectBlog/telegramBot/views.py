from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.apps import apps
from .bot import UpdateWithToken
from json import loads, decoder


@csrf_exempt
def webhook(request):
    dispatcher = apps.get_app_config('telegramBot').dispatcher
    bot = apps.get_app_config('telegramBot').bot
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
    telegram_update = UpdateWithToken.de_json(data=update_data, bot=bot)
    telegram_update.csrf_token = get_token(request)
    dispatcher.process_update(telegram_update)
    return HttpResponse("OK")
