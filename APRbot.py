import os
import threading
import logging
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

# 🔧 Логгирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔐 Переменные окружения
TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))  # Render задаёт порт

# 📊 Формулы расчёта
def calculate_apr(profit, principal, days):
    return (profit / principal) * (365 / days) * 100

def calculate_apy(profit, principal, days):
    period_rate = profit / principal
    return ((1 + period_rate) ** (365 / days) - 1) * 100

def calculate_roi(profit, principal):
    return (profit / principal) * 100

# 🟢 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send me 3 numbers: principal, profit, and days. Example:\n\n50000 108.47 15"
    )

# 📥 Обработка ввода
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    try:
        parts = update.message.text.split()
        if len(parts) != 3:
            raise ValueError("Wrong format")

        principal = float(parts[0].replace("_", "").replace(",", ""))
        profit = float(parts[1])
        days = int(parts[2])

        apr = calculate_apr(profit, principal, days)
        apy = calculate_apy(profit, principal, days)
        roi = calculate_roi(profit, principal)

        await update.message.reply_text(
            f"📈 ROI: {roi:.2f}%\n📉 APR: {apr:.2f}%\n🌱 APY: {apy:.2f}%"
        )

    except Exception:
        await update.message.reply_text("⚠️ Please send 3 values like:\n50000 108.47 15")

# 🌐 Flask для Render Web Service
web_app = Flask(__name__)

@web_app.route("/")
def index():
    return "Bot is running!"

def run_flask():
    web_app.run(host="0.0.0.0", port=PORT)

# 🚀 Запуск Telegram-бота и Flask
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))

    # Запуск Flask-сервера в отдельном потоке
    threading.Thread(target=run_flask).start()

    # Запуск Telegram polling
    application.run_polling()