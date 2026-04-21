import os
import telebot
import random
import time
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

# ID DEL GRUPO DE PRUEBA CONFIGURADO
ID_GRUPO_OBJETIVO = -1002035446864

# --- BASE DE DATOS: 80 FRASES DEL INSTRUCTOR (ÍNTEGRAS) ---
FRASES_INSTRUCTOR = [
    # Bloque A: Motivación
    "¡ATENCIÓN! He revisado los registros y parecen soldados de verdad. ¡Sigan así!",
    "¡Reclutas, el informe de bajas es impresionante! No se relajen.",
    "¡Escuchen bien! El operativo destacado está marcando el paso.",
    "¡A las armas! El ranking está que arde.",
    "¡Buen trabajo, soldados! El Alto Mando está satisfecho... por ahora.",
    "¡Fuego a discreción! Habéis convertido la jungla en vuestro patio.",
    "Veo que las raciones han sentado bien. ¡Puntuaciones de élite!",
    "¡A formar! Es un orgullo ver vuestros nombres en este informe.",
    "Soldados, vuestra eficiencia ha subido un 200%. ¡Ese es el espíritu!",
    "¡Atención! La Misión 2 tiene nuevos dueños en este Top 5.",
    "No esperaba menos de una unidad bajo mi mando. ¡Leyendas!",
    "¡Reclutas, habéis demostrado que los obstáculos son solo objetivos!",
    "¡Mirad ese ranking! Es poesía bélica en estado puro.",
    "¡Excelente despliegue! El enemigo está en retirada.",
    "Soldados, hoy descansáis como héroes, mañana os quiero más rápidos.",
    "¡Esa es la actitud! Sangre, sudor y píxeles. ¡Gran trabajo!",
    "El Instructor reconoce vuestro valor. ¡Defiendan esa posición!",
    "¡Impresionante! Habéis batido el récord de la unidad.",
    "¡A la carga! Que el mundo sepa quién domina esta jungla.",
    "Soldados, habéis cumplido el objetivo. ¡A disfrutar del botín!",
    # Bloque B: Sarcasmo
    "¡Reclutas! He visto tortugas con más iniciativa. ¡Muevan el culo!",
    "¿Eso es todo? Mi abuela disparaba mejor y tenía menos lag.",
    "Soldados, el objetivo es eliminar enemigos, no hacerse selfies.",
    "Veo muchos nombres abajo. ¿Están de vacaciones o tienen miedo?",
    "¡Atención! Si el ranking fuera un desfile, iríais marcha atrás.",
    "¿Disparáis balas o palomitas? ¡Esa puntería es de vergüenza!",
    "He visto reclutas con más agallas en su primer día. ¡Espabilad!",
    "Soldado, si buscas el botón de 'rendirse', te has equivocado.",
    "¿Esa es vuestra puntuación o la temperatura? ¡Es ridícula!",
    "¡Reclutas! No quiero excusas, quiero bajas en mi escritorio.",
    "Si la jungla hablara, se estaría riendo de vuestro rendimiento.",
    "He visto simuladores de paseo más intensos. ¡Acción!",
    "Soldados, dejad de jugar con las plantas y usad el plomo.",
    "¡Atención! El último del ranking limpiará las letrinas.",
    "Vuestra técnica es tan mala que el enemigo muere de risa.",
    "¡Reclutas! ¿Necesitáis un mapa para entrar en el Top 5?",
    "He visto bots con más carisma y puntería. ¡Penoso!",
    "La próxima vez, aseguraos de llevar el seguro quitado.",
    "¿Eso ha sido un disparo o un estornudo? ¡Meteos en la pelea!",
    "El Instructor está decepcionado. El Top 5 salva el honor.",
    # Bloque C: Estilo Gun4Fun
    "¡Soldados! La Misión 2 no se completa sola. Vigilo.",
    "¡Recluta del Top 1, invite a una ronda! Menuda marca.",
    "¡A formar! El ranking está listo. ¡Fuego a discreción!",
    "La inteligencia confirma: el Top 5 son leyendas. El resto... sigan.",
    "¡Soldados, uníos! La puntería necesita un ajuste.",
    "¡Misión 2 informando! Nuestros reclutas son más duros.",
    "¡Instructor en el canal! El ranking separa hombres de niños.",
    "Recordad: en Gun4Fun no hay medallas por participar, solo por dominar.",
    "¡Asegurad el perímetro! El viernes rendiréis cuentas.",
    "¡Reclutas! El ranking es vuestro espejo. ¿Os gusta?", 
    "Soldados, la jungla es nuestra. Recordádselo al enemigo.",
    "¡Gun4Fun no duerme! He contado vuestras bajas toda la noche.",
    "¡Atención! El Top 5 será recordado en los anales de la misión.",
    "No hay mayor gloria que ver tu nombre en lo más alto.",
    "¡Soldados! Vuestra misión es superar al de arriba.",
    "El Instructor ha hablado: ¡menos charla y más acción!",
    "¡Reclutas! La Misión 2 es vuestro examen. ¿Vais a suspender?",
    "¡Fuego! El ranking semanal es el único informe que importa.",
    "Soldados, haced que cada bala cuente. No regalo puntos.",
    "¡Gun4Fun al frente! Demostrad que sois de élite.",
    # Bloque D: Breves
    "¡Sin piedad! El ranking no perdona debilidades.",
    "¡Rompan filas! El Top 5 les espera.",
    "¡Instructor informando! Tenemos héroes aquí.",
    "¡Aseguren marcas! La gloria es para los persistentes.",
    "¡Última llamada! ¡A jugar!",
    "¡A las armas! El ranking se actualiza ahora.",
    "¡Puntuaciones de infarto! Buen trabajo.",
    "¡Reclutas, al frente! Quiero el máximo.",
    "¡Ranking listo para revisión!",
    "¡Fuego y gloria! Mirad el Top 5.",
    "¡A por el récord! Sin excusas.",
    "¡Disciplina y puntería! Es todo.",
    "¡Informe de bajas procesado!",
    "¡A los puestos de combate!",
    "¡Sin descanso hasta el Top 1!",
    "¡Misión activa! Ranking actualizado.",
    "¡Objetivo cumplido!",
    "¡Honor y puntos!",
    "¡Demostrad vuestra valía!",
    "¡Rompan filas y a disparar!",
    "¡Instructor fuera! Al combate."
]

# --- 3. NUEVO: HILO DE AUTOMATIZACIÓN (El Sargento) ---
def tarea_diaria():
    while True:
        # 86400 segundos = 24 horas. El primer mensaje sale a las 24h de encender el bot.
        time.sleep(86400) 
        try:
            # Elegimos una frase de motivación/sarcasmo para el aviso diario
            frase_aviso = random.choice(FRASES_INSTRUCTOR)
            mensaje = f"🪖 MENSAJE DEL INSTRUCTOR 🪖\n\n\"{frase_aviso}\"\n\nSoldados, no dejen que el ranking se enfríe. ¡Usen /game para desplegarse!"
            bot.send_message(ID_GRUPO_OBJETIVO, mensaje, parse_mode="Markdown")
        except Exception as e:
            print(f"Error en tarea diaria: {e}")

# Iniciamos el hilo de la tarea diaria sin bloquear el bot
t_diaria = Thread(target=tarea_diaria)
t_diaria.daemon = True
t_diaria.start()

# --- 4. MANEJADORES DE COMANDOS ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy el Instructor de Gun4fun. Usa /game para empezar en el campo de entrenamiento. ¡Estás listo soldado!")

@bot.message_handler(commands=['game'])
def list_games(message):
    # Misión 01
    bot.send_message(message.chat.id, "🎯 MISIÓN 01: ENTRENAMIENTO BÁSICO", parse_mode="Markdown")
    bot.send_game(message.chat.id, "shooter_01")

    # Misión 02
    bot.send_message(message.chat.id, "🎯 MISIÓN 2: OPERACIÓN JUNGLE FURY", parse_mode="Markdown")
    bot.send_game(message.chat.id, "shooter_02")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🏆 VER RANKING DE COMBATE", callback_data="ver_ranking"))
    bot.send_message(message.chat.id, "📊 ESTADÍSTICAS DE CAMPAÑA", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # Capturamos quién está interactuando
    user = call.from_user
    nombre_soldado = user.username if user.username else user.first_name

    if call.data == 'ver_ranking':
        frase = random.choice(FRASES_INSTRUCTOR)
        # Aquí podrías integrar la lectura real de Firebase en el futuro
        ranking_text = f"🪖 {frase}\n\n1. @Comandante - 5000\n2. @Soldado_Rambo - 4200\n3. @Elite_Sniper - 3800\n\n¡Vuelve a la carga!"
        bot.answer_callback_query(call.id, text=ranking_text, show_alert=True)
    
    elif call.game_short_name == 'shooter_01':
        # Añadimos el parámetro ?user= para que el juego sepa quién juega
        bot.answer_callback_query(call.id, url=f"https://c-servan.github.io/Gun4fun-game/v1/?user={nombre_soldado}")
        
    elif call.game_short_name == 'shooter_02':
        # Añadimos el parámetro ?user= para que el juego sepa quién juega
        bot.answer_callback_query(call.id, url=f"https://c-servan.github.io/Gun4fun-game/v2/?user={nombre_soldado}")
    else:
        bot.answer_callback_query(call.id)

# --- 5. ARRANQUE COMBINADO ---
if __name__ == "__main__":
    print("Lanzando servidor de vida...")
    keep_alive()
    print("Bot iniciando polling...")
    bot.polling(none_stop=True)
