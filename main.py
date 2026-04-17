import os
import telebot
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy el Instructor de Gun4fun. Usa /game para empezar en el campo de entrenamiento. Estas listo soldado!.")
@bot.message_handler(commands=['game'])
def send_game(message):
    bot.send_game(message.chat.id, "shooter_01")

@bot.callback_query_handler(func=lambda call: call.game_short_name == 'shooter1')
def game_callback(call):
    # Aquí es donde pondremos el enlace al juego más adelante
    bot.answer_callback_query(call.id, url="https://c-servan.github.io/Gun4fun-game/")
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)
