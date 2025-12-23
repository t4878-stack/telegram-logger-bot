from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime, timedelta, time
import asyncio

TOKEN = "8542143557:AAEwuIFQCmyEU1EmiCEixA738H0UumiBt1I"

# دیکشنری برای ذخیره پیام‌ها به ازای هر کاربر
user_logs = {}

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! پیام هاتو بفرست تا با زمان ثبت کنم.\n"
        "برای دیدن همه پیام‌ها /show رو بزن."
    )

# ذخیره پیام‌ها با زمان ایران
async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    now = datetime.utcnow() + timedelta(hours=3, minutes=30)  # ایران +3:30
    now_str = now.strftime("%H:%M")

    if user_id not in user_logs:
        user_logs[user_id] = []

    user_logs[user_id].append(f"{now_str} : {text}")
    await update.message.reply_text(f"{now_str} : {text}")

# نمایش همه پیام‌ها با تاریخ امروز
async def show_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    today = (datetime.utcnow() + timedelta(hours=3, minutes=30)).date()
    today_str = today.strftime("%Y-%m-%d")
    
    if user_id in user_logs and user_logs[user_id]:
        messages = "\n".join(user_logs[user_id])
        await update.message.reply_text(f"پیام‌های امروز {today_str}:\n{messages}")
    else:
        await update.message.reply_text("هیچ پیامی ثبت نشده است.")

# پاکسازی خودکار ساعت 12 شب
async def clear_logs_at_midnight(app):
    while True:
        now = datetime.utcnow() + timedelta(hours=3, minutes=30)
        next_midnight = datetime.combine(now.date() + timedelta(days=1), time())
        seconds_until_midnight = (next_midnight - now).total_seconds()
        await asyncio.sleep(seconds_until_midnight)
        user_logs.clear()
        print("تمام پیام‌ها پاک شد!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("show", show_logs))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_message))

    # اجرای تسک پاکسازی خودکار در پس‌زمینه
    app.job_queue.run_repeating(lambda _: clear_logs_at_midnight(app), interval=60, first=0)

    print("Bot running...")
    app.run_polling()
