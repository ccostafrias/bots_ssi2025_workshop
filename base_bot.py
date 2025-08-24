from telegram import Update
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, ContextTypes
from math import pow
import datetime
import os

# Carregar variáveis do arquivo .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

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
	    "/lembrete - Recebe um tempo (em minutos) e uma mensagem que será exibida depois desse tempo",
        "/faltamdias - Recebe uma data (DD MM AAAA) e saiba quantos dias faltam para chegar nessa data",
	    "/bhaskara - Recebe os coeficientes de uma equação quadrática e calcula as raízes da equação!",
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
        return "segunda"
    elif dia_semana == 1:
        return "terca"
    elif dia_semana == 2:
        return "quarta"
    elif dia_semana == 3:
        return "quinta"
    elif dia_semana == 4:
        return "sexta"
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


async def faltamdias(update: Update, context: ContextTypes.DEFAULT_TYPE):
	try:
		if len(context.args) != 3:
			await update.message.reply_text("Use assim: /faltam DD MM AAAA")
			return

		# Lê a data passada como argumento
		dia = int(context.args[0]) 
		mes = int(context.args[1])
		ano = int(context.args[2])
		data_alvo = datetime.date(ano, mes, dia)

		# Data de hoje
		hoje = datetime.date.today()

		# Calcula diferença
		if data_alvo < hoje:
			await update.message.reply_text("Essa data já passou!")
		else:
			faltam_dias = (data_alvo - hoje).days
			await update.message.reply_text(f"Faltam {faltam_dias} dias para {dia}/{mes}/{ano}")

	except ValueError:
		await update.message.reply_text("Formato inválido! Use: /faltam DD MM AAAA")
		
async def bhaskara(update: Update, context: ContextTypes.DEFAULT_TYPE):
	try:
		if len(context.args) != 3:
			await update.message.reply_text('Use assim: /bhaskara a b c')
			return
		
		a = float(context.args[0])
		b = float(context.args[1])
		c = float(context.args[2])
		
		delta = pow(b, 2) - (4*a*c)
		
		if delta < 0:
			await update.message.reply_text('Delta negativo, não há raízes reais!')
			return
		else:
			x1 = round(((-1*b)+pow(delta, 0.5))/2*a, 2)
			if delta == 0:
				await update.message.reply_text(f'Delta é 0, logo a única raíz é {x1}')
			else:
				x2 = round(((-1*b)-pow(delta, 0.5))/2*a, 2)
				await update.message.reply_text(f'Delta é {delta}, logo há duas raízes: {x1} e {x2}')			
		
		
	except ValueError:
		await update.message.reply_text("Formato inválido! Use: /bhaskara a b c")	

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
    app.add_handler(CommandHandler("faltamdias", faltamdias))
    app.add_handler(CommandHandler("bhaskara", bhaskara))

    print("Bot rodando... Pressione Ctrl+C para parar.")
    app.run_polling()

main()
