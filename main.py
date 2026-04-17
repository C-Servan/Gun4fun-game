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
from telebot import types  # Asegúrate de que esta línea esté arriba del todo

@bot.message_handler(commands=['game'])
def list_games(message):
    # Creamos el teclado con botones
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # Botón para el Juego 1
    btn1 = types.InlineKeyboardButton("🎮 Jugar: Super Shooter 01", callback_data="play_shooter_01")
    # Botón para el Juego 2
    btn2 = types.InlineKeyboardButton("🚀 Jugar: Super Shooter 02 (PRO)", callback_data="play_shooter_02")
    
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, "🏅 **CAMPO DE ENTRENAMIENTO GUN4FUN**\nSelecciona una misión, soldado:", reply_markup=markup, parse_mode="Markdown")

# Manejador para detectar qué botón han pulsado
@bot.callback_query_handler(func=lambda call: call.data.startswith("play_"))
def handle_game_selection(call):
    if call.data == "play_shooter_01":
        bot.send_game(call.message.chat.id, "shooter_01")
    elif call.data == "play_shooter_02":
        bot.send_game(call.message.chat.id, "shooter_02")
    
    # Esto quita el "reloj de arena" del botón en Telegram
    bot.answer_callback_query(call.id)
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)
