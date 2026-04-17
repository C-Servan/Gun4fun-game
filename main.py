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

# --- COMANDO /GAME CON MENÚ VISUAL ---
@bot.message_handler(commands=['game'])
def list_games(message):
    # Enlaces RAW extraídos de tus archivos
    url_img_1 = "https://raw.githubusercontent.com/C-Servan/Gun4fun-game/main/assets/portada1.jpg"
    url_img_2 = "https://raw.githubusercontent.com/C-Servan/Gun4fun-game/main/assets/portada2.jpg"

    # --- ENVIAR JUEGO 1 ---
    markup1 = types.InlineKeyboardMarkup()
    # Importante: el callback_data debe coincidir con el nombre corto en BotFather
    btn1 = types.InlineKeyboardButton("🎮 Jugar Misión 01", callback_data="shooter_01")
    markup1.add(btn1)
    
    bot.send_photo(
        message.chat.id, 
        url_img_1, 
        caption="🔹 **MISIÓN 01: ENTRENAMIENTO BÁSICO**\nPractica tu puntería con los objetivos móviles.", 
        parse_mode="Markdown", 
        reply_markup=markup1
    )

    # --- ENVIAR JUEGO 2 ---
    markup2 = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton("🚀 Jugar Misión 02 (PRO)", callback_data="shooter_02")
    markup2.add(btn2)

    bot.send_photo(
        message.chat.id, 
        url_img_2, 
        caption="🔹 **MISIÓN 02: ASALTO TÁCTICO**\nEntrenamiento avanzado con motor Phaser 3.", 
        parse_mode="Markdown", 
        reply_markup=markup2
    )

# --- MANEJADORES DE APERTURA (Para que los botones funcionen) ---
@bot.callback_query_handler(func=lambda call: call.game_short_name == 'shooter_01')
def game1_callback(call):
    bot.answer_callback_query(call.id, url="https://c-servan.github.io/Gun4fun-game/v1/")

@bot.callback_query_handler(func=lambda call: call.game_short_name == 'shooter_02')
def game2_callback(call):
    bot.answer_callback_query(call.id, url="https://c-servan.github.io/Gun4fun-game/v2/")
    
    # Esto quita el "reloj de arena" del botón en Telegram
    bot.answer_callback_query(call.id)
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)
