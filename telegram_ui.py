import os
import io
import telebot
from image_parser import ImageParser
from telegram_usage import TelegramUsage
from config import bot_key


bot = telebot.TeleBot(bot_key)
telegram_us = TelegramUsage()

@bot.message_handler(content_types= ["photo"])
def take_photo(message):
    value_photos = []
    for photos in message.photo:
        raw = photos.file_id
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        value_photos.append(telegram_us.save_tmp_file(downloaded_file))
    value_photo = telegram_us.detect_less_compressed(value_photos)
    print(value_photo)
    print('+++++++++++++++++++++++++++')
    #TODO add the extintions and send it as file?

@bot.message_handler(content_types=['document'])
def take_photo_uncompressed(message):
    print('They have printed document')
    print('====================================')
    # save_dir = message.caption
    # save_dir = os.getcwd()
    file_name = message.document.file_name
    print(file_name)
    print('-----------------------------')
    file_id = message.document.file_name
    print(file_id)
    print('=====================================')
    file_id_info = bot.get_file(message.document.file_id)
    print(file_id_info)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    # downloaded_file = bot.download_file(file_id_info.file_path)
    # src = file_name
    #TODO complete the download of photo

if __name__ == '__main__':
    bot.polling()