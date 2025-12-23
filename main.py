import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# حافظه موقت
user_logs = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "هر پیامی بفرستی با ساعت ثبت می‌کنم.\n"
        "برای دیدن لاگ‌ها /show رو بزن."
    )

async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    now = datetime.now().strftime("%H:%M")

    user_logs.setdefault(user_id, [])
    user_logs[user_id].append(f"ساعت {now} : {text}")

    await update.message.reply_text(f"ساعت {now} : {text}")

async def show_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logs = user_logs.get(user_id)

    if not logs:
        await update.message.reply_text("هیچ پیامی ثبت نشده.")
        return

    await update.message.reply_text("\n".join(logs))

if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("❌ TELEGRAM_BOT_TOKEN تنظیم نشده")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("show", show_logs))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_message))

    print("✅ Bot running...")
    app.run_polling()
