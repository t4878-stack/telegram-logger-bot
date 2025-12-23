from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime

TOKEN = "BOT_TOKEN"


# دیکشنری برای ذخیره پیام‌ها به ازای هر کاربر
user_logs = {}

# دستور /start


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! پیام هاتو بفرست تا با زمان ثبت کنم.\n"
        "برای دیدن همه پیام‌ها /show رو بزن."
    )

# ذخیره پیام‌ها با زمان


async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    now = datetime.now().strftime("%H:%M")

    if user_id not in user_logs:
        user_logs[user_id] = []

    user_logs[user_id].append(f"ساعت {now} : {text}")
    await update.message.reply_text(f" ساعت {now} : {text}")

# نمایش همه پیام‌ها


async def show_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_logs and user_logs[user_id]:
        message = "\n".join(user_logs[user_id])
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("هیچ پیامی ثبت نشده است.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("show", show_logs))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, log_message))

    print("Bot running...")
    app.run_polling()
