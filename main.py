import os
from datetime import datetime
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import threading

TOKEN = os.environ.get("8542143557:AAEwuIFQCmyEU1EmiCEixA738H0UumiBt1I")


app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive."

user_logs = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! پیام بده ثبتش می‌کنم.")

async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    text = update.message.text
    t = datetime.now().strftime("%H:%M")

    user_logs.setdefault(uid, []).append(f"{t} : {text}")
    await update.message.reply_text(f"{t} : {text}")

async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    msgs = user_logs.get(uid, [])
    await update.message.reply_text("\n".join(msgs) if msgs else "چیزی نیست.")

def run_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("show", show))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_message))
    app_bot.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

