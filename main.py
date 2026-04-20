import os
import telebot
import random
from flask import Flask
from threading import Thread
from telebot import types

# --- 1. CONFIGURACIÓN DEL SERVIDOR WEB ---
app = Flask('')

@app.route('/')
def home():
    return "¡Bot Gun4Fun está vivo y operando!"

def run_server():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_server)
    t.daemon = True
    t.start()

# --- 2. CONFIGURACIÓN DEL BOT DE TELEGRAM ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- BASE DE DATOS DE FRASES (Se mantiene igual) ---
FRASES_INSTRUCTOR = [
    "¡ATENCIÓN! Soldados de verdad en la Misión 2. ¡Sigan así!",
    "¡Sin piedad, reclutas! El ranking no perdona debilidades.",
    # ... (Mantén tus 80 frases aquí)
]

# Comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy el Instructor de Gun4fun. Usa /game para empezar en el campo de entrenamiento. ¡Estás listo soldado!")

# --- CORRECCIÓN CRÍTICA EN /GAME ---
@bot.message_handler(commands=['game'])
def list_games(message):
    try:
        # Misión 1
        markup01 = types.InlineKeyboardMarkup()
        # REGLA DE ORO: El botón de juego DEBE ser el primero
        btn_play01 = types.InlineKeyboardButton("🎮 Jugar Misión 1", callback_game=types.CallbackGame())
        btn_rank01 = types.InlineKeyboardButton("🏆 Ver Ranking", callback_data="rank_01")
        markup01.row(btn_play01) # Fila 1: Solo el juego
        markup01.row(btn_rank01) # Fila 2: El ranking
        
        bot.send_game(message.chat.id, "shooter_01", reply_markup=markup01)

        # Misión 2
        markup02 = types.InlineKeyboardMarkup()
        btn_play02 = types.InlineKeyboardButton("🎮 Jugar Misión 2", callback_game=types.CallbackGame())
        btn_rank02 = types.InlineKeyboardButton("🏆 Ver Ranking", callback_data="rank_02")
        markup02.row(btn_play02)
        markup02.row(btn_rank02)

        bot.send_game(message.chat.id, "shooter_02", reply_markup=markup02)
        
    except Exception as e:
        print(f"Error en comando /game: {e}")
        bot.send_message(message.chat.id, "Instructor informando: Hubo un fallo en la entrega del equipo. Comandante, verifique el nombre de los juegos en BotFather.")

# Manejador de callbacks corregido
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        # Prioridad 1: Botones de Ranking (callback_data)
        if call.data and call.data.startswith("rank_"):
            mision = "Misión 1" if "01" in call.data else "Misión 2"
            msg = f"🪖 INFORME DEL INSTRUCTOR: {mision}\n\n1. @Comandante - 500\n2. @Soldado1 - 400\n\n¡A las armas!"
            bot.answer_callback_query(call.id, text=msg, show_alert=True)
        
        # Prioridad 2: Botones de Juego (game_short_name)
        elif call.game_short_name:
            if call.game_short_name == 'shooter_01':
                bot.answer_callback_query(call.id, url="https://c-servan.github.io/Gun4fun-game/v1/")
            elif call.game_short_name == 'shooter_02':
                bot.answer_callback_query(call.id, url="https://c-servan.github.io/Gun4fun-game/v2/")
        
        else:
            bot.answer_callback_query(call.id)
            
    except Exception as e:
        print(f"Error en callback: {e}")
        bot.answer_callback_query(call.id, text="Error en el sistema de telemetría.")

# --- 3. ARRANQUE ---
if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)