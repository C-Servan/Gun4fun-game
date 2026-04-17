import os
import telebot
from flask import Flask
from threading import Thread

# Configuración del servidor web para Render
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Configuración del Bot
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy Gun4fun-game. Estoy listo para los juegos.")

if name == "__main__":
    # Arranca el servidor web en un hilo aparte
    t = Thread(target=run)
    t.start()
    # Arranca el bot
    bot.polling(none_stop=True)
