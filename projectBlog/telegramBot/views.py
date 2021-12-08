from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.apps import apps


@csrf_exempt
def webhook(request):
    dispatcher = apps.get_app_config('telegramBot').dispatcher
    dispatcher.process_update(request.body)
    return HttpResponse("Foo!")
