from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import datetime

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = update.message.text

    await update.message.reply_text(mensagem)



async def somas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
	resultado = 0  
	
        if len(args) < 2:
            await update.message.reply_text("Por favor, use assim: /soma 5 7 3 ...")
            return 
	
        for i in args:
	    num = float(i)
            resultado = resultado + num

        await update.message.reply_text(f"O resultado da soma é {resultado}")

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
