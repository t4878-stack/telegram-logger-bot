import os
import asyncio
from datetime import datetime
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =====================
# CONFIG
# =====================
TOKEN = os.environ.get("8542143557:AAEwuIFQCmyEU1EmiCEixA738H0UumiBt1I")
PORT = int(os.environ.get("PORT", 10000))

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN not set")

# =====================
# FLASK (for Render)
# =====================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive."

# =====================
# TELEGRAM BOT
# =====================
user_logs = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام.\nپیام بفرست، ذخیره می‌کنم.\n/show = نمایش پیام‌ها"
    )

async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    time = datetime.now().strftime("%H:%M")

    user_logs.setdefault(user_id, [])
    user_logs[user_id].append(f"{time} | {text}")

    await update.message.reply_text(f"ثبت شد: {time}")

async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    msgs = user_logs.get(user_id)

    if not msgs:
        await update.message.reply_text("چیزی ثبت نشده.")
        return

    await update.message.reply_text("\n".join(msgs))

async def run_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()

    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("show", show))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_message))

    await app_bot.run_polling()

# =====================
# MAIN
# =====================
async def main():
    # Flask باید جدا اجرا بشه
    loop = asyncio.get_running_loop()
    loop.run_in_executor(
        None,
        lambda: app.run(host="0.0.0.0", port=PORT)
    )

    await run_bot()

if __name__ == "__main__":
    asyncio.run(main())
