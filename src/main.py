# src/main.py
"""
Ponto de entrada do agente virtual:
- Inicializa o bot Telegram
- Orquestra o fluxo CrewAI
- Usa ferramentas para Google Sheets, Calendar e Email
"""

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from src import config

# Estados do ConversationHandler
NOME, EMAIL, SERVICO, ESCOLHA_HORARIO = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Bem-vindo à Agência Criativa XYZ. Qual seu nome?")
    return NOME

async def receber_nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nome'] = update.message.text
    await update.message.reply_text("Qual seu e-mail?")
    return EMAIL

async def receber_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['email'] = update.message.text
    await update.message.reply_text("Qual tipo de serviço deseja (design, site, social media)?")
    return SERVICO

async def receber_servico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['servico'] = update.message.text
    # Aqui chamar função para registrar no Google Sheets
    # e sugerir horários (stub)
    horarios = ['10:00', '14:00', '16:00']  # Exemplo fixo
    context.user_data['horarios'] = horarios
    msg = "Escolha um dos horários disponíveis: " + ", ".join(horarios)
    await update.message.reply_text(msg)
    return ESCOLHA_HORARIO

async def escolher_horario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    horario = update.message.text
    if horario not in context.user_data['horarios']:
        await update.message.reply_text("Horário inválido. Escolha um dos sugeridos.")
        return ESCOLHA_HORARIO
    # Aqui criar evento no Google Calendar e gerar protocolo
    protocolo = '123456'  # Gerar aleatório depois
    link_meet = 'https://meet.google.com/xyz123'
    await update.message.reply_text(f"Agendamento confirmado para {horario}. Link: {link_meet}\nProtocolo: {protocolo}\nObrigado!")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_nome)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_email)],
            SERVICO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_servico)],
            ESCOLHA_HORARIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, escolher_horario)],
        },
        fallbacks=[]
    )
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
