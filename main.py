from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime, timedelta
import asyncio

TOKEN = "8542143557:AAEwuIFQCmyEU1EmiCEixA738H0UumiBt1I"

# دیکشنری برای ذخیره پیام‌ها به ازای هر کاربر
user_logs = {}

def iran_now():
    return datetime.utcnow() + timedelta(hours=3, minutes=30)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! پیام هاتو بفرست تا با زمان ثبت کنم.\n"
        "برای دیدن همه پیام‌ها /show رو بزن."
    )

async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    now = iran_now().strftime("%H:%M")
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
        now = iran_now()
        # ساعت 00:00 ایران
        target = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if now >= target:
            target += timedelta(days=1)
        wait_seconds = (target - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        # جمع‌بندی برای همه کاربران
        for user_id, logs in user_logs.items():
            if logs:
                message = "💡 جمع‌بندی دیروز:\n" + "\n".join(logs)
                await app.bot.send_message(chat_id=user_id, text=message)
        # خالی کردن لیست‌ها
        user_logs.clear()

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",_
