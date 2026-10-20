import logging
import os

from telegram import (
  Update,
  InlineKeyboardButton,
  InlineKeyboardMarkup,
)
from telegram.ext import (
  Application,
  CommandHandler,
  ContextTypes,
  CallbackQueryHandler,
)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
  """Welcome the user."""
  user = update.effective_user
  message = update.effective_message

  if message is None:
    logger.warning("Received an update without a message.")
    return

  first_name = user.first_name if user else "there"

  keyboard = [
    [
      InlineKeyboardButton(
        "ℹ️ About",
                callback_data="about",
            ),
      InlineKeyboardButton(
        "🆘 Help",
        callback_data="help",
        ),
    ],
  ]

  reply_markup = InlineKeyboardMarkup(keyboard)

  await message.reply_text(
    f"Hello, {first_name}!\n\n"
    "I'm your friendly bot here to assist you. Use the buttons below or type /help to see what I can do.",
    reply_markup=reply_markup
  )

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
  """Provide help information to the user."""
  message = update.effective_message

  if message is None:
    logger.warning("Received an update without a message.")
    return

  await message.reply_text(
    "Here are the commands you can use:\n\n"
    "/start - Start the bot\n"
    "/help - Show available commands\n"
    "/about - Learn more about this bot\n"
    "/ping - Check the bot's responsiveness\n"
)

async def about(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
  """Provide information about the bot."""
  message = update.effective_message

  if message is None:
    logger.warning("Received an update without a message.")
    return

  await message.reply_text(
    "This bot is designed to assist users with various tasks. "
    "It can respond to commands, provide information, and more. "
    "Feel free to explore its capabilities!"
)

async def ping(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
  """Respond to the user with a 'Pong!' message."""
  message = update.effective_message

  if message is None:
    logger.warning("Received an update without a message.")
    return

  await message.reply_text("Pong! 🏓")

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
  """Log unexpected errors."""
  logger.error(
    msg="Exception while handling an update:",
    exc_info=context.error
  )

def main() -> None:
  """Configure and start the bot."""
  token = os.getenv("TELEGRAM_BOT_TOKEN")

  if not token:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set.")

  application = Application.builder().token(token).build()

  # Register command handlers
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CommandHandler("help", help_command))
  application.add_handler(CommandHandler("about", about))
  application.add_handler(CommandHandler("ping", ping))

  # Register error handling
  application.add_error_handler(error_handler)

  logger.info("Bot is starting...")
  application.run_polling()

if __name__ == "__main__":
  main()