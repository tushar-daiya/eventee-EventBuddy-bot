import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

access_token = os.getenv('TUSHAR_BOT_ACCESS_TOKEN')
# bot_username = os.getenv('BOT_USERNAME')

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = "Hello 👋 I am ChatSummarizer.\nI summarize numerous text messages.\nInvite me into your groups and I will summarize them for you."
    await update.message.reply_text(response)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am here to help.")

# async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("This is a custom command")


# Responses
def handle_response(text: str):
    return 'Responding'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'Text: {text}\nType: {message_type}')
    return
    response = 'responding'

    # if message_type == 'private':
    #     response = handle_response(text) + ' to private text'
    # else:
    #     response = handle_response(text) + ' to group text'
    # elif bot_username in text:
    #     new_text = text.replace(bot_username, '').strip()
    #     response = handle_response(new_text)
    # else:
    #     return

    await update.message.reply_text(response)


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('Update:',update,'caused error',context.error)


if __name__ == "__main__":
    print('Starting bot... ')
    app = Application.builder().token(access_token).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    # app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    # app.add_error_handler(error)

    print('Polling... ')
    app.run_polling(poll_interval=3)
