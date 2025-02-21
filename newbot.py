import os
from dotenv import load_dotenv
import logging
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

load_dotenv()

access_token = os.getenv('CHATBUDDY_ACCESS_TOKEN')
bot_username = os.getenv('BOT_USERNAME')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Dictionary to store unread messages for each user
unread_messages = {}

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(f"Hello {user.first_name}! Use /summarize to get a summary of unread messages.")

async def summarize(update: Update, context: CallbackContext) -> None:
    """Summarize unread messages for the user."""
    user_id = update.effective_user.id
    if user_id in unread_messages:
        messages = unread_messages[user_id]
        summary = "\n".join(messages)
        await update.message.reply_text(f"Summary of unread messages:\n{summary}")
        unread_messages[user_id] = []  # Clear the messages after summarizing
    else:
        await update.message.reply_text("No unread messages found.")

async def store_message(update: Update, context: CallbackContext) -> None:
    """Store messages from the group."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_text = update.message.text

    # Check if the message is from a group (not a private chat)
    if chat_id != user_id:
        # Store the message for all users in the group
        members = await context.bot.get_chat_members(chat_id)
        for member in members:
            if member.user.id != user_id:  # Exclude the sender
                if member.user.id not in unread_messages:
                    unread_messages[member.user.id] = []
                unread_messages[member.user.id].append(message_text)

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(access_token).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("summarize", summarize))

    # Message handler for storing messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, store_message))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
