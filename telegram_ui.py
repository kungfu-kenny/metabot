import telebot
from config import bot_key

bot = telebot.Telebot(bot_key)

@bot.message_handler(content_types= ["photo"])
def verifyUser(message):
    print ("Got photo")