from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime, timedelta
import asyncio

TOKEN = "8542143557:AAEwuIFQCmyEU1EmiCEixA738H0UumiBt1I"

user_logs = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! پیام هاتو بفرست تا با زمان ثبت کنم.\n"
        "برای دیدن همه پیام‌ها /show رو بزن."
    )

async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    now = datetime.now().strftime("%H:%M")

    if user_id not in user_logs:
        user_logs[user_id] = []

    user_logs[user_id].append(f"ساعت {now} : {text}")
    await update.message.reply_text(f"ساعت {now} : {text}")

async def show_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_logs and user_logs[user_id]:
        message = "\n".join(user_logs[user_id])
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("هیچ پیامی ثبت نشده است.")

async def daily_summary(app):
    while True:
        now = datetime.utcnow() + timedelta(hours=3, minutes=30)  # ایران
        target = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        wait_seconds = (target - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        for user_id, logs in user_logs.items():
            if logs:
                await app.bot.send_message(chat_id=user_id, text="جمع‌بندی روزانه شما:\n" + "\n".join(logs))
                user_logs[user_id] = []

async def post_init(app):
    asyncio.create_task(daily_summary(app))

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("show", show_logs))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_message))

    print("Bot running...")
    app.run_polling()
