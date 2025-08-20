from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import datetime

TOKEN = "INSIRA SEU TOKEN AQUI"

# Contador global da função contagem
contador = 0

# Horários das aulas
horario_aulas = {
    "segunda": ["8:00 MQAM", "10:15 BD"],
    "terca": ["8:00 OAC II", "10:15 MQAM"],
    "quarta": ["8:00 Redes", "10:15 SO"],
    "quinta": ["8:00 BD", "10:15 OAC II"],
    "sexta": ["8:00 SO", "10:15 Redes"]
}

# ------------------------------
# Comandos do bot
# ------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Bem vindo a Owlficina de criação de bots no telegram! Digite '/help' para ver os comandos disponíveis!")



async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comandos = [
        "/start - Inicia o bot",
        "/oi - Troca de cumprimentos simples",
        "/contagem - Conta quantas vezes esse comando já foi usado",
        "/aulas - Mostra as próximas aulas",
	"/soma - Recebe 2 números e mostra o resultado da soma",
	"/lembrete - Recebe um tempo (em minutos) e uma mensagem que será exibida depois desse tempo"
    ]
    texto = "Comandos disponíveis neste bot:\n" + "\n".join(comandos)
    await update.message.reply_text(texto)



async def oi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Oi, tudo bem com você?")



#Função que mostra o número de vezes que essa função foi ativada
async def contagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global contador
    contador += 1
    await update.message.reply_text(f"Este comando já foi usado {contador} vezes!")



# Função que decide o dia a mostrar
def dia_aula_agora():
    now = datetime.datetime.now()
    dia_semana = now.weekday()  # 0=segunda, ..., 4=sexta
    hora = now.hour + now.minute/60

    if dia_semana == 0:  # segunda
        return "terca" if hora >= 12 else "segunda"
    elif dia_semana == 1:
        return "quarta" if hora >= 12 else "terca"
    elif dia_semana == 2:
        return "quinta" if hora >= 12 else "quarta"
    elif dia_semana == 3:
        return "sexta" if hora >= 12 else "quinta"
    elif dia_semana == 4:
        return "segunda" if hora >= 12 else "sexta"
    else:  # sábado ou domingo
        return "segunda"



async def aulas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dia = dia_aula_agora()
    aulas = horario_aulas[dia]
    texto = f"Próximas aulas ({dia.capitalize()}):\n" + "\n".join(aulas)
    await update.message.reply_text(texto)



async def soma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args  

        if len(args) < 2:
            await update.message.reply_text("Por favor, use assim: /soma 5 7")
            return

        num1 = float(args[0])
        num2 = float(args[1])
        resultado = num1 + num2

        await update.message.reply_text(f"A soma de {num1} + {num2} é {resultado}")

    except ValueError:
        await update.message.reply_text("Digite apenas números, exemplo: /soma 10 20")



# Função que será chamada pelo job
async def enviar_lembrete(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(chat_id=job.chat_id, text=f"Lembrete: {job.data}")


async def lembrete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Primeiro argumento = tempo em minutos
        tempo = int(context.args[0]) * 60

        # O resto da frase = mensagem do lembrete
        mensagem = " ".join(context.args[1:])
        if not mensagem:
            mensagem = "Lembrete!"

        # Agenda o lembrete
        chat_id = update.effective_chat.id
        context.job_queue.run_once(enviar_lembrete, when=tempo, chat_id=chat_id, data=mensagem)

        await update.message.reply_text(f"Lembrete criado! Vou te lembrar em {tempo} segundos.")

    except (IndexError, ValueError):
        await update.message.reply_text("Uso: /lembrete <minutos> <mensagem>")



# ------------------------------
# Função principal
# ------------------------------

def main():
    app = Application.builder().token(TOKEN).build()

    # Registra os handlers
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("oi", oi))
    app.add_handler(CommandHandler("contagem", contagem))
    app.add_handler(CommandHandler("aulas", aulas))
    app.add_handler(CommandHandler("soma", soma))
    app.add_handler(CommandHandler("lembrete", lembrete))

    print("Bot rodando... Pressione Ctrl+C para parar.")
    app.run_polling()

main()
