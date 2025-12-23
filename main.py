import json
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

DATA_FILE = "daily_tasks.json"
CHAT_IDS = set()

def iran_now():
    return datetime.utcnow() + timedelta(hours=3, minutes=30)

def load_tasks():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    CHAT_IDS.add(update.message.chat_id)
    await update.message.reply_text("سلام! پیام‌های امروزت ذخیره می‌شوند و شب جمع‌بندی می‌کنم.")

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
    else:
        await update.message.reply_text("\n".join(tasks))

async def show_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("نمایش کارهای امروز", callback_data="show")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("برای مشاهده کارهای امروز:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tasks = load_tasks()
    if not tasks:
        await query.edit_message_text("هیچ کاری امروز ثبت نشده.")
    else:
        await query.edit_message_text("\n".join(tasks))

async def daily_summary():
    tasks = load_tasks()
    if not tasks:
        return
    summary = "\n".join(tasks)
    for chat_id in CHAT_IDS:
        await app.bot.send_message(chat_id, f"💡 کارهای دیروز:\n{summary}")
    save_tasks([])

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    print("Error: BOT_TOKEN is not set in environment!")
    exit(1)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("show_button", show_button))
app.add_handler(CommandHandler("show", show_tasks))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_message))
app.add_handler(CallbackQueryHandler(button_callback))

scheduler = AsyncIOScheduler()
scheduler.add_job(lambda: app.create_task(daily_summary()), "cron", hour=0, minute=0)
scheduler.start()

app.run_polling()
