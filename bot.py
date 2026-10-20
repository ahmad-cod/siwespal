import logging
import os

from telegram import (
  Update,
  InlineKeyboardButton,
  InlineKeyboardMarkup,
  BotCommand,
)
from telegram.ext import (
  Application,
  CommandHandler,
  ContextTypes,
  CallbackQueryHandler,
  MessageHandler,
  filters,
)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
  """Handle button presses from the inline keyboard."""
  query = update.callback_query

  if query is None:
    logger.warning("Received a callback query without a query.")
    return

  await query.answer()

  if query.data == "about":
    await about(update, context)
  elif query.data == "help":
    await help_command(update, context)
  else:
    await query.edit_message_text(
      text="Unknown action. Please use the buttons provided."
    )

  
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

async def handle_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
  """Handle text messages that are not commands."""
  message = update.effective_message

  if message is None or message.text is None:
    logger.warning("Received an update without a message.")
    return

  text = message.text.strip().lower()

  if not text:
    await message.reply_text("You sent an empty message. Please type something.")
    return

  if text in ["hi", "hello", "hey"]:
    await message.reply_text("Hello! How can I assist you today?")
  elif text in ["bye", "goodbye", "see you"]:
    await message.reply_text("Goodbye! Have a great day!")
  else:
    await message.reply_text(
      "I'm not sure how to respond to that. "
      "Please use the buttons or type /help for assistance."
    )

async def post_init(
    application: Application
) -> None:
  """Set bot commands after the application has started."""
  commands = [
    BotCommand("start", "Start the bot"),
    BotCommand("help", "Show available commands"),
    BotCommand("about", "Learn more about this bot"),
    BotCommand("ping", "Check the bot's responsiveness"),
  ]
  await application.bot.set_my_commands(commands)

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

  application = (Application.builder()
                 .token(token)
                 .post_init(post_init)
                 .build()
                )

  # Register command handlers
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CommandHandler("help", help_command))
  application.add_handler(CommandHandler("about", about))
  application.add_handler(CommandHandler("ping", ping))
  application.add_handler(CallbackQueryHandler(button_handler))
  # Register message handler for text messages
  application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

  # Register error handling
  application.add_error_handler(error_handler)

  logger.info("Bot is starting...")
  application.run_polling()

if __name__ == "__main__":
  main()