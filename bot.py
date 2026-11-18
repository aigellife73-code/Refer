import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# Configuration from your input
TELEGRAM_BOT_TOKEN = "9019675422:AAHczIEp7XDWvMtrmbrVAdrSGRHizWGMo7E"
REFER_LINK = "https://okmgi.paykexo.com/#/register?code=ARU29SA"

# Allowed batch count options
REFER_OPTIONS = [1, 3, 5, 10, 20, 50]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Jab user /start bhejega, toh yeh fixed options dikhayega"""
  keyboard = []
  row = []
  for count in REFER_OPTIONS:
    row.append(
        InlineKeyboardButton(
            f"🚀 {count} Refer", callback_data=f"start_refer_{count}"
        )
    )
    if len(row) == 2:  # 2 buttons per row
      keyboard.append(row)
      row = []
  if row:
    keyboard.append(row)

  reply_markup = InlineKeyboardMarkup(keyboard)

  await update.message.reply_text(
      "👋 **Welcome to Auto Refer Bot!**\n\nKitne refer ek sath karne hain,कृपया"
      " neeche diye gaye option mein se select karein:",
      reply_markup=reply_markup,
      parse_mode="Markdown",
  )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  data = query.data
  if data.startswith("start_refer_"):
    count = int(data.split("_")[2])
    await query.edit_message_text(
        text=(
            f"⚙️ **{count} Refer** ki process shuru ki ja rahi hai...\nKripya"
            " thoda intezaar karein."
        ),
        parse_mode="Markdown",
    )

    # Yahan automation script run hogi (jaise Playwright ya Requests)
    # Success hone par number & password telegram par bheja jayega
    # Already registered / Send OTP par screenshot capture karke bheja jayega

    # Example simulation for demo:
    chat_id = query.message.chat_id

    # Dummy Simulation:
    # 1. Agar Already Registered mila:
    # await context.bot.send_photo(chat_id=chat_id, photo=open('already_registered.png', 'rb'), caption="⚠️ Number Already Registered!")

    # 2. Agar Send OTP click hua:
    # await context.bot.send_photo(chat_id=chat_id, photo=open('otp_sent.png', 'rb'), caption="📩 Send OTP Clicked successfully!")

    # 3. Success hone par:
    # await context.bot.send_message(chat_id=chat_id, text=f"✅ Success!\nNumber: 9876543210\nPassword: example_pass")


def main():
  application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(button_handler))

  print("Bot is running...")
  application.run_polling()


if __name__ == "__main__":
  main()
