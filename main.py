import os
import telebot
from flask import Flask
from threading import Thread
from telebot import types

# --- CONFIGURACIÓN DEL SERVIDOR (Para Render) ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN DEL BOT ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy el Instructor de Gun4fun. Usa /game para empezar en el campo de entrenamiento. ¡Estás listo soldado!")

# --- COMANDO /GAME ---
@bot.message_handler(commands=['game'])
def list_games(message):
    # Ya no enviamos "send_photo", Telegram usará la imagen que subiste a BotFather
    
    # --- LANZAR MISIÓN 01 ---
    bot.send_message(message.chat.id, "🎯 **MISIÓN 01: ENTRENAMIENTO BÁSICO**", parse_mode="Markdown")
    bot.send_game(message.chat.id, "shooter_01")

    # --- LANZAR MISIÓN 02 ---
    bot.send_message(message.chat.id, "🚀 **MISIÓN 02: ASALTO TÁCTICO (PRO)**", parse_mode="Markdown")
    bot.send_game(message.chat.id, "shooter_02")

# --- MANEJADOR DE BOTONES ---
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.game_short_name == 'shooter_01':
        bot.answer_callback_query(call.id, url="https://c-servan.github.io/Gun4fun-game/v1/")
    elif call.game_short_name == 'shooter_02':
        bot.answer_callback_query(call.id, url="https://c-servan.github.io/Gun4fun-game/v2/")
    else:
        bot.answer_callback_query(call.id)

# --- ARRANQUE ---
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)
