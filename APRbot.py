import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Bot is running...")

# 📊 Формулы расчёта:
def calculate_apr(profit, principal, days):
    daily_rate = profit / principal
    apr = daily_rate * (365 / days) * 100
    return apr

def calculate_apy(profit, principal, days):
    period_rate = profit / principal
    periods_per_year = 365 / days
    apy = ((1 + period_rate) ** periods_per_year - 1) * 100
    return apy

def calculate_roi(profit, principal):
    return (profit / principal) * 100

# 🟢 /start команда:
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send me 3 numbers: principal, profit, and days. Example:\n\n50000 108.47 15"
    )

# 📥 Обработка пользовательского ввода:
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

    except Exception as e:
        await update.message.reply_text("⚠️ Please send 3 values like:\n50000 108.47 15")

# 🚀 Основной запуск:
if __name__ == "__main__":
    # ✅ ИСПРАВЛЕНО: имя переменной окружения
    TOKEN = os.environ.get("BOT_TOKEN")  # ← так ты должен был указать в Render

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))

    print("✅ Bot is running...")
    app.run_polling()