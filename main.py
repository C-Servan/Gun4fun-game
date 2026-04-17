import os
import telebot

# Usaremos una variable de entorno para que tu Token no sea público
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Estoy preparándome para ser tu bot de juegos.")

if name == "__main__":
    bot.polling(none_stop=True)
