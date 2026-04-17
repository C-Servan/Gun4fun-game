import os
import telebot
from flask import Flask
from threading import Thread
from telebot import types

# --- 1. CONFIGURACIÓN DEL SERVIDOR WEB (Para evitar que Render se duerma) ---
app = Flask('')

@app.route('/')
def home():
    return "¡Bot Gun4Fun está vivo y operando!"

def run_server():
    # Render usa el puerto de la variable PORT, si no existe usa el 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_server)
    t.daemon = True
    t.start()

# --- 2. CONFIGURACIÓN DEL BOT DE TELEGRAM ---
# Asegúrate de que en Render has puesto la variable "BOT_TOKEN"
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy el Instructor de Gun4fun. Usa /game para empezar en el campo de entrenamiento. ¡Estás listo soldado!")

# Comando /game
@bot.message_handler(commands=['game'])
def list_games(message):
    # Misión 01
    bot.send_message(message.chat.id, "🎯 **MISIÓN 01: ENTRENAMIENTO BÁSICO**", parse_mode="Markdown")
    bot.send_game(message.chat.id, "shooter_01")

    # Misión 02
    bot.send_message(message.chat.id, "🚀 **MISIÓN 02: ASALTO TÁCTICO (PRO)**", parse_mode="Markdown")
    bot.send_game(message.chat.id, "shooter_02")

# Manejador de los botones de "Play" de los juegos
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.game_short_name == 'shooter_01':
        bot.answer_callback_query(call.id, url="https://c-servan.github.io/Gun4fun-game/v1/")
    elif call.game_short_name == 'shooter_02':
        bot.answer_callback_query(call.id, url="https://c-servan.github.io/Gun4fun-game/v2/")
    else:
        bot.answer_callback_query(call.id)

# --- 3. ARRANQUE COMBINADO ---
if __name__ == "__main__":
    print("Lanzando servidor de vida...")
    keep_alive()  # Arranca Flask en un hilo separado
    print("Bot iniciando polling...")
    bot.polling(none_stop=True) # Arranca el bot
