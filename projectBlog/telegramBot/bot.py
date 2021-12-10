from typing import Any
from telegram import Update
from telegram.ext import CallbackContext
from django.conf import settings
from django.urls import reverse
from requests import post


class UpdateWithToken(Update):
    csrf_token = None


def message(update: UpdateWithToken, context: CallbackContext):
    telegram_id = None
    if update.message is not None:
        telegram_id = update.message.message_id
    if update.edited_message is not None:
        telegram_id = update.edited_message.message_id
    post(settings.TELEGRAM_BOT["webhook_base_url"] + reverse("create_post"), headers={
        "X-CSRFToken": update.csrf_token
    }, cookies={
        "csrftoken": update.csrf_token
    }, json={
        "author_info": {
            "first_name": update.effective_user["first_name"],
            "last_name": update.effective_user["last_name"]
        },
        "project_name": update.effective_chat["title"],
        "text": update.effective_message.text_markdown,
        "telegram_id": telegram_id
    })


def image(update: Update, context: CallbackContext):
    print(update.effective_message.caption_markdown)
    biggest_photo = {'object': None, 'height': 0}
    for photo_size in update.effective_message.photo:
        if photo_size.height > biggest_photo['height']:
            biggest_photo['height'] = photo_size.height
            biggest_photo['object'] = photo_size
    print(biggest_photo)
    if biggest_photo['object'] is None:
        return
    file_object = context.bot.get_file(biggest_photo['object'])
    print(file_object)
