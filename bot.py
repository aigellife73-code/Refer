import logging
import random
import string
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)
import requests

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TELEGRAM_BOT_TOKEN = "9019675422:AAHczIEp7XDWvMtrmbrVAdrSGRHizWGMo7E"
REFER_OPTIONS = [1, 3, 5, 10, 20, 50]


def generate_random_credentials():
  phone = str(random.choice([6, 7, 8, 9])) + "".join(
      random.choices(string.digits, k=9)
  )
  password = "".join(
      random.choices(string.ascii_letters + string.digits, k=8)
  )
  return phone, password


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  keyboard = []
  row = []
  for count in REFER_OPTIONS:
    row.append(
        InlineKeyboardButton(
            f"🚀 {count} Refer", callback_data=f"start_refer_{count}"
        )
    )
    if len(row) == 2:
      keyboard.append(row)
      row = []
  if row:
    keyboard.append(row)

  reply_markup = InlineKeyboardMarkup(keyboard)
  await update.message.reply_text(
      "👋 **Auto Refer Bot Started!**\n\nKitne refer ek sath karne hain, option"
      " select karein:",
      reply_markup=reply_markup,
      parse_mode="Markdown",
  )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  data = query.data
  if data.startswith("start_refer_"):
    count = int(data.split("_")[2])
    chat_id = query.message.chat_id

    await query.edit_message_text(
        text=(
            f"⚙️ **{count} Refer** ki process shuru ho chuki hai...\nKripya"
            " thoda intezaar karein."
        ),
        parse_mode="Markdown",
    )

    for i in range(count):
      phone, password = generate_random_credentials()
      try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"✅ **Refer Successful ({i+1}/{count})**\n📱 Number:"
                f" `{phone}`\n🔑 Password: `{password}`"
            ),
            parse_mode="Markdown",
        )
      except Exception as e:
        await context.bot.send_message(
            chat_id=chat_id, text=f"❌ Error with number {phone}: {str(e)}"
        )

    await context.bot.send_message(
        chat_id=chat_id, text="🎉 Selected batch ke sabhi refers complete ho gaye!"
    )


def main():
  application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(button_handler))
  print("Bot is running...")
  application.run_polling()


if __name__ == "__main__":
  main()
