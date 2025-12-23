# main.py
import json
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN ="BOT_TOKEN"
DATA_FILE = "daily_tasks.json"

# محاسبه زمان ایران بدون pytz
def iran_now():
    return datetime.utcnow() + timedelta(hours=3, minutes=30)

# فایل ذخیره‌سازی
def load_tasks():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# ---------- هندلرها ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! پیام‌های امروزت رو میتونی همینجا بنویسی. شب ساعت 12 جمع‌بندی می‌کنم.")

async def add_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    iran_time = iran_now().strftime("%Y-%m-%d %H:%M")
    tasks = load_tasks()
    tasks.append(f"{iran_time} - {text}")
    save_tasks(tasks)

async def show_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    if not tasks:
        await update.message.reply_text("هیچ کاری امروز ثبت نشده.")
        return
    message = "\n".join(tasks)
    await update.message.reply_text(f"کارهای امروزت:\n{message}")

# دکمه inline برای نمایش
async def show_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("نمایش کارهای امروز", callback_data="show")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("برای مشاهده کارهای امروز:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "show":
        tasks = load_tasks()
        if not tasks:
            await query.edit_message_text("هیچ کاری امروز ثبت نشده.")
        else:
            await query.edit_message_text("\n".join(tasks))

# ---------- جمع‌بندی اتوماتیک ----------
async def daily_summary(context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    if not tasks:
        return
    chat_id = context.job.chat_id
    summary = "\n".join(tasks)
    await context.bot.send_message(chat_id, f"💡 کارهای دیروز:\n{summary}")
    save_tasks([])

# ---------- برنامه اصلی ----------
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("show_button", show_button))
    app.add_handler(CommandHandler("show", show_tasks))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_message))
    app.add_handler(CallbackQueryHandler(button_callback))

    # زمان‌بندی جمع‌بندی ساعت 12 شب ایران
    scheduler = AsyncIOScheduler()
    CHAT_ID = "اینجا_چت_آیدی_تو"  # می‌توان از ENV گرفت
    scheduler.add_job(daily_summary, "cron", hour=0, minute=30, args=[app.job_queue], kwargs={"context": {"chat_id": int(CHAT_ID)}})
    scheduler.start()

    app.run_polling()
