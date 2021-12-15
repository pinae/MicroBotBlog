from telegram import Update
from telegram.ext import CallbackContext
from django.conf import settings
from django.urls import reverse
from requests import post
from ssl import SSLError
from time import sleep
from telegram.error import NetworkError
from codecs import decode


class UpdateWithToken(Update):
    csrf_token = None


def get_telegram_id(update: UpdateWithToken):
    telegram_id = None
    if update.message is not None:
        telegram_id = update.message.message_id
    if update.edited_message is not None:
        telegram_id = update.edited_message.message_id
    return telegram_id


def add_media_group_id(update: UpdateWithToken, data: dict):
    if update.message is not None and update.message.media_group_id is not None:
        data["media_group_id"] = update.message.media_group_id
    if update.edited_message is not None and update.edited_message.media_group_id is not None:
        data["media_group_id"] = update.edited_message.media_group_id
    return data


def request_save(view_name, data, csrf_token, try_no=1):
    try:
        response = post(settings.DOMAIN + reverse(view_name), headers={
            "Connection": "Keep-Alive",
            "X-CSRFToken": csrf_token
        }, cookies={
            "csrftoken": csrf_token
        }, json=data)
        if response.text != "OK":
            print(response.text)
    except SSLError or NetworkError:
        if try_no <= 10:
            sleep(1.5)
            request_save(view_name, data, csrf_token, try_no=try_no+1)
        else:
            print("Tried 10 times. Always getting an SSLError. Giving up.")


def message(update: UpdateWithToken, context: CallbackContext):
    telegram_id = get_telegram_id(update)
    request_save(view_name="create_post", data={
        "author_info": {
            "first_name": update.effective_user["first_name"],
            "last_name": update.effective_user["last_name"]
        },
        "project_name": update.effective_chat["title"],
        "text": decode(update.effective_message.text_markdown.encode('utf-8'), encoding="unicode_escape")
        if update.effective_message.text_markdown is not None else None,
        "telegram_id": telegram_id,
        "is_edit": update.edited_message is not None
    }, csrf_token=update.csrf_token)


def image(update: UpdateWithToken, context: CallbackContext):
    print(update.effective_message.caption_markdown)
    biggest_photo = {'object': None, 'height': 0}
    for photo_size in update.effective_message.photo:
        if photo_size.height > biggest_photo['height']:
            biggest_photo['height'] = photo_size.height
            biggest_photo['object'] = photo_size
    if biggest_photo['object'] is None:
        return
    for try_no in range(10):
        try:
            file_object = context.bot.get_file(biggest_photo['object'])
            break
        except SSLError or NetworkError:
            sleep(1.5)
            if try_no >= 9:
                print("Tried 10 times to load the file object. Always getting an SSLError. Giving up.")
                return
    telegram_id = get_telegram_id(update)
    data = {
        "author_info": {
            "first_name": update.effective_user["first_name"],
            "last_name": update.effective_user["last_name"]
        },
        "project_name": update.effective_chat["title"],
        "caption": decode(update.effective_message.caption_markdown.encode('utf-8'), encoding="unicode_escape")
        if update.effective_message.caption_markdown is not None else None,
        "album": [file_object['file_path']],
        "telegram_id": telegram_id,
        "is_edit": update.edited_message is not None
    }
    add_media_group_id(update, data)
    request_save(view_name="download_image", data=data, csrf_token=update.csrf_token)
