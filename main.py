from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime, timedelta
from persiantools.jdatetime import JalaliDate

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
    today_str = now.date().isoformat()  # YYYY-MM-DD برای ذخیره‌سازی روز

    if user_id not in user_logs:
        user_logs[user_id] = []

    user_logs[user_id].append((today_str, f"{now_str} : {text}"))
    await update.message.reply_text(f"{now_str} : {text}")

# نمایش پیام‌های امروز با تاریخ شمسی
async def show_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    now = datetime.utcnow() + timedelta(hours=3, minutes=30)
    today_str = now.date().isoformat()

    if user_id in user_logs:
        today_messages = [msg for date, msg in user_logs[user_id] if date == today_str]

        if today_messages:
            jalali_date = JalaliDate(now.date())
            message = f"پیام‌های امروز {jalali_date.strftime('%-d %B %Y')}\n" + "\n".join(today_messages)
            await update.message.reply_text(message)
        else:
            await update.message.reply_text("هیچ پیامی امروز ثبت نشده است.")
    else:
        await update.message.reply_text("هیچ پیامی ثبت نشده است.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("show", show_logs))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_message))

    print("Bot running...")
    app.run_polling()
