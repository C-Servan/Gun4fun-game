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

# --- BASE DE DATOS COMPLETA: 80 FRASES DEL INSTRUCTOR ---
FRASES_INSTRUCTOR = [
    # Bloque A: Motivación (20)
    "¡ATENCIÓN! He revisado los registros de la Misión 2 y parecen soldados de verdad. ¡Sigan así!",
    "¡Reclutas, el informe de bajas es impresionante! Pero no se relajen, la jungla se traga a los confiados.",
    "¡Escuchen bien! El operativo destacado está marcando el paso. ¿Van a dejar que les de lecciones un recluta?",
    "¡A las armas! El ranking está que arde y el olor a pólvora me encanta por las mañanas.",
    "¡Buen trabajo, soldados! El Alto Mando de Gun4Fun está satisfecho... por ahora.",
    "¡Fuego a discreción! Habéis convertido la jungla en vuestro patio de recreo esta semana.",
    "Veo que las raciones de combate os han sentado bien. ¡Esas puntuaciones son de auténtica élite!",
    "¡A formar! Es un orgullo ver vuestros nombres en este informe. ¡Que no baje el ritmo!",
    "Soldados, vuestra eficiencia ha subido un 200%. ¡Ese es el espíritu de Gun4Fun!",
    "¡Atención! La Misión 2 tiene nuevos dueños y están en este Top 5.",
    "No esperaba menos de una unidad bajo mi mando. ¡Puntuaciones de leyenda!",
    "¡Reclutas, habéis demostrado que los obstáculos son solo objetivos a batir!",
    "¡Mirad ese ranking! Es poesía bélica en estado puro.",
    "¡Excelente despliegue! El enemigo está en retirada gracias a vuestra presión.",
    "Soldados, hoy descansáis como héroes, pero el viernes que viene os quiero más rápidos.",
    "¡Esa es la actitud! Sangre, sudor y píxeles. ¡Gran trabajo!",
    "El Instructor Gun4Fun reconoce vuestro valor. ¡Seguid defendiendo esa posición!",
    "¡Impresionante! Habéis batido el récord de efectividad de la unidad.",
    "¡A la carga! Que el mundo sepa quién domina esta jungla.",
    "Soldados, habéis cumplido el objetivo con honores. ¡A disfrutar del botín!",

    # Bloque B: Sarcasmo e Instrucción (20)
    "¡Reclutas! He visto tortugas con más iniciativa que algunos de ustedes. ¡Muevan el culo!",
    "¿Eso es todo lo que tienen? Mi abuela disparaba mejor y tenía menos lag.",
    "Soldados, el objetivo es eliminar enemigos, no hacerse selfies con las serpientes.",
    "Veo muchos nombres en la parte baja de la lista. ¿Están de vacaciones o la jungla les da miedo?",
    "¡Atención! Si el ranking fuera un desfile, algunos de ustedes irían marchando hacia atrás.",
    "¿Estáis disparando balas o palomitas? ¡Esa puntería es de vergüenza, reclutas!",
    "He visto reclutas con más agallas en su primer día de instrucción. ¡Espabilad!",
    "Soldado, si buscas el botón de 'rendirse', te has equivocado de juego. ¡A disparar!",
    "¿Esa es vuestra puntuación o es la temperatura ambiente? ¡Es ridícula!",
    "¡Reclutas! No quiero excusas, quiero bajas confirmadas en mi escritorio.",
    "Si la jungla hablara, se estaría riendo de vuestro rendimiento esta semana.",
    "He visto simuladores de paseo más intensos que vuestras partidas. ¡Acción!",
    "Soldados, dejad de jugar con las plantas y empezad a usar el plomo.",
    "¡Atención! El último del ranking limpiará las letrinas hasta el próximo viernes.",
    "Vuestra técnica es tan mala que los enemigos se mueren de risa, no de disparos.",
    "¡Reclutas! ¿Necesitáis un mapa o una invitación formal para entrar en el Top 5?",
    "He visto bots con más carisma y puntería que media unidad. ¡Penoso!",
    "Soldados, la próxima vez que entréis en la jungla, aseguraos de llevar el seguro quitado.",
    "¿Eso ha sido un disparo o un estornudo? ¡Meteos en la pelea de verdad!",
    "El Instructor está decepcionado. Menos mal que el Top 5 salva un poco el honor.",

    # Bloque C: Estilo Gun4Fun (20)
    "¡Soldados! La Misión 2 no se va a completar sola. El Instructor Gun4Fun vigila.",
    "¡Recluta del Top 1, solicito que invite a una ronda! Menuda puntuación.",
    "¡A formar! El ranking semanal está listo. Si no te gusta tu puesto: ¡Fuego a discreción!",
    "La inteligencia confirma que el Top 5 está lleno de leyendas. El resto... seguid intentándolo.",
    "¡Soldados, uníos! La puntuación colectiva sube, pero vuestra puntería necesita un ajuste.",
    "¡Misión 2 informando! El terreno está difícil, pero nuestros reclutas son más duros.",
    "¡Instructor Gun4Fun en el canal! El ranking de hoy separa a los soldados de los niños.",
    "Recordad reclutas: en Gun4Fun no hay medallas por participar, solo por dominar.",
    "¡Asegurad el perímetro! El viernes es el día de rendir cuentas ante este Instructor.",
    "¡Reclutas! El ranking es el espejo de vuestro esfuerzo. ¿Os gusta lo que veis?",
    "Soldados, la jungla es nuestra. Solo hay que recordárselo al enemigo cada día.",
    "¡Gun4Fun no duerme! El Instructor ha estado contando vuestras bajas toda la noche.",
    "¡Atención! El Top 5 de esta semana será recordado en los anales de la Misión 2.",
    "No hay mayor gloria que ver tu nombre en lo más alto del tablón.",
    "¡Soldados! Vuestra única misión es superar al que tenéis encima en la lista.",
    "El Instructor Gun4Fun ha hablado: ¡menos charla en el grupo y más acción!",
    "¡Reclutas! La Misión 2 es vuestro examen final. ¿Vais a suspender?",
    "¡Fuego! El ranking semanal es el único informe que me importa.",
    "Soldados, haced que cada bala cuente. El Instructor no regala los puntos.",
    "¡Gun4Fun al frente! Demostrad que sois la unidad de élite que este bot espera.",

    # Bloque D: Breves y Directas (20)
    "¡Sin piedad, reclutas! El ranking no perdona debilidades.",
    "¡Rompan filas y vayan directos al combate! El Top 5 les espera.",
    "¡Instructor Gun4Fun informando! Los números no mienten: tenemos héroes aquí.",
    "¡Aseguren el perímetro y superen esas marcas! La gloria es para los persistentes.",
    "¡Última llamada para los que quieran salir de la zona de confort! ¡A jugar!",
    "¡A las armas, soldados! El ranking se actualiza ahora.",
    "¡Puntuaciones de infarto! Buen trabajo unidad.",
    "¡Reclutas, al frente! No acepto menos que el máximo.",
    "¡Instructor Gun4Fun: Ranking listo para revisión!",
    "¡Fuego y gloria! Mirad el Top 5 de hoy.",
    "¡Soldados, a por el récord! No hay excusas.",
    "¡Disciplina y puntería! El ranking lo es todo.",
    "¡Atención! Informe de bajas procesado.",
    "¡Reclutas, a los puestos de combate!",
    "¡Sin descanso hasta llegar al Top 1!",
    "¡Misión 2 activa! Ranking actualizado.",
    "¡Instructor Gun4Fun: Objetivo cumplido!",
    "¡Soldados, honor y puntos!",
    "¡Reclutas, demostrad vuestra valía!",
    "¡Rompan filas y a disparar!",
    "¡Instructor fuera! El campo de batalla os espera."
]

# Comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy el Instructor de Gun4fun. Usa /game para empezar en el campo de entrenamiento. ¡Estás listo soldado!")

# Comando /game corregido
@bot.message_handler(commands=['game'])
def list_games(message):
    # Misión 1
    markup01 = types.InlineKeyboardMarkup()
    # Usamos callback_game para el botón de jugar y callback_data para el de ranking
    markup01.add(types.InlineKeyboardButton("🎮 Jugar Misión 1", callback_game=types.CallbackGame()))
    markup01.add(types.InlineKeyboardButton("🏆 Ver Ranking", callback_data="rank_01"))
    
    bot.send_message(message.chat.id, "🎯 **MISIÓN 1: ENTRENAMIENTO BÁSICO**", parse_mode="Markdown")
    bot.send_game(message.chat.id, "shooter_01", reply_markup=markup01)

    # Misión 2
    markup02 = types.InlineKeyboardMarkup()
    markup02.add(types.InlineKeyboardButton("🎮 Jugar Misión 2", callback_game=types.CallbackGame()))
    markup02.add(types.InlineKeyboardButton("🏆 Ver Ranking", callback_data="rank_02"))

    bot.send_message(message.chat.id, "🎯 **MISIÓN 2: OPERACIÓN JUNGLE FURY**", parse_mode="Markdown")
    bot.send_game(message.chat.id, "shooter_02", reply_markup=markup02)

# Manejador de callbacks corregido (Separando lógica de Juego y de Botones)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # 1. Si el callback es para INICIAR un juego
    if call.game_short_name:
        if call.game_short_name == 'shooter_01':
            bot.answer_callback_query(call.id, url="https://c-servan.github.io/Gun4fun-game/v1/")
        elif call.game_short_name == 'shooter_02':
            bot.answer_callback_query(call.id, url="https://c-servan.github.io/Gun4fun-game/v2/")
    
    # 2. Si el callback es un botón de RANKING (usa callback_data)
    elif call.data and call.data.startswith("rank_"):
        mision = "Misión 1" if "01" in call.data else "Misión 2"
        # Placeholder del ranking
        msg = f"🪖 INFORME DEL INSTRUCTOR: {mision}\n\n1. @Comandante - 500\n2. @Recluta1 - 450\n\n¡A las armas!"
        bot.answer_callback_query(call.id, text=msg, show_alert=True)
    
    # 3. Respuesta por defecto para evitar que el botón se quede "cargando"
    else:
        bot.answer_callback_query(call.id)

# --- 3. ARRANQUE ---
if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)