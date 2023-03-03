from telegram import Update
from telegram.ext import CallbackContext
from django.conf import settings
from django.urls import reverse
from requests import post
from ssl import SSLError
from time import sleep
from telegram.error import NetworkError
from codecs import decode


def get_telegram_id(update: Update):
    telegram_id = None
    if update.message is not None:
        telegram_id = update.message.message_id
    if update.edited_message is not None:
        telegram_id = update.edited_message.message_id
    return telegram_id


def add_media_group_id(update: Update, data: dict):
    if update.message is not None and update.message.media_group_id is not None:
        data["media_group_id"] = update.message.media_group_id
    if update.edited_message is not None and update.edited_message.media_group_id is not None:
        data["media_group_id"] = update.edited_message.media_group_id
    return data


def request_save(view_name, data, csrf_token):
    response = post(settings.DOMAIN + reverse(view_name), headers={
        "Connection": "Keep-Alive",
        "X-CSRFToken": csrf_token
    }, cookies={
        "csrftoken": csrf_token
    }, json=data)
    if response.text != "OK":
        print(response.text)


async def message(update: Update, context: CallbackContext):
    telegram_id = get_telegram_id(update)
    request_save(view_name="create_post", data={
        "author_info": {
            "first_name": update.effective_user["first_name"],
            "last_name": update.effective_user["last_name"]
        },
        "project_name": update.effective_chat["title"],
        "text": update.effective_message.text_markdown,
        "telegram_id": telegram_id,
        "is_edit": update.edited_message is not None
    }, csrf_token=context.bot_data['csrf_token'])


async def image(update: UpdateWithToken, context: CallbackContext):
    biggest_photo = {'object': None, 'height': 0}
    for photo_size in update.effective_message.photo:
        if photo_size.height > biggest_photo['height']:
            biggest_photo['height'] = photo_size.height
            biggest_photo['object'] = photo_size
    if biggest_photo['object'] is None:
        return
    file_object = await context.bot.get_file(biggest_photo['object'])
    telegram_id = get_telegram_id(update)
    data = {
        "author_info": {
            "first_name": update.effective_user["first_name"],
            "last_name": update.effective_user["last_name"]
        },
        "project_name": update.effective_chat["title"],
        "caption": decode(update.effective_message.caption_markdown.encode('utf-8'), encoding="unicode_escape")
        if update.effective_message.caption_markdown is not None else None,
        "album": [file_object.file_path],
        "telegram_id": telegram_id,
        "is_edit": update.edited_message is not None
    }
    add_media_group_id(update, data)
    request_save(view_name="download_image", data=data, csrf_token=context.bot_data['csrf_token'])


async def error_handler(update: Update, context: CallbackContext):
    print(type(context.error))
    print(context.error)
    if type(context.error) is SSLError or type(context.error) is NetworkError:
        print("Sleeping for 2,5s.")
        sleep(2.5)
        print("Trying to process the update again.")
        await context.application.process_update(update)
