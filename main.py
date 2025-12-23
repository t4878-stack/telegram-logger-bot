from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime, timedelta

TOKEN = "8542143557:AAEwuIFQCmyEU1EmiCEixA738H0UumiBt1I"

# دیکشنری برای ذخیره پیام‌ها به ازای هر کاربر
user_logs = {}
# نگهداری تاریخ آخرین ثبت پیام
last_log_date = {}

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
    today_str = now.strftime("%Y-%m-%d")
    now_str = now.strftime("%H:%M")

    # اگر تاریخ تغییر کرده، حافظه رو پاک کن
    if user_id in last_log_date and last_log_date[user_id] != today_str:
        user_logs[user_id] = []

    last_log_date[user_id] = today_str

    if user_id not in user_logs:
        user_logs[user_id] = []

    user_logs[user_id].append(f" {now_str} : {text}")
    await update.message.reply_text(f" {now_str} : {text}")

# نمایش همه پیام‌ها
async def show_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    now = datetime.utcnow() + timedelta(hours=3, minutes=30)
    today_str = now.strftime("%Y-%m-%d")

    # اگر تاریخ تغییر کرده، حافظه رو پاک کن
    if user_id in last_log_date and last_log_date[user_id] != today_str:
        user_logs[user_id] = []
        last_log_date[user_id] = today_str

    if user_id in user_logs and user_logs[user_id]:
        message = f"پیام‌های امروز {now.strftime('%d %b %Y')}:\n" + "\n".join(user_logs[user_id])
        await update.message.reply_text(message)
    else:
        await update.message.reply_text(f"پیامی برای امروز {now.strftime('%d %b %Y')} ثبت نشده است.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("show", show_logs))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_message))

    print("Bot running...")
    app.run_polling()
