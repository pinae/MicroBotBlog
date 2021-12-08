from telegram import Update
from telegram.ext import CallbackContext


def message(update: Update, context: CallbackContext):
    if update.edited_message is not None:
        print("Edited ID:", update.edited_message.message_id)
    if update.message is not None:
        print("New ID:", update.message.message_id)
    print(update.effective_message.text_markdown)
    print("Chat Titel:", update.effective_chat['title'])
    print(update.effective_user)
    # context.bot.send_message(chat_id=update.effective_chat.id, text=str(update))


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
