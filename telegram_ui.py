import os
from pprint import pprint
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from image_parser import ImageParser
from telegram_usage import TelegramUsage
from config import (bot_key,
                    callback_separator,
                    callback_data_show,
                    callback_data_update,
                    callback_data_delete,
                    callback_data_show_f,
                    callback_data_update_f,
                    callback_data_delete_f,
                    callback_data_show_un,
                    callback_data_update_un,
                    callback_data_delete_un)


bot = telebot.TeleBot(bot_key)
telegram_us = TelegramUsage()

@bot.message_handler(content_types= ["photo"])
def take_photo(message) -> None:
    value_photos = []
    #TODO add here parameters and not send them via the callback !
    # telegram_us.your_name =
    for photos in message.photo:
        raw = photos.file_id
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        value_photos.append(telegram_us.save_tmp_file(downloaded_file))
    value_photo_name = telegram_us.detect_less_compressed(value_photos)
    
    value_examine = f'{callback_data_show}{message.message_id}{callback_separator}{os.path.splitext(value_photo_name)[0]}'
    value_update = f'{callback_data_update}{message.message_id}{callback_separator}{os.path.splitext(value_photo_name)[0]}'
    value_delete = f'{callback_data_delete}{message.message_id}{callback_separator}{os.path.splitext(value_photo_name)[0]}'

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('Analyse Tags', callback_data=value_examine))
    keyboard.row(telebot.types.InlineKeyboardButton('Update Tags', callback_data=value_update),
                telebot.types.InlineKeyboardButton('Remove Tags', callback_data=value_delete))

    bot.reply_to(message, 'Select command what to do with a photo:', reply_markup=keyboard)
    #TODO add the extintions and send it as file?
    #TODO make updating values to the values; 

@bot.message_handler(content_types=['document'])
def take_photo_uncompressed(message) -> None:
    file_name = message.document.file_name
    if telegram_us.detect_image_ext(file_name):
        file_id_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_id_info.file_path)
        if telegram_us.detect_image_value(downloaded_file):
            value_photo = telegram_us.save_tmp_file(downloaded_file, False, os.path.splitext(file_name)[-1])
        else: 
            bot.reply_to(message, f"Unfortunatelly we faced several problems with sent file {file_name}. It seems to be broken")
            return
    else:
        bot.reply_to(message, "Unfortunatelly it's not seems like the image file. It is seen by an extention")
        return

@bot.callback_query_handler(func=lambda call: True)
def calculate_answer_on_the_buttons(query):
    data = query.data
    data_user = query.from_user.id
    
    if data.startswith(callback_data_update):
        value_sent = data.split(callback_data_update)[-1]
        message_id, message_photo = value_sent.split(callback_separator)
        message_photo_name, message_photo_path = telegram_us.detect_usage_location(message_photo, callback_data_update)
        message_photo_out = telegram_us.produce_file_update(message_photo_path, message_photo_name)
        message_photo_text = telegram_us.produce_message_photo_text(callback_data_update)
        # file_obj = io.BytesIO(your_bin_data)
        # file_obj.name = "MarksSYAP.xlsx"
        # bot.send_document(message.chat.id,file_obj)
        image_new = open(os.path.join(message_photo_path, message_photo_out), 'rb')
        bot.send_photo(data_user, image_new, caption=message_photo_text, reply_to_message_id=message_id)
        image_new.close()
        # ImageParser().produce_print(message_photo_out, message_photo_path)
        os.remove(os.path.join(message_photo_path, message_photo_out))
        
    if data.startswith(callback_data_show):
        value_sent = data.split(callback_data_show)[-1]
        message_id, message_photo = value_sent.split(callback_separator)
        bot.send_message(data_user, text='Checking_2', reply_to_message_id=message_id)
        message_photo_name, message_photo_path = telegram_us.detect_usage_location(message_photo, callback_data_show)
        
    if data.startswith(callback_data_delete):
        value_sent = data.split(callback_data_delete)[-1]
        message_id, message_photo = value_sent.split(callback_separator)
        bot.send_message(data_user, text='Checking_3', reply_to_message_id=message_id)
        message_photo_name, message_photo_path = telegram_us.detect_usage_location(message_photo, callback_data_delete)


if __name__ == '__main__':
    bot.polling()